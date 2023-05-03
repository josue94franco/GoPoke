from aws_cdk import aws_cognito as _cognito, RemovalPolicy, aws_iam as _iam, CfnOutput
from constructs import Construct


class Cognito(Construct):
    def __init__(self, scope: Construct, _id: str):
        super().__init__(scope, _id)

        self.user_pool = _cognito.UserPool(
            self,
            f"{scope.node.id}-cognito-userPool",
            self_sign_up_enabled=True,
            sign_in_aliases=_cognito.SignInAliases(email=True, phone=True),
            auto_verify=_cognito.AutoVerifiedAttrs(email=True, phone=True),
            password_policy=_cognito.PasswordPolicy(
                min_length=6,
                require_digits=False,
                require_lowercase=False,
                require_uppercase=False,
                require_symbols=False,
            ),
            account_recovery=_cognito.AccountRecovery.PHONE_AND_EMAIL,
            removal_policy=RemovalPolicy.RETAIN,
           )

        self.client_web = self.create_client(scope, "web", False)

        CfnOutput(self, "userPoolId", value=self.user_pool.user_pool_id)

        CfnOutput(self, "region", value=self.user_pool.env.region)

    def create_client(
        self, scope: Construct, name: str, generate_secret: bool = True
    ) -> _cognito.UserPoolClient:

        user_pool_client = _cognito.UserPoolClient(
            self,
            f"{scope.node.id}-{name}-Client",
            user_pool=self.user_pool,
            generate_secret=generate_secret,
            auth_flows=_cognito.AuthFlow(user_password=True, user_srp=True),
            supported_identity_providers=[
                _cognito.UserPoolClientIdentityProvider.COGNITO
            ],
            read_attributes=_cognito.ClientAttributes().with_standard_attributes(
                address=True,
                birthdate=True,
                email=True,
                family_name=True,
                fullname=True,
                gender=True,
                given_name=True,
                last_update_time=True,
                middle_name=True,
                nickname=True,
                phone_number=True,
                preferred_username=True,
                profile_picture=True,
                website=True,
            ),
            write_attributes=_cognito.ClientAttributes().with_standard_attributes(
                address=True,
                birthdate=True,
                email=True,
                family_name=True,
                fullname=True,
                gender=True,
                given_name=True,
                last_update_time=True,
                middle_name=True,
                nickname=True,
                phone_number=True,
                preferred_username=True,
                profile_picture=True,
                website=True,
            ),
        )

        identity_pool = _cognito.CfnIdentityPool(
            self,
            f"{scope.node.id}-{name}-identityPool",
            allow_unauthenticated_identities=False,
            cognito_identity_providers=[
                _cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                    client_id=user_pool_client.user_pool_client_id,
                    provider_name=self.user_pool.user_pool_provider_name,
                )
            ],
        )

        role_auth = _iam.Role(
            self,
            f"{scope.node.id}-{name}-auth-group-role",
            description="Default role for authenticated users",
            assumed_by=_iam.FederatedPrincipal(
                "cognito-identity.amazonaws.com",
                conditions={
                    "StringEquals": {
                        "cognito-identity.amazonaws.com:aud": identity_pool.ref
                    },
                    "ForAnyValue:StringLike": {
                        "cognito-identity.amazonaws.com:amr": "authenticated",
                    },
                },
                assume_role_action="sts:AssumeRoleWithWebIdentity",
            ),
        )

        role_unauth = _iam.Role(
            self,
            f"{scope.node.id}-{name}-unauth-group-role",
            description="Default role for anonymous users",
            assumed_by=_iam.FederatedPrincipal(
                "cognito-identity.amazonaws.com",
                conditions={
                    "StringEquals": {
                        "cognito-identity.amazonaws.com:aud": identity_pool.ref
                    },
                    "ForAnyValue:StringLike": {
                        "cognito-identity.amazonaws.com:amr": "unauthenticated",
                    },
                },
                assume_role_action="sts:AssumeRoleWithWebIdentity",
            ),
        )

        _cognito.CfnIdentityPoolRoleAttachment(
            self,
            f"identity-pool-{name}-role-attachment",
            identity_pool_id=identity_pool.ref,
            roles={
                "authenticated": role_auth.role_arn,
                "unauthenticated": role_unauth.role_arn,
            },
        )

        CfnOutput(self, f"{name}-clientId", value=user_pool_client.user_pool_client_id)

        CfnOutput(self, f"{name}-identityPoolId", value=identity_pool.ref)
        return user_pool_client
