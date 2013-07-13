import time
from pymongo import MongoClient


class Backend():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.main_database
        # Collection for usernames and logins
        self.users = self.db.users

    def _get_user_info(self, username):
        # Returns document corresponding to a particular user
        return self.users.find_one({'Username': username})

    def add_user(self, username, password):
        doc = {'Username': username,
               'Location': None,
               'Neighbors': []}
        self.users.insert(doc)
        return True

    def fb_login(self, username, password):
        # TODO: Check for facebook login here
        return True

    def update_location(self, username, location):
        self._get_user_info(username)['Location'] = location

    def get_location(self, username):
        return self._get_user_info(username)['Location']

    def add_neighbor(self, username, neighbor):
        # TODO: There's probably a better way of doing this
        return_val = False
        # 0 = Pending
        # 1 = Accept
        # 2 = Reject
        res_val = 0
        while True:
            # Check for response here
            if res_val == 1:
                print '{0} and {1} are now linked!'.format(username, neighbor)
                doc = self._get_user_info(username)
                doc['Neighbors'].append(neighbor)
                return_val = True
                break
            elif res_val == 2:
                print '{0} and {1} link not accepted =('.format(username, neighbor)
                break
            else:
                time.sleep(5)
                
        return return_val



def main():
    backend = Backend()

    test_login = 'Test'
    test_password = 'Password'

    backend.add_user(test_login, test_password)


    login_res = backend.fb_login(test_login, test_password)
    if not login_res:
        print 'Login not accepted =('
        return False

    # Location: (longitude, latitude, accuracy) 
        
if __name__ == '__main__':
    main()
