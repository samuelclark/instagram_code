import os
from pattern.vector import Corpus, Document, PORTER


def create_weib_document_index(weib_lexicon):
    """
            combines the caption and comment text from a media object
            and converts it into a Pattern.vecotor Document
            returns {id:Document(text,tag)}
    """
    document_index = {}
    for wid, wobj in weib_lexicon.iteritems():
        text = wobj['text']
        tag = wobj['label']
        print tag
        document_index[wid] = Document(text, type=tag, stemmer=PORTER)
    return document_index


def get_weib():
    lexicon_file = 'subclues_weib.tff'
    lexicon_file = os.path.join('resources', lexicon_file)
    doc_idx = {}
    if os.path.exists(lexicon_file):
        with open(lexicon_file, 'rb') as lexicon:
            get_value = lambda idx: line[idx].split("=")[1]
            for line in lexicon:
                line = line.split()
                try:
                    key = "_".join([line[2], line[3]])
                    doc_idx[key] = {'text': get_value(
                        2),
                        'pos': get_value(3),
                        'label': get_value(5)}
                except:
                    pass

    weib_docidx = create_weib_document_index(doc_idx)
    return weib_docidx


def get_docidx_fromfile(file_name, label):
    doc_idx = {}
    if os.path.exists(file_name):
        with open(file_name, 'rb') as lexicon_file:
            for line in lexicon_file:
                try:
                    line = line.strip()
                    doc_idx[line] = {'text': line, 'label': label}
                except:
                    print line
    return doc_idx

lexicon_docidx = {}
pos_file = os.path.join('resources', 'positive-words.txt')
neg_file = os.path.join('resources', 'negative-words.txt')
pdoc_idx = get_docidx_fromfile(pos_file, 'positive')
ndoc_idx = get_docidx_fromfile(neg_file, 'negative')
weib_docidx = get_weib()
doc_list = [pdoc_idx, ndoc_idx, weib_docidx]
for docidx in doc_list:
    lexicon_docidx.update(docidx)
