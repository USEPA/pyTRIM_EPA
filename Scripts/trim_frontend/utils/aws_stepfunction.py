import json
import threading
import boto3
from .logging import make_logger

"""
To replace:
    fetch_output_for_step_function_execution
    get_complete_logs_from_group_and_stream
    get_step_function_results
"""


class StepfnxHelper:
    logger = make_logger("StepfnxHelper")

    sfn_client = boto3.client("stepfunctions")
    ecs_client = boto3.client("ecs")
    logs_client = boto3.client("logs")

    # stepfunction data
    status = ""
    output = {}
    logs = []

    # task data
    cluster_arn = None
    task_def_arn = None
    task_arn = None
    task_id = None

    # logging data
    container_name = ""
    log_group_name = ""
    log_group_prefix = "ecs"

    def __init__(self, execution_arn=None):
        self.execution_arn = execution_arn

    def start_stepfnx_execution(self, scn_id, statemachineArn):
        rsp = self.sfn_client.start_execution(
            stateMachineArn=statemachineArn,
            input=json.dumps({"scenarioId": str(scn_id), "generateFakeResults": "false"}),
        )
        return rsp["executionArn"]

    def get_stepfnx_status(self):
        self.logger.info("Checking stepfunction status...")

        exec_rsp = self.sfn_client.describe_execution(executionArn=self.execution_arn)
        self.status = exec_rsp.get("status", "").upper()

        if self.status == "SUCCEEDED":
            output = exec_rsp.get("output", "{}")
            parsed_output = json.loads(output)
            for key in parsed_output:
                self.output[key] = parsed_output[key]
        elif self.task_failed():
            self.status = "FAILED"
            self.logs = self.get_logs()

        return {"status": self.status, "output": self.output, "logs": self.logs}

    def fetch_task_metadata(self):
        # task information
        try:
            exec_hist_rsp = self.sfn_client.get_execution_history(executionArn=self.execution_arn)

            for evt in exec_hist_rsp.get("events", []):
                _details = evt.get("taskSubmittedEventDetails", {})
                if evt.get("type") == "TaskSubmitted" and _details.get("resourceType") == "ecs":
                    evt_details = json.loads(_details["output"])

                    tasks = evt_details.get("Tasks", [])
                    task = tasks[0] if len(tasks) > 0 else None
                    if not task:
                        return []

                    self.cluster_arn = task["ClusterArn"]
                    self.task_def_arn = task["TaskDefinitionArn"]
                    self.task_arn = task["TaskArn"]
                    self.task_id = self.task_arn.split("/")[-1]
        except Exception as e:
            return [f"Error fetching logs: {e}"]

        # logging, container information
        try:
            task_defs_rsp = self.ecs_client.describe_task_definition(taskDefinition=self.task_def_arn)
            container_defs = task_defs_rsp["taskDefinition"]["containerDefinitions"]
            if len(container_defs) > 1:
                self.logger.warning(f"More than one container definition found for [{self.task_def_arn}]")

            for container_def in task_defs_rsp["taskDefinition"]["containerDefinitions"]:
                self.container_name = container_def["name"]
                self.log_group_name = container_def["logConfiguration"]["options"]["awslogs-group"]
                self.log_group_prefix = container_def["logConfiguration"]["options"]["awslogs-stream-prefix"]
        except Exception as e:
            return [f"Error fetching logs: {e}"]

    def task_failed(self) -> bool | None:
        """
        Check if task failed
        Usually the step function won't stop running until it times out...
        """
        try:
            if not (self.cluster_arn and self.task_arn and self.container_name):
                self.fetch_task_metadata()

            task_def_resp = self.ecs_client.describe_tasks(
                cluster=self.cluster_arn,
                tasks=[self.task_arn],
            )
            for container in task_def_resp["tasks"][0]["containers"]:
                if container["name"] == self.container_name:
                    exit_code = container.get("exitCode")
                    return exit_code == 1
        except Exception:
            return None

    def get_logs(self):
        """
        Retrieve container logs from CloudWatch

        Pagination only done when "nextXToken" response
        from get_log_events equals the "nextToken" you had just passed in
        """
        log_stream_name = f"{self.log_group_prefix}/{self.container_name}/{self.task_id}"
        self.logger.info(f"Fetching logs from [{log_stream_name}]...")

        rv = []
        next_token = None
        try:
            for attempt in range(10):
                params = {
                    "logGroupName": self.log_group_name,
                    "logStreamName": log_stream_name,
                    "startFromHead": True,
                }

                if next_token is not None:
                    params["nextToken"] = next_token

                logs_rsp = self.logs_client.get_log_events(**params)
                log_events = logs_rsp.get("events", [])

                for evt in log_events:
                    rv.append({"timestamp": evt["timestamp"], "message": evt["message"]})

                if next_token is not None and logs_rsp["nextForwardToken"] == next_token:
                    break
                else:
                    next_token = logs_rsp["nextForwardToken"]
        except Exception as e:
            self.logger.warning(f"Could not retrieve logs: {e}")
        return self.sanitize_logs(rv)

    # FIXME -- only getflow for now... and should clean up entrypoint.py
    def sanitize_logs(self, logs):
        # "sanitize" but really we're just clipping out all the debugging before getflow start
        log_entrypoint = "app context attempt..."
        for i, log in enumerate(logs):
            if log_entrypoint in log["message"]:
                return logs[i:]
        return []

    # EXPERIMENTAL BACKGROUND POLLING
    def wait_for_task(self):
        def _wait():
            self.logger.info(f"Monitoring {self.container_name}...")
            waiter = self.ecs_client.get_waiter("tasks_stopped")
            try:
                waiter.wait(  # this is blocking!
                    cluster=self.cluster_arn,
                    tasks=[self.task_arn],
                    WaiterConfig={"Delay": 6, "MaxAttempts": 100},
                )
                self.logger.info(f"Task stopped for {self.container_name}")
            except Exception as e:
                self.logger.info(e)

        monitoring = threading.Thread(target=_wait, daemon=True)
        monitoring.start()
