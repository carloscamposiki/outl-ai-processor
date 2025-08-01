import boto3, json

class BedrockAdapter:
    def __init__(self, region: str = "us-east-1"):
        self.client = boto3.client("bedrock-runtime",
                                   region_name=region)

    def invoke_model(self, model_id: str, input_text: str) -> str:
        body = json.dumps(self._build_body(input_text))

        response = self.client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json"
        )
        # Bedrock streams the body as bytes; turn it into a dict, then text:
        output = json.loads(response["body"].read())
        return output['output']['message']['content'][0]['text']

    def _build_body(self, user_text: str) -> dict:
        inf_params = {"maxTokens": 500, "topP": 0.9, "topK": 20, "temperature": 0.7}
        system_list = [{"text": "You are a summarizer assistant."}]
        message_list = [{"role": "user", "content": [{"text": user_text}]}]
        return {
            "schemaVersion": "messages-v1",
            "messages": message_list,
            "system": system_list,
            "inferenceConfig": inf_params
        }
