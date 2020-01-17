#!/usr/bin/env python3
"""
A standalone twitter client implementation
see https://tweepy.readthedocs.io/en/latest/
"""
import tweepy

# add these bad bois to your .env
consumer_key = "6UxH5PtAxe6a3xjLoTPNIBKCm"
consumer_secret = "Qzjmx8XZ1AbJqdfPGGaav6fnmTPhIOr7k8GcezHmP6w8CxqidO"
access_token = "894582349-JFgq2f5EMc7OyCTQ6T2udF4XTDSaPTFbLH3Nhp4U"
access_token_secret = "9t2meQJtccQc6QfKhoKBRAXIlU9fHdhFyGMmuJ54GeLmy"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class TwitterClient(tweepy.StreamListener):
    def __init__(self, api, filter_track, filter_hashtags, filter_usernames):
        """Initialize TwitterClient class"""
        self.api = api
        self.filter_track = filter_track
        self.filter_hashtags = filter_hashtags
        self.filter_usernames = filter_usernames

    def add_subscription(self, **kwargs):
        """
        Depending on what **kwargs you have it'll add that arg
        to it's respective list for filtering, and logs what
        was added to the console and log file
        """
        for arg in kwargs.keys():
            if arg == "track":
                self.filter_track.append(arg)
                print("Added {} as filter".format(arg))
                logger.info("Added {} as filter".format(arg))
            if arg == "username":
                self.filter_usernames.append(arg)
                print("Added {} as filter".format(arg))
                logger.info("Added {} as filter".format(arg))
            if arg == "hashtag":
                self.filter_hashtags.append(arg)
                print("Added {} as filter".format(arg))
                logger.info("Added {} as filter".format(arg))

    def remove_subscription(self, **kwargs):
        """
        Depending on what **kwargs you have it'll remvote hat arg
        from it's respective list for filtering, and logs what
        was removed to the console and log file
        """
        try:
            for arg in kwargs.keys():
                temp_arg = arg
                if arg == "track":
                    self.filter_track.remove(arg)
                    print("Removed {} as filter".format(arg))
                    logger.info("Removed {} as filter".format(arg))
                if arg == "username":
                    self.filter_usernames.remove(arg)
                    print("Removed {} as filter".format(arg))
                    logger.info("Removed {} as filter".format(arg))
                if arg == "hashtag":
                    self.filter_hashtags.remove(arg)
                    print("Removed {} as filter".format(arg))
                    logger.info("Removed {} as filter".format(arg))
        except Exception:
            print("{} isn't a filter right now".format(temp_arg))
            logger.error("{} isn't a filter right now".format(temp_arg))

    def filter_by_hashtag(self, status):
        """
        Returns true if the hashtags of the tweet searched
        match all the hashtags in the filter otherwise
        it returns false and an empty list if the hashtags don't match
        all the hashtags of the filter
        """
        # line comprehension to access the hashtags of each tweet
        hashtags_ = [hashtag['text'] for hashtag in
                     status.entities['hashtags']]
        # Are you able to make this error go away? Haha
        if not self.filter_hashtags or set(self.filter_hashtags).issubset(set(hashtags_)):
            print("Filtered by {}".format(self.filter_hashtags))
            logger.info("Filtered tweets by {}".format(self.filter_hashtags))
            return [True, hashtags_]
        return False, []

    def filter_by_username(self, status):
        """
        Returns true if the username of the tweet searched
        is one of the username filters
        """
        # name of the user to filter by
        name = status.user.name
        # if filter_usernames is empty or the tweet username is in
        # the list of usernames to filter by return true
        if not self.filter_usernames or name in self.filter_usernames:
            return True
            print("Filtered by {}".format(self.filter_usernames))
            logger.info("Filtered tweets by {}".format(self.filter_usernames))

    def current_filters(self):
        """ Logs the current filters used at the moment """
        if self.filter_usernames:
            print("{} is a filter at the moment"
                  .format(self.filter_usernames))
            logger.info("{} is a filter at the moment"
                        .format(self.filter_usernames))

        if self.filter_hashtags:
            print("{} is a filter at the moment"
                  .format(self.filter_hashtags))
            logger.info("{} is a filter at the moment"
                        .format(self.filter_hashtags))

        if self.filter_track:
            print("{} is a filter at the moment".format(self.filter_track))
            logger.info("{} is a filter at the moment"
                        .format(self.filter_track))

    def on_status(self, status):
        """
        Prints and logs tweets with the added filter of a username
        and hashtags if they're included
        """
        if TwitterClient.filter_by_username(self, status):
            flag, hashtags_ = TwitterClient.filter_by_hashtag(self, status)
            if flag:
                print(status.text, hashtags_)
                logger.info("Found tweet: {} {}".format(status.text,
                                                        hashtags_))


def main():
    """
    Sets the filters through command line args and starts the Twitter client
    """
    # filter text of tweet itself to contain the words in filter_track
    # but can be turned into a command line arg
    filter_track = ["cats", "dogs"]
    # hashtags to filter by
    # but can be turned into a command line arg
    filter_hashtags = ['botw']
    # filter the tweets to only come from this username
    # but can be turned into a command line arg
    filter_usernames = []
    myTwitterClientListener = TwitterClient(api, filter_track,
                                            filter_hashtags, filter_usernames)
    myTwitterClient = tweepy.Stream(auth=api.auth,
                                    listener=myTwitterClientListener)
    # myTwitterClientListener.add_subscription("boop")
    print(myTwitterClientListener.filter_track)
    print(myTwitterClient.filter(track=myTwitterClientListener.filter_track))


if __name__ == '__main__':
    main()
