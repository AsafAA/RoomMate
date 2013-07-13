from pymongo import MongoClient
from haversine import multipleUserThresh

AEPI = (37.867062, -122.251914, 0)
TOPDOG = (37.868315, -122.257472, 0)
CHANNING = (37.867551, -122.254256, 3.2)
HASTE = (37.866611, -122.25409, 4.3)
THRESH = 1000

def encode_user(user):
    return {'_type': 'User',
            'fb_token': user.fb_token,
            'location': user.location,
            'neighbors': user.neighbors}


def decode_user(doc):
    assert doc['_type'] == 'User'
    return User(doc['fb_token'],
                doc['location'],
                doc['neighbors'])


class User():
    def __init__(self, fb_token, location, neighbors):
        self.fb_token = fb_token
        self.location = location
        self.neighbors = neighbors


class Backend():
    # _id is the public facebook id
    # _token is the private facebook token for interfacing
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.main_database
        # Collection for usernames and logins
        # Clean for dev purposes
        try:
            self.db.users.drop()
        except:
            pass
        self.users = self.db.users

    def _get_user(self, fb_id):
        return decode_user(self.users.find_one({'ID': fb_id})['Data'])

    def _update_user(self, fb_id, data):
        self.users.update({'ID': fb_id}, {'ID': fb_id, 'Data': encode_user(data)})

    def _get_neighbor_locs(self, my_id):
        loc_dict = {}
        me = self._get_user(my_id)
        for n in me.neighbors:
            friend = self._get_user(n)
            if friend.location:
                loc_dict[n] = tuple(friend.location)
        return loc_dict

    def add_user(self, fb_id, fb_token):
        data = User(fb_token, None, [])
        doc = {'ID': fb_id,
               'Data': encode_user(data)}
        self.users.insert(doc)
        return True

    def update_location(self, fb_id, location):
        user = self._get_user(fb_id)
        user.location = location
        self._update_user(fb_id, user)
        neighbor_locs = self._get_neighbor_locs(fb_id)
        return multipleUserThresh(self._get_user(fb_id).location, neighbor_locs, THRESH)

    def request_link(self, my_id, friend_id):
        # TODO Send link notification here
        return

    def confirm_link(self, my_id, friend_id):
        # TODO Send confirm notification here
        me = self._get_user(my_id)
        friend = self._get_user(friend_id)
        me.neighbors.append(friend_id)
        friend.neighbors.append(my_id)
        self._update_user(my_id, me)
        self._update_user(friend_id, friend)

       

def main():
    backend = Backend()

    id_1 = 'User 1'
    token_1 = 'Token 1'

    id_2 = 'User 2'
    token_2 = 'Token 2'

    id_3 = 'User 3'
    token_3 = 'Token 3'

    backend.add_user(id_1, token_1)
    backend.add_user(id_2, token_2)
    backend.add_user(id_3, token_3)

    backend.confirm_link(id_1, id_2)
    backend.confirm_link(id_1, id_3)

    print backend.update_location(id_1, AEPI)
    print backend.update_location(id_2, TOPDOG)
    print backend.update_location(id_3, HASTE)



if __name__ == '__main__':
    main()
