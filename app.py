#!/usr/bin/env python3

import os
from aws_cdk import (
    core as cdk,
    aws_lambda as _lambda,
    aws_lambda_nodejs as _node_lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_secretsmanager as sm
)

class cron_fn_stack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        secret = sm.Secret.from_secret_arn(self, "SLACK_TOKEN", 
            secret_arn=os.getenv('SLACK_TOKEN_ARN')
        )

        fn = _node_lambda.NodejsFunction(self, "good-morning-fn",
            entry="../good-morning-bot/index_lambda.js",
            deps_lock_file_path="../good-morning-bot/package-lock.json",
            environment={
                "SLACK_TOKEN": secret.secret_value.to_string()
            }
        )

        events.Rule(self, "cron-morning",
            schedule=events.Schedule.cron(hour="9", week_day="MON-FRI"),
            targets=[targets.LambdaFunction(handler=fn)]
        )

app = cdk.App()
cron_fn_stack(app, 'stack')
app.synth()
