from instagram.client import InstagramAPI
from pattern.vector import count as vec_count
CLIENT_SECRET = '04e72f5e767147bbb4da6168c3495270'
CLIENT_ID = 'e8bddc5ef0e5460cbc5c05a8945c282f'
REDIRECT_URL = 'http://127.0.0.1:5000/login'
ACCESS_TOKEN = '194916491.e8bddc5.f6a363bb1db74f808cf0e55c6dca9e53'
USER_ID = '194916491'
api = InstagramAPI(access_token=ACCESS_TOKEN)

def tag_recent_media(tag,count=50):

		sresults = api.tag_recent_media(count=count,tag_name=tag)
		print sresults[0]
		return sresults[0]

def build_tag_index(recent_media):
	"""
		Transforms recent_media into dictionaries of tags and edges
		(input) [list of media]
		(return) {'nodes':{}, 'edges':{}}
	"""

	nodes = {}
	edges = {}

	for media in recent_media[:10]:
		try:
			tags = media.tags
		except:
			tags = []
		for tag in tags:
			tname = tag.name.encode('ascii','ignore')

			nodes[tname] = nodes.get(tname,0) +1
			tags.remove(tag)
			tnames = [t.name.encode('ascii','ignore') for t in tags]
			if tname in edges:
				edges[tname] += tnames
			else:
				print "{1} new edges for {0}".format(tname,len(tnames))
				edges[tag.name] = tnames

	for name,tags in edges.items():
		edge_freq = vec_count(tags)
		edges[name] = edge_freq

	return {'nodes':nodes, 'edges':edges}


tag = 'happy'
rm = tag_recent_media(tag)

index = build_tag_index(rm)
nodes = index['nodes']
edges = index['edges']
