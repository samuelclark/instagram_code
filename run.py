from gold_standard import didx
import sys
import classifier  
# from weib_sentiment import lexicon_docidx
# tags = ['sad','happy']



########################################################################




#bored_docs = create_tag_docs('bored')
#fun_docs = create_tag_docs('fun')
"""
num=5
for count in range(1,num):
	pnc = create_posneg_classifier(count=count)
	pnc.nb_train()
	r = pnc.nb_test(gold_standard=didx.values())
	print count,'\t',r


print "\n" * 3
for count in range(1,num):
	tlc = create_taglist_classifier(all_tags,count=count)
	tlc.nb_train()
	r = tlc.nb_test()
	print count,"\t",r
"""


try:
	source = sys.argv[1]
	classifier_type = sys.argv[2]
	count = int(sys.argv[3])
	max_docs = int(sys.argv[4])
	simple = sys.argv[5]
except:
	source = 'instagram'
	classifier_type = 'posneg'
	count = None
	max_docs = None
	simple = False
	print "usage = python run.py <source> <classifier_type> <num files to pull from> <num docs per file>"
	print "defaulting to {0}\t{1}\t{2}".format(source,classifier_type,count)

if classifier_type == 'all':
	pol_class = classifier.create_taglist_classifier(count=count,mode=source)

elif classifier_type =='posneg':
	if simple == 'True':
		pos_list = ['happy']
		neg_list = ['sad']
		pol_class = classifier.create_posneg_classifier(max_docs=max_docs,count=count,mode=source,pos_list=pos_list,neg_list=neg_list)
	else:
		pol_class = classifier.create_posneg_classifier(max_docs=max_docs,count=count,mode=source)

pol_class.nb_train()
r = pol_class.nb_test()
print pol_class
print r
classifier.classify_by_user(pol_class)