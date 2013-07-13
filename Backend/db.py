from pymongo import MongoClient
from sets import Set


def encode_user(user):
    return {'_type': 'User',
            'username': user.username,
            'fb_id': user.fb_id,
            'location': user.location,
            'neighbors': user.neighbors}


def decode_user(doc):
    assert doc['_type'] == 'User'
    return User(doc['username'],
                doc['fb_id'],
                doc['location'],
                doc['neighbors'])


class User():
    def __init__(self, fb_token, location, neighbors):
        self.fb_token = fb_token
        self.location = location
        self.neighbors = neighbors

    def update_location(self, location):
        self.location = location

class Backend():
    # _id is the public facebook id
    # _token is the private facebook token for interfacing
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.main_database
        # Collection for usernames and logins
        self.users = self.db.users

    def _get_user_info(self, fb_id):
        # Returns document corresponding to a particular user
        return self.users.find_one({'ID': fb_id})

    def add_user(self, fb_id, fb_token):
        data = User(fb_token, None, [])
        doc = {'ID': fb_id,
               'Data': encode_user(data)}
        self.users.insert(doc)
        return True

    def get_user(self, fb_id):
        return decode_user(self._get_user_info(fb_id)['Data'])

    def add_link(self, my_token, my_id, friend_id):
        device_token = 
        pay_load = #Kern
        fb_api.send_push_notification(thePayLoad=pay_load)

    def confirm_link(self, my_token, my_id, friend_id):
        # TODO Confirm notification here
        me = self.get_user(my_id)
        friend = self.get_user(friend_id)
        me.neighbors.append(friend)
        friend.neighbors.append(me)

def main():
    backend = Backend()

    test_login = 'Test'
    test_password = 'Password'

    backend.add_user(test_login, test_password)

    res_val = backend.add_user(test_login, test_password)
    if not res_val:
        print 'User add failed'
        return False

    # Location: (longitude, latitude, accuracy)
    user = backend.login(test_login, test_password)
    user.update_location((10, 10, 10))
    print user.location


if __name__ == '__main__':
    main()
