import requests
import json
import boto3
import os
from dynamodb_json import json_util
from select import error


# se crea un cliente de dynamodb
client = boto3.resource('dynamodb')
tabla = client.Table(os.environ["POKETABLE"])

# contenido de servicio de Lambda.
def handler(event, context):
    try:

        query = event.get("queryStringParameters")
        name = query.get("name")

        # consultar la tabla para ver si esta el pokemon solicitado
        response = tabla.get_item(

            Key={
                "name": name
            }
        )

        # Validar el nombre de del pokemon dentro  de la tabla para ya no consultar desde el api gateway.
        if response is not None and 'Items' in response:
            result = json_util.loads(response['Items'])
        else:

            url = f"https://pokeapi.co/api/v2/pokemon/{name}"
            response = requests.get(
                url,

                # es tiempo maximo que se da para que responda la petición.
                timeout=25,
            )
            # El guardado en la tabla de DynamoDB.
            result = response.json()
            result["name"] = name
            response = tabla.put_item(

                Item=result
            )
        # la respuesta del servicio de la lambda y del api
        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'isBase64Encoded': False,
            # los headers son los encabezados principales del servicio
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,Accept,Accept-Encoding,Connection,x-api-key',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,PATCH,DELETE,HEAD',
                'Access-Control-Max-Age': '86400'
            }
        }
    except Exception:
        exc_type, exc_value, exc_traceback = error

        return {
            'statusCode': 400,
            'body': json.dumps(error),
            'isBase64Encoded': False,
            # los headers son los encabezados principales del servicio
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,Accept,Accept-Encoding,Connection,x-api-key',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,PATCH,DELETE,HEAD',
                'Access-Control-Max-Age': '86400'
            }
        }
        return (400)
    
   
    
    
