try:
    import unzip_requirements
except ImportError:
    pass
from model.model import TranslatorModel_fr_en
import json

src = 'fr'
trg = 'en'

model_path = './model'
bucket_name = 's3bucket'
model_prefix = f'Marian_pytorch_model_{src}-{trg}.bin'

model = TranslatorModel_fr_en(model_path=model_path, s3_bucket=bucket_name, model_prefix=model_prefix)

def translate(event, context):
    try:
        print(event['body'])
        body = json.loads(event['body'])
        translated_text = model.predict(body['text'])

        return {
				'statusCode': 200,
				'headers': {
					'Content-Type': 'application/json',
	                'Access-Control-Allow-Origin': '*',
	                "Access-Control-Allow-Credentials": True
				},
				'body': json.dumps({'translated_text': translated_text})
        }
        
    except Exception as e:
        print(repr(e))
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            'body': json.dumps({"error": repr(e)})
        }