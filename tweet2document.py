from pattern.vector import Document, PORTER
import document_modifier

"""
This file transforms tweets into pattern.Document objects
that are then turned into a corpus --> a classifer.
SC 9/24/2013
"""


def create_tweet_document_index(tweets, tag, num=10000):
    """
            combines the caption and comment text from a media object
            and converts it into a Pattern.vecotor Document
            returns {id:Document(text,tag)}
    """
    document_index = {}
    for tid, tweet in tweets.iteritems():
        text = tweet.get('text', '')
        document_index[tid] = Document(
            document_modifier.pos_feature_builder(text.lower()),
            type=tag,
            stemmer=PORTER)
        if len(document_index) == num:
            print "trimming media {0} to documents {1}".format(len(tweets), num)
            return document_index

    return document_index
