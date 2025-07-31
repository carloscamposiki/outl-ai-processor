import unittest
from unittest.mock import MagicMock, patch
from src.adapter.api.blue_sky_api import BlueSkyAPI
from src.exception.blue_sky_exception import BlueSkyException
from src.adapter.api.token_manager import TokenManager


class TestBlueSkyAPI(unittest.TestCase):

    def setUp(self):
        self.mock_token_manager = MagicMock(spec=TokenManager)
        self.mock_session = MagicMock()
        self.mock_token_manager.get_session.return_value = self.mock_session
        self.mock_session.get_token.return_value = "mock_token"
        self.blue_sky_api = BlueSkyAPI(token_generator=self.mock_token_manager)

    @patch('src.adapter.api.blue_sky_api.requests.post')
    def test_make_post_success(self, mock_post):
        """ Test successful post creation """
        # Arrange
        text = "Test post content"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Act
        self.blue_sky_api.make_post(text)

        # Assert
        mock_post.assert_called_once_with(
            'https://bsky.social/xrpc/app.bsky.unspecced.makePost',
            json={'text': text},
            headers={'Authorization': 'mock_token'}
        )

    @patch('src.adapter.api.blue_sky_api.requests.post')
    def test_make_post_failure(self, mock_post):
        """ Test when post creation fails """
        # Arrange
        text = "Test post content"
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        # Act & Assert
        with self.assertRaises(BlueSkyException) as context:
            self.blue_sky_api.make_post(text)

        self.assertEqual(
            str(context.exception),
            'Failed to make post: 500 - Internal Server Error'
        )
        mock_post.assert_called_once_with(
            'https://bsky.social/xrpc/app.bsky.unspecced.makePost',
            json={'text': text},
            headers={'Authorization': 'mock_token'}
        )


if __name__ == '__main__':
    unittest.main()
