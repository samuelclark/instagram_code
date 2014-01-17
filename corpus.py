import tag2docidx
from pattern.vector import Corpus
import random


def create_posneg_corpus(pos_tags, neg_tags, count=None,
                         mode='instagram', max_docs=None):
    """
            Creates a document index of pos_tags with label 'positive'
            and a document index of neg_tags with label 'negative'
    """
    pos_label = 'positive'
    neg_label = 'negative'
    pos_media = {}
    neg_media = {}
    # turn each pos/neg tag object into a document
    pos_t2d = tag2docidx.Tag2Document(pos_label, count, mode, max_docs)
    neg_t2d = tag2docidx.Tag2Document(neg_label, count, mode, max_docs)

    # iterate through pos tags
    for each in pos_tags:
        pos_t2d.load_with_tag(each)
        pos_docs = pos_t2d.tag_docs
        pos_media.update(pos_docs)

    # iterate through neg tags
    for each in neg_tags:
        neg_t2d.load_with_tag(each)
        neg_docs = neg_t2d.tag_docs
        neg_media.update(neg_docs)

    # get rid of excess pos tags
    if len(pos_media) > len(neg_media):
        diff = int(len(pos_media)) - len(neg_media)
        keys = pos_media.keys()
        random.shuffle(keys)
        print "removing {0} pos docs".format(diff)
        [pos_media.pop(key) for key in keys[:diff] if diff >= 1]

    # or get rid of excess neg tags (it is about balancing the corpus)
    elif len(neg_media) > len(pos_media):
        diff = int(len(neg_media)) - len(pos_media)
        keys = neg_media.keys()
        random.shuffle(keys)
        print "removing {0} neg docs".format(diff)
        [neg_media.pop(key) for key in keys[:diff] if diff >= 1]

    print "pos_media = {0}, neg_media = {1}".format(len(pos_media), len(neg_media))
    pos_media.update(neg_media)
    posneg_corp = create_corpus(pos_media)
    return posneg_corp


def create_corpus(document_index):
    """
            creates a Pattern.vector Corpus from a {did:Document}
    """
    print "creating Corpus with {0} Documents".format(len(document_index))
    docs = document_index.values()
    for i in range(3):
        random.shuffle(docs)
    corp = Corpus(documents=docs)
    return corp


def create_taglist_corpus(tag_file_list, count=None, mode='instagram'):
    """
            creates a corpus from all the tags
    """
    taglist_docidx = {}
    for tag_file in tag_file_list:
        tag_docs = create_tag_docs(tag_file, count=count, mode=mode)
        taglist_docidx.update(tag_docs)
    taglist_corp = create_corpus(taglist_docidx)
    return taglist_corp
