import os

from pattern.vector import Corpus,Document,PORTER

def get_gold_docidx(file_name):
	doc_index = {}
	with open(file_name,'rb') as gold_file:

		for line in gold_file:
			line = line.split('\t')
			did = line[1]
			tag = line[4]
			if tag == 'positive' or tag == 'negative':
				text = line[5]
				doc_index[did] = Document(text,type=tag,stemmer=PORTER)
	return doc_index


gs_file = 'twitter-gold.tsv'
file_name = os.path.join('resources',gs_file)

didx = get_gold_docidx(file_name)