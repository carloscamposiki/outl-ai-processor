import requests
from src.exception.blue_sky_exception import BlueSkyException
from src.adapter.api.token_manager import TokenManager
from datetime import datetime, timezone

class BlueSkyAPI:

    def __init__(self, token_generator: TokenManager):
        self.token_generator = token_generator

    def make_post(self, text: str) -> None:
        url = 'https://bsky.social/xrpc/com.atproto.repo.createRecord'
        token = self.token_generator.get_session().get_token()
        headers = {'Authorization': token}
        now = datetime.now(timezone.utc).isoformat().replace("-03:00", "Z")
        payload = {
            'repo': 'outoftheloop-ai.bsky.social',
            'collection': "app.bsky.feed.post",
            'record': {
                "$type": "app.bsky.feed.post",
                "text": text,
                "createdAt": now,
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise BlueSkyException(f'Failed to make post: {response.status_code} - {response.text}')
