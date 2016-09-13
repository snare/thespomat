import sys
import twitter
import time
import requests
import pysrt
import thespomat


class ThespomatBot(object):
    def __init__(self, config=None):
        if not config:
            self.config = thespomat.config
        self.creds = None

        # check config
        c = self.config.api_keys
        for s in [c.consumer_key, c.consumer_secret, c.access_key, c.access_secret]:
            if s == 'xxx':
                raise ConfigException("No twitter API keys found")

        # load srt
        self.load_srt()

    def load_srt(self):
        """
        Grab the SRT file and parse it
        """
        print("Loading SRT")
        self.srt = None
        if self.config.srt_url:
            r = requests.get(self.config.srt_url)
            if r.status_code == 200:
                self.srt = pysrt.from_string(r.text)
            else:
                print("Failed to retrieve SRT: {}".format(r))
        else:
            raise ConfigException("No SRT URL specified")

    def auth(self):
        """
        Authenticate with twitter.
        """
        print("Authenticating...")
        c = self.config.api_keys
        self.api = twitter.Api(consumer_key=c.consumer_key,
                               consumer_secret=c.consumer_secret,
                               access_token_key=c.access_key,
                               access_token_secret=c.access_secret)
        self.creds = self.api.VerifyCredentials()
        print("Authenticated as '{}'".format(self.creds.screen_name))
        print("Credentials: {}".format(self.creds))

        if self.config.test_mode:
            print("Running in test mode")
            self.api.PostUpdate = self.test_post_update

    def loop(self):
        """
        Just tweet the damn movie forever.
        """
        print("Loop it through Jones...")

        while True:
            last_s = None
            for s in self.srt:
                if last_s:
                    t = (s.start.minutes * 60 + s.start.seconds) - (last_s.start.minutes * 60 + last_s.start.seconds)
                    print("Sleeping {}".format(t))
                    time.sleep(t)
                last_s = s

                if len(s.text) <= 140:
                    twoots = [s.text]
                else:
                    twoots = []
                    for line in s.text.split('\n'):
                        twoots.extend([line[i:i + 140] for i in range(0, len(line), 140)])
                for t in twoots:
                    while True:
                        print(u"Tweeting: {}".format(t))
                        try:
                            self.api.PostUpdate(t)
                            break
                        except Exception as e:
                            print("Failed to twoot, sleeping {}: {}".format(self.config.rate_limit_delay, e))
                            if e.message[0]['code'] == 185:
                                time.sleep(self.config.rate_limit_delay)
                            else:
                                break

    def clear(self):
        """
        Clear the timeline.
        """
        while len(self.api.GetUserTimeline()):
            for tweet in self.api.GetUserTimeline():
                print("Deleting tweet id {}".format(tweet.id))
                self.api.DestroyStatus(tweet.id)

    def test_post_update(self, *args, **kwargs):
        print("PostUpdate(): args = {} kwargs = {}".format(args, kwargs))
