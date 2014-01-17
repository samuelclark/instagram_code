import cPickle
import os
import datetime
import time
from instagram.client import InstagramAPI
CLIENT_SECRET = '04e72f5e767147bbb4da6168c3495270'
CLIENT_ID = 'e8bddc5ef0e5460cbc5c05a8945c282f'
REDIRECT_URL = 'http://127.0.0.1:5000/login'
ACCESS_TOKEN = '194916491.e8bddc5.f6a363bb1db74f808cf0e55c6dca9e53'
USER_ID = '194916491'

class TagSearch:
	"""
		This class is a controller for the api searching for TagSearch
	"""
	def __init__(self,access_token,tag):
		assert isinstance(tag,str)
		self.api = InstagramAPI(access_token=ACCESS_TOKEN)
		self.api_calls = 0
		self.tag = tag
		self.created = datetime.datetime.now()
		self.save_path = self.get_save_path()
		self.saved_media = self.load_saved_media()
		self.num_runs = 0

	def get_save_path(self,save_dir='tag_pickles'):
		save_dir =os.path.join(save_dir,self.tag)
		date_str = "{0}_{1}.pkl".format(self.tag,self.created.strftime("%d-%m-%Y"))
		outfile = os.path.join(save_dir,date_str)
		if not os.path.exists(save_dir):
			os.mkdir(save_dir)
		return outfile

	def set_tag(self):
		self.saved_media = self.get_save_path()
		self.tag = tag
	def load_saved_media(self):
		if os.path.exists(self.save_path):
			with open(self.save_path,'rb') as save_file:
				saved_media = cPickle.load(save_file)
		else:
			saved_media = {}
		#print "{1} : saved_media = {0}\t time: {2} seconds".format(len(saved_media),self.save_path,(e-s).seconds)
		return saved_media
	def __str__(self):
		s = 'Tags: {0}\nAPICalls: {1}'.format(self.tag_list,self.api_calls)
		return s


	def tag_search(self,count=10):
		"""
			Search InstagramAPI tags for similar tags to self.tag
			(input)
				count = number of search results
		"""
		search_results = self.api.tag_search(self.tag,count=count)
		self.api_calls+=1
		return search_results

	def tag_recent_media(self,count=50):
		sresults = self.api.tag_recent_media(count=count,tag_name=self.tag)
		self.api_calls+=1
		print sresults[0]
		return sresults[0]

	def save_recent_media(self):
		num_duplicates = 0
		num_saved = 0
		for each in self.tag_recent_media():
			mid = each.id
			if mid in self.saved_media:
				num_duplicates+=1
			else:
				self.saved_media[mid] = each
				num_saved+=1

		print "Saving {0} to {1}\nduplicates={2}".format(num_saved,self.save_path,num_duplicates)
		with open(self.save_path,'wb') as save_file:
			cPickle.dump(self.saved_media,save_file)

	def run_search(self):
		
		self.save_path = self.get_save_path()
		self.saved_media = self.load_saved_media()
		print "searching for ({0})\tnum_runs={1}\nnum_saved={2}\tAPICalls={3}".format(self.tag,self.num_runs,len(self.saved_media),self.api_calls)
		self.save_recent_media()
		self.num_runs+=1






ts = TagSearch(access_token=ACCESS_TOKEN,tag='happy')
tags = ['happy','sad','good','bad','fun','bored','love','hate','awesome','sucks','cool','stupid','want','ugly','beautiful']
sleep_time = 2
while(True):
	for tag in tags:
		try:
			ts.tag = tag
			ts.run_search()

		except Exception as e:
			print e.message

		time.sleep(sleep_time)
		print "sleeping"
		for i in range(sleep_time):
			if i % 1 == 0:
				r = "-"*i + " : " + str((sleep_time-i))
				print r
			time.sleep(1)
		print



