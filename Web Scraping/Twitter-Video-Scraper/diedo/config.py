from requests_oauthlib import OAuth1


class Config(object):

    def __init__(self):
        self._get_tweet_ids()
        self._get_auth_creds()
        self._get_api_endpoint()
        super().__init__()

    # auth settings
    CONSUMER_KEY = "ZjwbfdfvSfQpTT9pqGywAduGQ"
    CONSUMER_SECRET = "KixWECgnICJ5QzHpoyH6Gfg8iv9tzJUhFCqj1PigRUzfWCQqJJ"
    ACCESS_TOKEN = "271849992-1VVc1zlotT6frUpUYOMk0Ghr04aptAUeTuZj8fvH"
    ACCESS_TOKEN_SECRET = "B86aJyc6U02ff0LQMkafMM5ZSlXH2oLZlCdmEIEVtJgBC"

    # properties
    auth = None
    poll_url = None
    tweet_url = None

    # data files path
    poll_path = "data/poll"
    tweet_path = "data/tweet"

    # poll ids
    tweet_ids = [
        "1339978750952390657",
    ]

    def _get_tweet_ids(self):
        return ",".join(self.tweet_ids)

    def _get_auth_creds(self):
        auth = OAuth1(
            self.CONSUMER_KEY,
            self.CONSUMER_SECRET,
            self.ACCESS_TOKEN,
            self.ACCESS_TOKEN_SECRET
        )
        self.auth = auth

    def _get_api_endpoint(self):
        url = f'https://api.twitter.com/2/tweets?ids={self._get_tweet_ids()}&expansions=attachments.poll_ids&poll.fields=duration_minutes,end_datetime,options,voting_status'
        self.poll_url = url
