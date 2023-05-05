import boto3


ClientId = '59cjg6sgfmblgiduoc6mdkrgcl',

client = boto3.client('cognito-idp')

"""response = client.admin_create_user(
    UserPoolId='us-west-2_NcDat1gRk',
    Username='josue_myspace@hotmail.com',
    UserAttributes=[
        {
            'Name': 'fullname',
            'Value': 'josue'
        },
    ],
    MessageAction='SUPPRESS',
)

response = client.admin_set_user_password(
    UserPoolId='us-west-2_NcDat1gRk',
    Username='josue_myspace@hotmail.com',
    Password='pepito23',
    Permanent=True
)"""
'''response = client.sign_up(
    ClientId='59cjg6sgfmblgiduoc6mdkrgcl',
    Username='josue_myspace@hotmail.com',
    Password='pepito23',
    UserAttributes=[
        {
            'Name': 'name',
            'Value': 'josue'
        },
    ],
)'''
#metodo para confirmar el codigo de verificacion que manda al correo
'''response = client.confirm_sign_up(
    ClientId='59cjg6sgfmblgiduoc6mdkrgcl',
    Username='josue_myspace@hotmail.com',
    ConfirmationCode='279721',
    ForceAliasCreation=False,
)'''
#este metodo se utiliza para iniciar sesion 
response = client.initiate_auth(
    AuthFlow='USER_PASSWORD_AUTH',
    AuthParameters={
        'USERNAME': 'josue_myspace@hotmail.com',
        'PASSWORD': 'pepito23'
    },
   
    
    ClientId='59cjg6sgfmblgiduoc6mdkrgcl',
    
)
#Se utiliza cuando el codigo de verificación ha expitado y es necesario generar uno nuevo
'''response = client.resend_confirmation_code(
    ClientId='59cjg6sgfmblgiduoc6mdkrgcl',
    Username='josue_myspace@hotmail.com',
)'''
   
print(response)

