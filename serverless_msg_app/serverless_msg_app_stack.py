from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
)
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from constructs import Construct
import os

class ServerlessMsgAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 🔹 DynamoDB Table
        self.table = dynamodb.Table(
            self, "MessagesTable",
            partition_key=dynamodb.Attribute(
                name="messageUUID",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # 🔹 Lambda Function (Docker-based)
        lambda_fn = DockerImageFunction(
            self, "MessageProcessorFunction",
            code=DockerImageCode.from_image_asset(os.path.join(os.getcwd(), "lambda")),
            environment={
                "TABLE_NAME": self.table.table_name
            },
        )

        # 🔹 Grant DynamoDB write access to the Lambda
        self.table.grant_write_data(lambda_fn)
        # 🔹 API Gateway (Invoke Lambda via HTTP)
        api = apigw.LambdaRestApi(
            self, "MessageApi",
            handler=lambda_fn,
            proxy=False
        )

        # Define a POST method on /submit
        messages = api.root.add_resource("submit")
        messages.add_method("POST")  # POST /submit