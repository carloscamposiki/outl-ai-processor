from src.adapter.aws.bedrock import BedrockAdapter
from src.services.prompt_builder import PromptBuilder
import json

class SummaryFetcher:

    def __init__(self,
                 bedrock_adapter: BedrockAdapter,
                 prompt_builder: PromptBuilder,
                 model_name: str):
        self.bedrock_adapter = bedrock_adapter
        self.prompt_builder = prompt_builder
        self.model_name = model_name

    def fetch(self, trend_name: str, posts: list[str]) -> str:
        prompt = self.prompt_builder.build(trend_name=trend_name,
                                           posts=posts)
        response = self.bedrock_adapter.invoke_model(model_id=self.model_name,
                                                     input_text=prompt)
        result = json.loads(response)
        if not result['status']:
            raise ValueError("Model failed to process summary request.")
        return result['summary']
