import boto3

client = boto3.client('cognito-idp')

response = client.admin_create_user(
    UserPoolId='string',
    Username='string',
    UserAttributes=[
        {
            'Name': 'string',
            'Value': 'string'
        },
    ],
   
       
    MessageAction='SUPPRESS',
 
   
)
response = client.admin_set_user_password(
    UserPoolId='string',
    Username='string',
    Password='string',
    Permanent=True
)

response = client.initiate_auth(
    AuthFlow='USER_PASSWORD_AUTH'
    AuthParameters={
        'PASSWORD': 'valor de username'
        'PASSWORD': 'contraseña a poner'
    },
    
    ClientId='string',
    
    
)
boto3.client('cognito-idp', aws_access_key_id='key',
                              aws_secret_access_key='secret', region_name='us-east-1')