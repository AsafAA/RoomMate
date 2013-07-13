import time
from pymongo import MongoClient
from flask import Flask, request
from haversine import multipleUserThresh
app = Flask(__name__)

AEPI = (37.867062, -122.251914, 0)
TOPDOG = (37.868315, -122.257472, 0)
CHANNING = (37.867551, -122.254256, 3.2)
HASTE = (37.866611, -122.25409, 4.3)

# THRESHES must be in ASCENDING order
THRESHES = [250, 500, 1000] # meters
WAIT = 1 # seconds


def encode_group(group):
    return {'_type': 'Group',
            'group_id': group.group_id,
            'phone_name_map': group.phone_name_map,
            'phone_loc_map': group.phone_loc_map,
            'phone_dnd_map': group.phone_dnd_map}


def decode_group(doc):
    assert doc['_type'] == 'Group'
    return Group(doc['group_id'],
                 doc['phone_name_map'],
                 doc['phone_loc_map'],
                 doc['phone_dnd_map'])


class Group():
    def __init__(self, group_id, phone_name_map, phone_loc_map, phone_dnd_map):
        self.group_id = group_id
        self.phone_name_map = phone_name_map
        self.phone_loc_map = phone_loc_map
        self.phone_dnd_map = phone_dnd_map


class Backend():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.main_database
        # Collection for usernames and logins
        self.groups = self.db.groups
        self.sync_data = self.db.sync_data
        users_group_map = {'ID': 'UGM', 'Data': dict()}
        broadcast_times = {'ID': 'BT', 'Data': dict()}
        min_threshes = {'ID': 'MT', 'Data': dict()}
        self.sync_data.insert(users_group_map)
        self.sync_data.insert(broadcast_times)
        self.sync_data.insert(min_threshes)

    def _get_group(self, group_id):
        return decode_group(self.groups.find_one({'ID': group_id})['Data'])
    
    def _get_sync(self, data_id):
        return self.sync_data.find_one({'ID': data_id})['Data']

    def _update_group(self, group_id, data):
        self.groups.update({'ID': group_id}, {'ID': group_id, 'Data': encode_group(data)})

    def _update_sync(self, dict_id, data):
        self.sync_data.update({'ID': dict_id}, {'ID': dict_id, 'Data': data})

    def _get_loc_map(self, group_id, my_id):
        filtered_groups = {}
        group = self._get_group(group_id)
        for phone in group.phone_loc_map.keys():
            if phone != my_id and group.phone_loc_map[phone] is not None and group.phone_dnd_map[phone] == 1:
                filtered_groups[phone] = group.phone_loc_map[phone]
        return filtered_groups

    def _remove_user(self, group_id, phone_id):
        group = self._get_group(group_id)
        group.phone_name_map.pop(phone_id, None)
        group.phone_loc_map.pop(phone_id, None)
        self._update_group(group_id, group)
        users_group_map = self._get_sync('UGM')
        users_group_map.pop(phone_id, None)
        self._update_sync('UGM', users_group_map)

    def add_user(self, group_id, phone_id, phone_name, toggle_state):
        users_group_map = self._get_sync('UGM')
        if phone_id in users_group_map.keys():
            self._remove_user(users_group_map[phone_id], phone_id)
        users_group_map[phone_id] = group_id
        self._update_sync('UGM', users_group_map)
       
        try:
            data = self._get_group(group_id)
        except:
            data = Group(group_id, dict(), dict(), dict())
            doc = {'ID': group_id,
                   'Data': encode_group(data)}
            self.groups.insert(doc)
       
        data.phone_name_map[phone_id] = phone_name
        data.phone_loc_map[phone_id] = None
        data.phone_dnd_map[phone_id] = toggle_state
        self._update_group(group_id, data)
        # Ensures a user can only be part of one group
        return True

    def update_location(self, group_id, phone_id, location):
        group = self._get_group(group_id)
        my_name = group.phone_name_map[phone_id]
        print '============UPDATING {0} LOCATION============='.format(my_name)
        group.phone_loc_map[phone_id] = location
        self._update_group(group_id, group)
        filtered_groups = self._get_loc_map(group_id, phone_id)

        # Reset phone pairs that meet the time threshold
        broadcast_times = self._get_sync('BT')
        min_threshes = self._get_sync('MT')
        for party_pair in broadcast_times.keys():
            time_diff = time.time() - broadcast_times[party_pair]
            if time_diff > WAIT:
                broadcast_times.pop(party_pair, None)
                try:
                    min_threshes.pop(party_pair, None)
                except:
                    pass

        # Go through thresholds, should be smallest to largest
        for thresh in THRESHES:
            offending_ids = multipleUserThresh((phone_id, group.phone_loc_map[phone_id]), filtered_groups, thresh)
            offending_names = [group.phone_name_map[phone_id_bad] for phone_id_bad in offending_ids]
            if offending_ids:
                for offending_id in offending_ids:
                    name = group.phone_name_map[offending_id]
                    party_pair = [offending_id, phone_id]
                    party_pair.sort()
                    party_pair = party_pair[0] + '_' + party_pair[1]
                    # Valid time pairs should have been reset, ensure if we see a smaller thresh we notify
                    if party_pair not in broadcast_times.keys() or thresh < min_threshes[party_pair]:
                            print 'Notification to {0}: {1} is within {2} meters!'.format(name, my_name, thresh)
                            print 'Notification to {0}: {1} is within {2} meters!'.format(my_name, name, thresh)
                            broadcast_times[party_pair] = time.time()
                            min_threshes[party_pair] = thresh

        self._update_sync('BT', broadcast_times)
        self._update_sync('MT', min_threshes)
        return offending_names


def test():
    backend = Backend()

    phone_id_1 = 'Alpha'
    phone_name_1 = 'Phone 1'
    group_id_1 = 'Group'

    phone_id_2 = 'Beta'
    phone_name_2 = 'Phone 2'
    group_id_2 = 'Group'

    phone_id_3 = 'Charlie'
    phone_name_3 = 'Phone 3'
    group_id_3 = 'Group'
    
    # Add three test users
    backend.add_user(group_id_1, phone_id_1, phone_name_1, True)
    backend.add_user(group_id_2, phone_id_2, phone_name_2, True)
    backend.add_user(group_id_3, phone_id_3, phone_name_3, True)
    
    # Test location updates
    # First update shouldn't yelt any notices
    backend.update_location(group_id_1, phone_id_1, AEPI)
    # Second update should notify pairs (1, 2)
    backend.update_location(group_id_2, phone_id_2, TOPDOG)
    # Third update should notify pairs (1, 3), (2, 3)
    backend.update_location(group_id_3, phone_id_3, HASTE)
    # Fourth update is fast and repetitive, should be no update
    backend.update_location(group_id_3, phone_id_3, HASTE)

    # Test location update to shorter distance
    # Fifth update should notify pairs (1, 2) (1, 3) as distance is
    # shorter
    backend.update_location(group_id_2, phone_id_2, AEPI)
    
    time_to_wait = 2
    print '================================================'
    print 'WAITING {0} SECONDS'.format(time_to_wait)
    print '================================================'
    time.sleep(time_to_wait)

    # Test removal of someone from the group
    backend.add_user('Wrong', phone_id_1, phone_name_1, True)
    backend.add_user('Wrong', phone_id_3, phone_name_3, True)
    # Should be no notice since phone 1 is not in a group and phone 3
    # in a different group
    backend.update_location(group_id_2, phone_id_2, AEPI)

    time_to_wait = 2
    print '================================================'
    print 'WAITING {0} SECONDS'.format(time_to_wait)
    print '================================================'
    time.sleep(time_to_wait)
    
    # Test updates after waiting past WAIT
    backend.add_user(group_id_1, phone_id_1, phone_name_1, True)
    #print backend._get_group(group_id_1).phone_loc_map
    backend.add_user(group_id_3, phone_id_3, phone_name_3, True)
    # First update should notify pairs (1, 2) since 2 already there
    backend.update_location(group_id_1, phone_id_1, AEPI)
    # Second update should not notify (no change)
    backend.update_location(group_id_2, phone_id_2, TOPDOG)
    # Third update should notify pairs (1, 3), (2, 3)
    backend.update_location(group_id_3, phone_id_3, HASTE)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        group_id = request.form['group_id']
        phone_id = request.form['phone_id']
        phone_name = request.form['phone_name']
        dnd = int(request.form['dnd'])
        backend.add_user(group_id, phone_id, phone_name, dnd)
        return "Done"

@app.route('/update_location', methods=['POST'])
def update_location():
    if request.method == 'POST':
        group_id = request.form['group_id']
        phone_id = request.form['phone_id']
        lon = float(request.form['lon'])
        lat = float(request.form['lat'])
        acc = float(request.form['acc'])
        location = (lon, lat, acc)
        backend.update_location(group_id, phone_id, location)
        return "Done"

backend = Backend()
if __name__ == '__main__':
    #app.run()
    test()
