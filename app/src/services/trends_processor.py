from src.services.post_sender import PostSender
from src.services.summary_fetcher import SummaryFetcher


class TrendsProcessor:

    def __init__(self,
                 post_sender: PostSender,
                 summary_fetcher: SummaryFetcher):
        self.post_sender = post_sender
        self.summary_fetcher = summary_fetcher

    def process(self, trend_name: str, posts:list[str]) -> None:
        summary = self.summary_fetcher.fetch(trend_name=trend_name,
                                             posts=posts)
        self.post_sender.send(summary)
