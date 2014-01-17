import loadpickle
from instagram2document import create_instagram_document_index
import instagram2document
import tweet2document
import datetime


def create_doc_idx(tag_list, mode='instagram'):
    """
        turns a tag_list into an index of pattern documents
    """
    doc_idx = {}
    for tag in tag_list:
        tag_docs = create_tag_docs(tag)
        doc_idx.update(tag_docs)
    return doc_idx


def create_tag_docs(tag, label=None, count=None, mode='instagram'):
    """
        loads tags from file and turns them into documents
    """
    if not label:
        label = tag
    if mode == 'instagram':
        tag_media = loadpickle.get_all_tagpickles(tag, count, 'tag_pickles')
        tag_docs = create_instagram_document_index(tag_media, label)
    elif mode == 'twitter':
        tag_media = loadpickle.get_all_tagpickles(tag, count, 'tweet_pickles')
        tag_docs = create_tweet_document_index(tag_media, label)
    return tag_docs


class Tag2Document:
    """
        This class handles the convesion of a instagram Media object to a pattern document
    """

    def __init__(self, label, count, mode, max_documents=None):

        self.tag = None
        self.label = label
        self.mode = mode
        self.count = count
        self.max_documents = max_documents
        self.save_dir = 'tag_pickles' if self.mode == 'instagram' else 'tweet_pickles'
        print self

    def __str__(self):
        return (
            "tag = {0}, count = {1}, save = {2}, max_docs = {3}".format(
                self.tag,
                self.count,
                self.save_dir,
                self.max_documents)
        )

    def load_with_tag(self, tag):
        """
            creates tag documents for  <tag>
            contains timing logic for optimization
        """
        self.tag = tag
        print "loading documents with tag = {0}".format(self.tag)
        loadp_start = datetime.datetime.now()
        self.create_tag_media()
        loadp_end = datetime.datetime.now()
        duration = (loadp_end - loadp_start).seconds
        if duration == 0:
            duration = 1
        print "loaded {0} media objects from pickles in {1} seconds with a rate of {2} pickles/second".format(len(self.tag_media), duration, float(len(self.tag_media)) / float(duration))
        loaddoc_start = datetime.datetime.now()
        self.create_tag_docs()
        loaddoc_end = datetime.datetime.now()
        duration = (loaddoc_end - loaddoc_start).seconds
        if duration == 0:
            duration = 1

        num_docs = len(self.tag_docs)
        print "loaded {0} documents from media in {1} seconds with a rate of {2} documents/seconds".format(num_docs, duration, float(num_docs) / float(duration))

    def create_tag_media(self):
        """
            loads all the tag/media files for <self.tag>
        """
        print "creating_tag_media\t{0}".format(self)
        self.tag_media = loadpickle.get_all_tagpickles(
            self.tag,
            self.count,
            self.save_dir)
        if not self.max_documents:
            self.max_documents = len(self.tag_media)

    def create_tag_docs(self):
        """
            uses tweet2document and instagram2document to produce pattern.Document representations
        """
        print "creating_tag_docs\t{0}".format(self)

        if self.mode == 'twitter':
            tag_docs = tweet2document.create_tweet_document_index(
                self.tag_media,
                self.label,
                self.max_documents)
        elif self.mode == 'instagram':
            tag_docs = instagram2document.create_instagram_document_index(
                self.tag_media,
                self.label,
                self.max_documents)
        self.tag_docs = tag_docs
