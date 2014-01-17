import os
import datetime
import cPickle
import time
from pattern.web import Twitter

class TweetSearch:
	"""
		This class is a controller for the api searching for TagTweet
	"""
	def __init__(self,tag):
		self.api_calls = 0
		self.tag = tag
		self.created = datetime.datetime.now()
		self.save_path = self.get_save_path()
		self.saved_media = self.load_saved_media()
		self.num_runs = 0

	def get_save_path(self,save_dir='tweet_pickles'):
		save_dir =os.path.join(save_dir,self.tag)
		date_str = "{0}_{1}.pkl".format(self.tag,self.created.strftime("%d-%m-%Y"))
		outfile = os.path.join(save_dir,date_str)
		if not os.path.exists(save_dir):
			os.mkdir(save_dir)
		return outfile

	def load_saved_media(self):
		s = datetime.datetime.now()
		if os.path.exists(self.save_path):
			with open(self.save_path,'rb') as save_file:
				saved_media = cPickle.load(save_file)
		else:
			saved_media = {}
		e = datetime.datetime.now()
		print "{1} : saved_media = {0}\t time: {2} seconds".format(len(saved_media),self.save_path,(e-s).seconds)
		return saved_media
	def __str__(self):
		s = 'Tag: {0}\nAPICalls: {1}'.format(self.tag,self.api_calls)
		return s


	def save_recent_media(self):
		num_duplicates = 0
		num_saved = 0
		last_id = None
		try:
			results = Twitter().search(self.tag,start=last_id,count=25)
		except Exception as e:
			print e
			results = []

		for each in results:
			
			mid = each.id
			each.text = each.text.encode("ascii","ignore")
			each.author = each.author.encode("ascii","ignore")
			if mid in self.saved_media:
				num_duplicates+=1
			else:
				self.saved_media[mid] = dict(each)
				num_saved+=1
			last_id = each.id
		if self.saved_media:
			print "Saving {0} to {1}\nduplicates={2}".format(num_saved,self.save_path,num_duplicates)

			with open(self.save_path,'wb') as save_file:
				try:
					save_file.write(cPickle.dumps(self.saved_media))
				except Exception as e:
					print e


	def run_search(self):
		
		self.save_path = self.get_save_path()
		self.saved_media = self.load_saved_media()
		print "searching for ({0})\tnum_runs={1}\nnum_saved={2}\tAPICalls={3}".format(self.tag,self.num_runs,len(self.saved_media),self.api_calls)
		self.save_recent_media()
		self.num_runs+=1


start ='happy'
ts = TweetSearch(tag=start)
tags = ['happy','sad','good','bad','fun','bored','love','hate','awesome','sucks','cool','stupid','want','ugly','beautiful']
sleep_time = 10
while(True):
	for tag in tags:
		#try:
		ts.tag = tag
		ts.run_search()

		#except Exception as e:
		#	print e.message

		time.sleep(sleep_time)
		print "sleeping"
		for i in range(sleep_time):
			if i % 1 == 0:
				r = "-"*i + " : " + str((sleep_time-i))
				print r
			time.sleep(1)
		print


	


