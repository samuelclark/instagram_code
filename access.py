import cPickle
import os
import datetime
from instagram.client import InstagramAPI

# credentials kept private

CLIENT_SECRET = ''
CLIENT_ID = ''
REDIRECT_URL = ''
ACCESS_TOKEN = ''
USER_ID = ''
# instantiate api
api = InstagramAPI(access_token=ACCESS_TOKEN)
recent_media, next = api.user_recent_media(user_id=USER_ID, count=25)


class User:

    """
            This class will query user relationships and create
            lists of user_ids that can then be queried for media
    """

    def __init__(self, api, user_id):
        """
                (input)
                        api = InstagramAPI
                        user_id = InstagramUserId --> defines root user
        """
        self.user_id = user_id
        self.current_user = api.user(self.user_id)
        self.followed_by = api.user_followed_by(self.user_id)[0]
        self.follows = api.user_follows(self.user_id)[0]


def recursive_user_follows_index(
        api, user_id, user_list, start=0, num_followers=20, target=100):
    """
            Recursively builds a list of user followers
            For each follower in user, for each follower in user.followers etc.
            Grows super fast
    """
    u = User(api, user_id)
    print "running with uid = {0}\tlist_size = {1}".format(user_id, len(set(user_list)))
    if len(set(user_list)) <= target:
        for user in u.follows[start:num_followers]:
            uid = user.id
            uobj = User(api, uid)
            if uid not in user_list:
                try:
                    user_list += uobj.follows
                    if len(set(user_list)) < target:
                        return (
                            user_list +
                            recursive_user_follows_index(
                                api,
                                uid,
                                user_list)
                        )
                except Exception as e:
                    print e.message
                    print "couldnt get followers for {0}".format(uid)

    return user_list


def save_user_list(user_id, user_list, dir_name='user_pickles'):
	"""
		Saves user_list to pickle files
	"""
    date_str = (datetime.datetime.now()).strftime("%d-%m-Y")
    file_str = '_'.join([date_str, user_id, '.pkl'])
    outfile = os.path.join(dir_name, file_str)
    with open(outfile, 'wb') as of:
        print "saving user_list with {0} users to {1}".format(len(user_list), outfile)
        cPickle.dump(user_list, of)

s_list = [0, 20, 40]
usr_list = recursive_user_follows_index(api, USER_ID, [], s_list[0])
save_user_list(USER_ID, usr_list)
