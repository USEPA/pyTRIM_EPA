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
