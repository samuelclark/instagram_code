import random
import datetime
from pattern.vector import Model,NB,Document,PORTER,TF,kfoldcv
class NBClassifier:
    """
        This class interfaces a pattern corpus with a pattern.vector nb classifier

    """
    def __init__(self,corpus,**kargs):
        """
            Initializes the NBClassifier class with a corpus and a NB instance
            (input): corpus = a corpus of pattern Documents constructed from Grams
        """
        self.corpus = corpus
        self.documents = self.corpus.documents
        self.model = Model(documents=self.documents,weight='TF-IDF')
        #self.documents.words = self.documents.keywords
        self.split_idx = len(self)/4
        self.nb = NB()


    def __len__(self):
        return len(self.documents)


    def classify_document(self,document):
        """
            classify document with nb instance
            (input):
                 document = Document instance with same format as classifier train set
            (output): classification result
        """
        return self.nb.classify(Document(document,stemmer=PORTER),discrete=True)

    def nb_train(self):
        """
            This function trains the classifier with (3/4) of the documents
            (input): None
            (outpu): trains self.nb
        """
        train_start = datetime.datetime.now()
        print "training with {0} docs".format(len(self)-self.split_idx)
        documents = self.documents[:-self.split_idx]
        random.shuffle(documents)
        [self.nb.train(doc) for doc in documents]
        train_end = datetime.datetime.now()
        print "training {0} docs took {1} seconds".format(len(documents),(train_end-train_start).seconds)


    def nb_test(self,gold_standard=None):
        """
            Evaluates the classifier on (1/4) of the documents
            (input): None
            (output): accuracy, precision, recall, f1
        """
        if not gold_standard:
            test_docs = self.documents[-self.split_idx:]
            conf_matrix = self.nb.confusion_matrix(test_docs)
            print conf_matrix.table

            return self.nb.test(test_docs)
        else:
            return self.nb.test(gold_standard)

    def get_documentlabel_distribution(self):
        """
            Gets the label distribution of the document set passed into
            self.nb classifier
            (input): None
            (output):
                 distribution = dictionary representation of the label:frequency distribution
                 rankdistribution = a ranked list of label keys by frequency
        """

        distribution = self.nb.distribution
        rankdistribution = sorted(distribution,key = lambda x: distribution[x],reverse=True)
        for each,key in enumerate(rankdistribution[:10]):
            print "{0}:\t{1} ({2})".format(each,key,distribution[key])

        return distribution,rankdistribution

    def run(self):
        """
            executes training / testing of classifier
        """
        print "training and testing {0} total documents...".format(len(self))
        self.nb_train()
        print "testing"
        result = self.nb_test()
        print "finalizing"
        self.nb.finalize()
        return result

