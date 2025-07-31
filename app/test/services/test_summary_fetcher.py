import unittest
from unittest.mock import MagicMock
from src.services.summary_fetcher import SummaryFetcher
from src.adapter.aws.bedrock import BedrockAdapter
from src.services.prompt_builder import PromptBuilder


class TestSummaryFetcher(unittest.TestCase):

    def setUp(self):
        self.mock_bedrock_adapter = MagicMock(spec=BedrockAdapter)
        self.mock_prompt_builder = MagicMock(spec=PromptBuilder)
        self.model_name = "test-model"
        self.fetcher = SummaryFetcher(
            bedrock_adapter=self.mock_bedrock_adapter,
            prompt_builder=self.mock_prompt_builder,
            model_name=self.model_name
        )

    def test_fetch_success(self):
        """ Test when the summary is fetched successfully """
        # Arrange
        trend_name = "Tech Trends"
        posts = ["Post 1", "Post 2"]
        prompt = "Generated prompt"
        response = '{"status": true, "summary": "This is a summary."}'

        self.mock_prompt_builder.build.return_value = prompt
        self.mock_bedrock_adapter.invoke_model.return_value = response

        # Act
        result = self.fetcher.fetch(trend_name, posts)

        # Assert
        self.assertEqual(result, "This is a summary.")
        self.mock_prompt_builder.build.assert_called_once_with(
            trend_name=trend_name, posts=posts
        )
        self.mock_bedrock_adapter.invoke_model.assert_called_once_with(
            model_id=self.model_name, input_text=prompt
        )

    def test_fetch_failure(self):
        """ Test when the summary fetch fails due to model processing error """
        # Arrange
        trend_name = "Tech Trends"
        posts = ["Post 1", "Post 2"]
        prompt = "Generated prompt"
        response = '{"status": false}'

        self.mock_prompt_builder.build.return_value = prompt
        self.mock_bedrock_adapter.invoke_model.return_value = response

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.fetcher.fetch(trend_name, posts)
        self.assertEqual(str(context.exception), "Model failed to process summary request.")
        self.mock_prompt_builder.build.assert_called_once_with(
            trend_name=trend_name, posts=posts
        )
        self.mock_bedrock_adapter.invoke_model.assert_called_once_with(
            model_id=self.model_name, input_text=prompt
        )


if __name__ == "__main__":
    unittest.main()