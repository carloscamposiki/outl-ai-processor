from src.adapter.api.blue_sky_api import BlueSkyAPI
from src.adapter.api.token_manager import TokenManager
from src.adapter.aws.secrets_manager import SecretsManager
from src.adapter.aws.bedrock import BedrockAdapter
from src.services.post_sender import PostSender
from src.services.summary_fetcher import SummaryFetcher
from src.services.trends_processor import TrendsProcessor
from src.services.prompt_builder import PromptBuilder
import os
import json

session_secret_name = os.getenv('SESSION_SECRET_NAME')
blue_sky_credentials_secret_name = os.getenv('BLUE_SKY_CREDENTIALS_SECRET_NAME')
bedrock_model_name = os.getenv('BEDROCK_MODEL_NAME')

secrets_manager = SecretsManager()
bedrock_client = BedrockAdapter()

token_manager = TokenManager(secrets_manager=secrets_manager,
                             session_secret_name=session_secret_name,
                             blue_sky_credentials_secret_name=blue_sky_credentials_secret_name)

blue_sky_api = BlueSkyAPI(token_manager)
prompt_builder = PromptBuilder()
summary_fetcher = SummaryFetcher(bedrock_adapter=bedrock_client,
                                 model_name=bedrock_model_name,
                                 prompt_builder=prompt_builder)
post_sender = PostSender(blue_sky_api)
trends_processor = TrendsProcessor(post_sender=post_sender,
                                   summary_fetcher=summary_fetcher)

def lambda_handler(event, __):
    if 'trend' in event:
        # This is a direct invocation with a trend
        trend = event['trend']
        posts = event['posts']
        trends_processor.process(trend, posts)
        return {
            'statusCode': 200
        }
    for sqs_record in event['Records']:
        trend = json.loads(sqs_record['body'])
        trends_processor.process(trend['trend'], trend['posts'])

    return {
        'statusCode': 200
    }
