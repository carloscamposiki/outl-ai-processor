from src.adapter.api.blue_sky_api import BlueSkyAPI

class PostSender:

    def __init__(self, blue_sky_api: BlueSkyAPI):
        self.blue_sky_api = blue_sky_api

    def send(self, trend_name: str, content: str) -> None:
        body = f'"{trend_name}": {content}'
        try:
            self.blue_sky_api.make_post(body)
        except Exception as e:
            raise RuntimeError(f"Failed to send post: {e}")
