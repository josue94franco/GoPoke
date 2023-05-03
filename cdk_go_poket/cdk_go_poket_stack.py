from aws_cdk import (
    # Duration,
    Stack,
    aws_dynamodb as dynamodb_cdk,
    aws_lambda as lambda_cdk,
    aws_apigateway as apigateway_cdk,
    
    RemovalPolicy
    # aws_sqs as sqs,
)
from constructs import Construct
from Cognito.cognito import Cognito

class CdkGoPoketStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # contructor de Layer
        lyr = lambda_cdk.LayerVersion(self, "MyLayer",
                                      removal_policy=RemovalPolicy.RETAIN,
                                      code=lambda_cdk.Code.from_asset("./Layers/dependencias"),
                                      compatible_runtimes=[lambda_cdk.Runtime.PYTHON_3_9],
                                      )

        # definicion de función lambda
        fn = lambda_cdk.Function(self, "MyFunction", function_name="mylambda",
                                 runtime=lambda_cdk.Runtime.PYTHON_3_9,
                                 handler="lambdas.handler",
                                 code=lambda_cdk.Code.from_asset("./Lambdas"),
                                 layers=[lyr]
                                 )

        # creación de tabala de dynamodb
        table = dynamodb_cdk.Table(self, "salida", table_name="salida",
                                   partition_key=dynamodb_cdk.Attribute(
                                       name="name", type=dynamodb_cdk.AttributeType.STRING),
                                   billing_mode=dynamodb_cdk.BillingMode.PAY_PER_REQUEST,

                                   )
        # para dar permisos a la función de acceder a la tabla.
        table.grant_read_write_data(fn)

        # variable de entorno para que en el lambda podamos accerder a la tabla
        fn.add_environment("POKETABLE", table.table_name)

        cognito = Cognito(self, "cognito")
        # creación de API Gateway
        api = apigateway_cdk.RestApi(self, "ChallengeTecnicoApi",
                                     default_cors_preflight_options=apigateway_cdk.CorsOptions(
                                         status_code=200,
                                         allow_origins=apigateway_cdk.Cors.ALL_ORIGINS,
                                         allow_methods=apigateway_cdk.Cors.ALL_METHODS
                                     ),
                                     )
        auth = apigateway_cdk.CognitoUserPoolsAuthorizer(
            self,
            f"{scope.node.id}-authorizer",
            cognito_user_pools=[cognito.user_pool],
            identity_source="method.request.header.Authorization",
        )

        # armando el endpoint
        endpoint = api.root.add_resource("pokemon")
        nombre = endpoint.add_resource("{name}")
        nombre.add_method(
            "GET",
            apigateway_cdk.LambdaIntegration(
                fn,
                proxy=True,
                passthrough_behavior=apigateway_cdk.PassthroughBehavior.NEVER
            ),
            method_responses=[apigateway_cdk.MethodResponse(status_code="200")],
            authorization_type=apigateway_cdk.AuthorizationType.COGNITO,
            authorizer=auth,
        )

# falta prueba de despliegue!!!!
# Falta validación en Postman!
