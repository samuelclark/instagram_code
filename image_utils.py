import requests
import os
import random
import loadpickle

"""
 This file handles the media objects images, functions
 include saving, etc
 """

def save_media_image(media,tag,quality='standard_resolution',save_dir='image_save'):
	ext = ".png"
	img = media.images[quality]
	img_req = requests.get(img.url,stream=True)
	img_str = "{0}_".format(tag)+''.join([media.id,ext])
	if not os.path.exists(os.path.join(save_dir,tag)):
		os.mkdir(os.path.join(save_dir,tag))
	img_save_str = os.path.join(save_dir,tag,img_str)
	if img_req.status_code == 200:
		with open(img_save_str,'wb') as save_file:
			for chunk in img_req.iter_content(1024):
				save_file.write(chunk)
		print "saved {0}".format(img_save_str)
	else:
		print "invalid request for media = {0}".format(media.id)

def gen_random_images(tags):

	for i in range(50):
		tag = random.choice(tags)
		print tag
		flist = loadpickle.get_files_from_path(tag)
		p = loadpickle.load_pickle(flist[0])
		med = random.choice(p.values())
		save_media_image(med,tag)


