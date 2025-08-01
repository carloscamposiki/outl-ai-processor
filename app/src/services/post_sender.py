from src.adapter.api.blue_sky_api import BlueSkyAPI

class PostSender:

    def __init__(self, blue_sky_api: BlueSkyAPI):
        self.blue_sky_api = blue_sky_api

    def send(self, content: str) -> None:
        if len(content) >= 300:
            raise ValueError("Content exceeds the maximum length of 299 characters.")
        try:
            self.blue_sky_api.make_post(content)
        except Exception as e:
            raise RuntimeError(f"Failed to send post: {e}")
