import unittest
from unittest.mock import patch, MagicMock
from src.adapter.aws.bedrock import BedrockAdapter
import json

class TestBedrockAdapter(unittest.TestCase):

    @patch('src.adapter.aws.bedrock.boto3.client')
    def test_invoke_model_success(self, mock_boto_client):
        # Arrange
        mock_client_instance = MagicMock()
        mock_boto_client.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response['body'].read.return_value = b'{"result": "success"}'
        mock_client_instance.invoke_model.return_value = mock_response

        adapter = BedrockAdapter()
        model_id = "test-model"
        input_text = "test input"
        expected_body = {
            'prompt': input_text,
            'max_tokens_to_sample': 2000
        }

        # Act
        result = adapter.invoke_model(model_id, input_text)

        # Assert
        self.assertEqual(result, '{"result": "success"}')
        mock_client_instance.invoke_model.assert_called_once_with(
            modelId=model_id,
            body=json.dumps(expected_body),
            contentType='text/plain'
        )

    @patch('src.adapter.aws.bedrock.boto3.client')
    def test_invoke_model_failure(self, mock_boto_client):
        # Arrange
        mock_client_instance = MagicMock()
        mock_boto_client.return_value = mock_client_instance
        mock_client_instance.invoke_model.side_effect = Exception("Test error")

        adapter = BedrockAdapter()
        model_id = "test-model"
        input_text = "test input"
        expected_body = {
            'prompt': input_text,
            'max_tokens_to_sample': 2000
        }

        # Act & Assert
        with self.assertRaises(Exception) as context:
            adapter.invoke_model(model_id, input_text)
        self.assertIn("Test error", str(context.exception))
        mock_client_instance.invoke_model.assert_called_once_with(
            modelId=model_id,
            body=json.dumps(expected_body),
            contentType='text/plain'
        )


if __name__ == '__main__':
    unittest.main()
