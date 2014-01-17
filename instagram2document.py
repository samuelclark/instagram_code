import document_modifier
from pattern.vector import Document, PORTER
import datetime
import random


def create_instagram_document_index(media_dict, tag, num, comments=True):
    """
        combines the caption and comment text from a media object
        and converts it into a Pattern.vecotor Document
        returns {id:Document(text,tag)}
    """
    print_val = 5000
    document_index = {}
    parse_start = datetime.datetime.now()
    items = media_dict.items()
    random.shuffle(items)
    count = 0
    for mid, mobj in items:
        count += 1
        text_value = get_media_text(mobj)
        document_index[mid] = Document(text_value, type=tag, stemmer=PORTER,
                                       stopwords=True)
        if count % print_val == 0:
            parse_end = datetime.datetime.now()
            duration = (parse_end - parse_start).seconds
            if duration == 0:
                duration = 1
            print "num_parsed = {0} time = {1} parse/time = {2}".format(len(document_index), duration, float(print_val) / float(duration))
            parse_start = datetime.datetime.now()
        if len(document_index) == num:
            print "trimming media {0} to documents {1}".format(len(media_dict), num)
            return document_index
    return document_index


def get_media_text(
        mobj, modifier=document_modifier.unigram_bigram_text_feature, comments=True):
       # text = mobj.caption.text if mobj.caption else " "
        if mobj.caption:
            text = mobj.caption.text
        else:
            text = None
        if comments:
            comment_text = ' '.join(c.text for c in mobj.comments)
            if text:
                text = " ".join([text, comment_text])
            else:
                text = comment_text
            text_value = modifier(text)
        return text_value
            # print tag,text_value
