import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    # fetch todo from the database

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    lang = event['pathParameters']['lang'] 
    
    # https://docs.aws.amazon.com/es_es/translate/latest/dg/translate-dg.pdf
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

    translate_text = translate.translate_text(Text=result['Item']['text'], SourceLanguageCode="auto", TargetLanguageCode=lang)
 
    # Anadimos nuevo index con el resultado de idioma traducido.
    result['Item']['text'] = translate_text['TranslatedText'] 

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
