import unittest
from unittest.mock import MagicMock
from src.services.trends_processor import TrendsProcessor
from src.services.post_sender import PostSender
from src.services.summary_fetcher import SummaryFetcher


class TestTrendsProcessor(unittest.TestCase):

    def setUp(self):
        self.mock_post_sender = MagicMock(spec=PostSender)
        self.mock_summary_fetcher = MagicMock(spec=SummaryFetcher)
        self.processor = TrendsProcessor(
            post_sender=self.mock_post_sender,
            summary_fetcher=self.mock_summary_fetcher
        )

    def test_process_success(self):
        """ Test successful processing of trends """
        # Arrange
        trend_name = "Tech Trends"
        posts = ["Post 1", "Post 2"]
        summary = "This is a summary."

        self.mock_summary_fetcher.fetch.return_value = summary

        # Act
        self.processor.process(trend_name, posts)

        # Assert
        self.mock_summary_fetcher.fetch.assert_called_once_with(
            trend_name=trend_name, posts=posts
        )
        self.mock_post_sender.send.assert_called_once_with(
            trend_name, summary
        )

    def test_process_fetch_failure(self):
        """ Test when fetching the summary raises an exception """
        # Arrange
        trend_name = "Tech Trends"
        posts = ["Post 1", "Post 2"]

        self.mock_summary_fetcher.fetch.side_effect = ValueError("Fetch failed")

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.processor.process(trend_name, posts)
        self.assertEqual(str(context.exception), "Fetch failed")
        self.mock_summary_fetcher.fetch.assert_called_once_with(
            trend_name=trend_name, posts=posts
        )
        self.mock_post_sender.send.assert_not_called()


if __name__ == "__main__":
    unittest.main()
