import requests
import json
import boto3
import os
from dynamodb_json import json_util

#se crea un cliente de dynamodb
client = boto3.client('dynamodb')

#contenido de servicio de Lambda.
def handler (event, context ):
    query = event.get("queryStringParameters")
    name = query.get("name")
    
    #consultar la tabla para ver si esta el pokemon solicitado
    response = client.get_item(
    TableName=os.environ["POKETABLE"],
    Key={
        "name": name 
    }
    )
    
    #Validar el nombre de del pokemos dentro  de la tabla para ya no consultar desde el api gateway.
    if response is not None and 'Items' in response:
            result = json_util.loads(response['Items'])
    else :
          


        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(
                url,
                         
                timeout=25, # es tiempo maximo que se da para que responda la petición.
            )
            #El guardado en la tabla de DynamoDB.
        result = response.text
        result["name"] = name
        response = client.put_item(
        TableName=os.environ["POKETABLE"], #VAriable de entorno 
        Item= result
    )
    #la respuesta del servicio de la lambda y del api
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


