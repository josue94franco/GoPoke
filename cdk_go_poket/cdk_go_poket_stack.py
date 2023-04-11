from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb_cdk,
    aws_lambda as lamda_cdk,
    aws_apigateway as apigateway_cdk,

    # aws_sqs as sqs,
)
from constructs import Construct


class CdkGoPoketStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

# definicion de función lambda
        fn = lambda_cdk_.Function(self, "MyFunction", funcion_name="mylambda"
                                  runtime=lambda_.Runtime.PYTHON_3_9,
                                  handler="lambdas.handler",
                                  code=lambda_cdk.Code.from_asset("./Lambdas")

                                  )
        # creación de tabala de dynamodb
        table = dynamodb_cdk.Table(self, "Table", table_name="salida"
                                   partition_key=dynamodb_cdk.Attribute(
                                       name="name", type=dynamodb_cdk.AttributeType.STRING),
                                   billing_mode=dynamodb_cdk.BillingMode.PAY_PER_REQUEST,

                                   )
        # para dar permisos a la función de acceder a la tabla.
        table.grant_read_write_data(fn)

# variable de entorno para que en el lambda podamos accerder a la tabla
        fn.add_environment("POKETABLE", table.table_name)


# creación de API Gateway
        api = apigateway_cdk.RestApi( self, "ChallengeTecnicoApi", default_cors_preflight_options=apigateway_cdk.CorsOptions(
            status_code=200,
            allow_origins=apigateway_cdk.Cors.ALL_ORIGINS,
            allow_methods=apigateway_cdk.Cors.ALL_METHODS
        ),)

# armando el endpoint
        endpoint = api.root.add_resource("pokemon")
        endpoint.add_method(
                "GET",
                apigateway_cdk.LambdaIntegration(
                    fn,
                    proxy=True,
                    passthrough_behavior=apigateway_cdk.PassthroughBehavior.NEVER
                ),
                method_responses=[apigateway_cdk.MethodResponse(status_code="200")]
            )


    
