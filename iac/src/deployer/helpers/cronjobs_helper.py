import boto3, getopt, os, sys
from common import (
    await_stack_completion,
    extract_output_val,
    die,
    figure_parent_dir,
    whoami_aws,
    loggy,
)

# setup scheduled startup/shutdown


class CronjobsHelper(object):
    def __init__(self):
        pass

    def create_cronjobs(self, stack_name, crons):
        try:
            if crons.get("ec2"):
                self.create_ec2_cronjobs(stack_name, crons["ec2"])

            # if crons.get("rds"):
            #    self.create_rds_cronjobs(stack_name, crons["rds"])

        except Exception as e:
            print(e)
            return {"status": "error"}

        return {"status": "success"}

    # EC2 autoscaling scheduled actions
    def create_ec2_cronjobs(self, stack_name, crons):
        autoscaling_client = boto3.client("autoscaling")
        groups = autoscaling_client.describe_auto_scaling_groups(
            Filters=[
                {
                    "Name": "tag:Name",
                    "Values": [
                        f"{stack_name}-web",
                        f"{stack_name}-bastionhost",
                    ],
                },
            ]
        )

        for group in groups["AutoScalingGroups"]:
            for job in crons:
                autoscaling_client.put_scheduled_update_group_action(
                    AutoScalingGroupName=group["AutoScalingGroupName"],
                    ScheduledActionName=job["name"],
                    DesiredCapacity=job["capacity"],
                    MinSize=job.get("min_capacity") or job["capacity"],
                    MaxSize=job.get("max_capacity") or job["capacity"],
                    Recurrence=job["cron_expression"],
                    TimeZone=job.get("timezone") or "America/New_York",
                )

        loggy("All EC2 cronjobs created successfully")

    # RDS maintenance start stop schedule
    def create_rds_cronjobs(self, stack_name, crons):
        self.create_resource_group(stack_name)

        rds_client = boto3.client("rds")
        rds_instance = rds_client.describe_db_instances(
            DBInstanceIdentifier=f"{stack_name}-mysql"
        )
        rds_instance = rds_instance["DBInstances"][0]

        ssm_client = boto3.client("ssm")
        maintenance_windows = ssm_client.describe_maintenance_windows()[
            "WindowIdentities"
        ]
        maintenance_windows = [w["Name"] for w in maintenance_windows]

        for job in crons:
            maintenance_name = f"{stack_name}-{job['name']}"
            if maintenance_name not in maintenance_windows:
                loggy(f"Skipping existing maintenance window [{maintenance_name}]...")
                continue

            window_id = ssm_client.create_maintenance_window(
                Name=maintenance_name,
                Description=job["name"],
                ScheduleTimezone=job.get("timezone") or "America/New_York",
                Schedule=f'cron({job["cron_expression"]})',
                Duration=job.get("duration") or 1,
                Cutoff=job.get("cutoff") or 0,
                AllowUnassociatedTargets=False,
            )["WindowId"]

            # TODO
            # associate the maintenance window with the rds instance
            window_target_id = ssm_client.register_target_with_maintenance_window(
                Name=f"{maintenance_name}-target",
                WindowId=window_id,
                ResourceType="INSTANCE",
                Targets=[
                    {
                        "Key": "InstanceIds",
                        "Values": [*self.get_ec2_instance_ids(rds_instance)],
                    }
                ],
            )["WindowTargetId"]

            # TODO
            ssm_client.register_task_with_maintenance_window()

        loggy("All RDS cronjobs created successfully")

    def create_resource_group(self, stack_name):
        import json

        (stack_id, outputs) = await_stack_completion(stack_name)
        rg_client = boto3.client("resource-groups")
        try:
            rg_client.create_group(
                Name=f"{stack_name}-rds-startstop",
                Description="RDS automated startup and shutdown",
                ResourceQuery={
                    "Type": "CLOUDFORMATION_STACK_1_0",
                    "Query": json.dumps(
                        {
                            "StackIdentifier": stack_id,
                            "ResourceTypeFilters": ["AWS::RDS::DBInstance"],
                        }
                    ),
                },
            )
        except Exception as e:
            if "group already exists" not in repr(e):
                raise Exception(repr(e))
