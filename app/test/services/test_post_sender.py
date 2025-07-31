import unittest
from unittest.mock import MagicMock
from src.services.post_sender import PostSender
from src.adapter.api.blue_sky_api import BlueSkyAPI


class TestPostSender(unittest.TestCase):

    def setUp(self):
        self.mock_blue_sky_api = MagicMock(spec=BlueSkyAPI)
        self.post_sender = PostSender(blue_sky_api=self.mock_blue_sky_api)

    def test_send_success(self):
        """ Test successful post sending """
        # Arrange
        trend_name = "Tech Trends"
        content = "This is a summary."
        expected_body = '"Tech Trends": This is a summary.'

        # Act
        self.post_sender.send(trend_name, content)

        # Assert
        self.mock_blue_sky_api.make_post.assert_called_once_with(expected_body)

    def test_send_failure(self):
        """ Test when sending a post raises an exception """
        # Arrange
        trend_name = "Tech Trends"
        content = "This is a summary."
        self.mock_blue_sky_api.make_post.side_effect = Exception("API error")

        # Act & Assert
        with self.assertRaises(RuntimeError) as context:
            self.post_sender.send(trend_name, content)
        self.assertEqual(str(context.exception), "Failed to send post: API error")
        self.mock_blue_sky_api.make_post.assert_called_once_with('"Tech Trends": This is a summary.')


if __name__ == "__main__":
    unittest.main()
