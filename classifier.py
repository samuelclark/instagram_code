import corpus
import nbclassifier
import os
import cPickle
import datetime
def classify_by_user(nb_classifier,count=10):
	"""
		Lets the user input phrases and get the result from nb_classifier
	"""

	num = 0
	results = {}
	answers = {"0":"neutral","1":"positive","2":"negative"}
	ckey = dict([(b,a) for a,b in answers.items()])
	out_f = "{0}_scan.pkl".format(datetime.datetime.now().strftime("%Y_%m_%d_%M_%s"))
	save_file = os.path.join("scans",out_f)
	while (num<count):
		phrase = raw_input("* enter a phrase:\n")
		class_result = nb_classifier.classify_document(phrase)
		print "\nphrase: {0}\nclass: {1}\n".format(phrase,class_result)
		correct = raw_input("correct: [Y/n]:")
		print unicode(correct)
		if correct == "q":
			with open(save_file,'wb') as pkl_file:
				cPickle.dump(results,pkl_file)
			break
		if correct == '\n' or not correct:
			print "correct"
			correct = 'Y'
			response = ckey.get(class_result,"neutral")

		elif correct =='n':
			response = raw_input("0(neut)\n1(pos)\n2(neg)")
			while response not in ["0","1","2"]:
				response = raw_input("--invalid 1(neutral)\n0(pos)\n2(neg)")
		else:
			continue

		results[phrase] = results.get(phrase,[]).append(answers[response])

		print "num scanned = {0}".format(len(results))

	with open(save_file,'wb') as pkl_file:
		cPickle.dump(results,pkl_file)






def create_classifier(corpus):
	nbclass_obj = nbclassifier.NBClassifier(corpus=corpus)
	return nbclass_obj

#neg_list=['sad','bad','hate','bored','ugly']
#pos_list=['happy','good','love','fun','beautiful']
def create_posneg_classifier(pos_list=['happy','good','love'],neg_list=['sad','bad','hate'],count=None,mode='instagram',max_docs=None):
	print "creating posneg classifier\t{0}\t{1}".format(pos_list,neg_list)
	posneg_corp = corpus.create_posneg_corpus(pos_list,neg_list,count,mode=mode,max_docs=max_docs)
	posneg_classifier = create_classifier(posneg_corp)
	return posneg_classifier

def create_taglist_classifier(max_docs,count=None,mode='instagram'):
	if mode =='instagram':
		tag_file_list= os.listdir('tag_pickles')
	elif mode =='twitter':
		tag_file_list = os.listdir('tweet_pickles')

	taglist_corp = corpus.create_taglist_corpus(tag_file_list, count,mode=mode)
	taglist_classifier = create_classifier(taglist_corp)
	return taglist_classifier

def test_accuracy_by_size(count):
	for idx in range(1,count):
		posneg_classifier= create_posneg_classifier(count=idx)
		acc_results = posneg_classifier.run()
		print "idx\t",acc_results


"""

#doc_idx = create_doc_idx(tag_list)
lexicon_corp = create_corpus(lexicon_docidx)
lexicon_classifier = create_classifier(lexicon_corp)
lresults = lexicon_classifier.run()
print lresults
classify_by_user(lexicon_classifier)"""