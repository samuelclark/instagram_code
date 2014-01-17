import cPickle
import os

"""
	This file implements loading pickles from /dir/subname/pkl, currently being used for
	/tag_pickles/tag/date_mid.pkl
"""


def load_pickle(file_path):
    """
            Load pickle object from a path
            (input)
                    file_path
            (ouput)
                    pickle_object
    """
    if os.path.exists(file_path):
        try:
            with file(file_path, 'rb') as file_obj:
                pick = cPickle.load(file_obj)

        except Exception as e:
            print "failed loading {0}", file_path
            print e.message
            pick = None
        return pick

    else:
        print "{0}"
        return None


def get_files_from_path(fname, save_dir='tag_pickles'):
    """
            returns a list of files
    """
    path = os.path.join(save_dir, fname)
    if os.path.exists(path):
        return (
            [os.path.join(path, fname)
             for fname in os.listdir(path) if fname != 'DS_Store']
        )
    else:
        return None


def get_all_tagpickles(tag, count=False, save_dir='tag_pickles',):
    t_dict = {}
    flist = get_files_from_path(tag, save_dir=save_dir)
    if count:
        for each in flist[:count]:
            media_dict = load_pickle(each)
            if media_dict:
                print each, len(media_dict)
                t_dict.update(media_dict)
    else:  # count = len(flist) then ony  do code once
        for each in flist:
            media_dict = load_pickle(each)
            if media_dict:
                t_dict.update(media_dict)
            else:
                print "no media for ", each
    if count:
        print "tag = {0}\tcombined = {1} files \tmedia {2}".format(tag, count, len(t_dict))
    else:

        print "combined {0} files \tmedia {1}".format(len(flist), len(t_dict))
    return t_dict


if __name__ == '__main__':
    # example usage
    flist = get_files_from_path('bad', 'tweet_pickles')
    print flist
    p = load_pickle(flist[0])
