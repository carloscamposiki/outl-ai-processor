import boto3
import json

class BedrockAdapter:

    def __init__(self):
        self.client = boto3.client('bedrock-runtime',
                                    region_name='us-east-1')

    def invoke_model(self, model_id: str, input_text: str) -> str:
        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(self.build_body(input_text)),
                contentType='application/json'
            )
            return response['body'].read().decode('utf-8')
        except Exception as e:
            print(f'Error invoking Bedrock model {model_id}: {e}')
            raise

    def build_body(self, input_text: str) -> dict:
        return {
            'prompt': f'\n\nHuman:\n\n{input_text}\n\nAssistant:\n\n',
            'max_tokens_to_sample': 2000
        }
