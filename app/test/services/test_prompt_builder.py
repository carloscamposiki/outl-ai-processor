import unittest
from unittest.mock import patch, mock_open
from src.services.prompt_builder import PromptBuilder

class TestPromptBuilder(unittest.TestCase):

    @patch("builtins.open",
           new_callable=mock_open,
           read_data="Hello [trend_name], here are the posts:\n[posts]")
    def test_read_prompt_template(self, mock_file):
        builder = PromptBuilder()
        self.assertEqual(builder.prompt_template, "Hello [trend_name], here are the posts:\n[posts]")

    @patch("builtins.open",
           new_callable=mock_open,
           read_data="Hello [trend_name], here are the posts:\n[posts]")
    def test_build_prompt(self, mock_file):
        """ Test building a prompt with a trend name and posts """
        # Arrange
        builder = PromptBuilder()
        trend_name = "Tech Trends"
        posts = ["Post 1", "Post 2", "Post 3"]
        expected_prompt = "Hello Tech Trends, here are the posts:\nPost 1\nPost 2\nPost 3"

        # Act
        result = builder.build(trend_name, posts)

        # Assert
        self.assertEqual(result, expected_prompt)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_prompt_template_file_not_found(self, mock_file):
        """ Test when the prompt template file is not found """
        # Arrange & Act
        with self.assertRaises(Exception) as context:
            PromptBuilder()
        self.assertEqual(str(context.exception), "Prompt template file not found.")

if __name__ == "__main__":
    unittest.main()