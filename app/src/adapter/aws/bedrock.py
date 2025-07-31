import boto3


class BedrockAdapter:

    def __init__(self):
        self.client = boto3.client('bedrock-runtime',
                                    region_name='us-east-1')

    def invoke_model(self, model_id: str, input_text: str) -> str:
        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=input_text,
                contentType='text/plain'
            )
            return response['body'].read().decode('utf-8')
        except Exception as e:
            print(f'Error invoking Bedrock model {model_id}: {e}')
            raise
