import time
from pymongo import MongoClient
from haversine import multipleUserThresh

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
            'phone_loc_map': group.phone_loc_map}


def decode_group(doc):
    assert doc['_type'] == 'Group'
    return Group(doc['group_id'],
                 doc['phone_name_map'],
                 doc['phone_loc_map'])


class Group():
    def __init__(self, group_id, phone_name_map, phone_loc_map):
        self.group_id = group_id
        self.phone_name_map = phone_name_map
        self.phone_loc_map = phone_loc_map


class Backend():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.main_database
        # Collection for usernames and logins
        # Clean for dev purposes
        try:
            self.db.groups.drop()
        except:
            pass
        self.groups = self.db.groups
        self.users_group_map = dict()
        self.broadcast_times = dict()
        self.min_threshes = dict()

    def _get_group(self, group_id):
        return decode_group(self.groups.find_one({'ID': group_id})['Data'])

    def _update_group(self, group_id, data):
        self.groups.update({'ID': group_id}, {'ID': group_id, 'Data': encode_group(data)})

    def _get_loc_map(self, group_id, my_id):
        filtered_groups = {}
        group = self._get_group(group_id)
        for phone in group.phone_loc_map.keys():
            if phone != my_id and group.phone_loc_map[phone] is not None:
                filtered_groups[phone] = group.phone_loc_map[phone]
        return filtered_groups

    def add_user(self, group_id, phone_id, phone_name, debug=False):
        try:
            data = self._get_group(group_id)
        except:
            data = Group(group_id, dict(), dict())
            doc = {'ID': group_id,
                   'Data': encode_group(data)}
            self.groups.insert(doc)
        
        data.phone_name_map[phone_id] = phone_name
        data.phone_loc_map[phone_id] = None
        self._update_group(group_id, data)
        # Ensures a user can only be part of one group
        if phone_id in self.users_group_map.keys():
            self.remove_user(self.users_group_map[phone_id], phone_id)
        self.users_group_map[phone_id] = group_id
        return True

    def remove_user(self, group_id, phone_id):
        group = self._get_group(group_id)
        group.phone_name_map.pop(phone_id, None)
        group.phone_loc_map.pop(phone_id, None)
        self._update_group(group_id, group)
        self.users_group_map.pop(phone_id, None)

    def update_location(self, group_id, phone_id, location, debug=False):
        group = self._get_group(group_id)
        my_name = group.phone_name_map[phone_id]
        print '============UPDATING {0} LOCATION============='.format(my_name)
        group.phone_loc_map[phone_id] = location
        self._update_group(group_id, group)
        filtered_groups = self._get_loc_map(group_id, phone_id)

        # Reset phone pairs that meet the time threshold
        for party_pair in self.broadcast_times.keys():
            time_diff = time.time() - self.broadcast_times[party_pair]
            if time_diff > WAIT:
                self.broadcast_times.pop(party_pair, None)
                try:
                    self.min_threshes.pop(party_pair, None)
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
                    party_pair = tuple(party_pair)
                    # Valid time pairs should have been reset, ensure if we see a smaller thresh we notify
                    if party_pair not in self.broadcast_times.keys() or thresh < self.min_threshes[party_pair]:
                            print 'Notification to {0}: {1} is within {2} meters!'.format(name, my_name, thresh)
                            print 'Notification to {0}: {1} is within {2} meters!'.format(my_name, name, thresh)
                            self.broadcast_times[party_pair] = time.time()
                            self.min_threshes[party_pair] = thresh

        return offending_names


def main():
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
    backend.add_user(group_id_1, phone_id_1, phone_name_1)
    backend.add_user(group_id_2, phone_id_2, phone_name_2)
    backend.add_user(group_id_3, phone_id_3, phone_name_3)
    
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
    # Fifth update should notify pairs (1, 2) as distance is
    # shorter
    backend.update_location(group_id_2, phone_id_2, AEPI)
    
    time_to_wait = 2
    print '================================================'
    print 'WAITING {0} SECONDS'.format(time_to_wait)
    print '================================================'
    time.sleep(time_to_wait)

    # Test removal of someone from the group
    backend.remove_user(group_id_1, phone_id_1)
    backend.add_user('Wrong', phone_id_3, phone_name_3, debug=True)
    # Should be no notice since phone 1 is not in a group and phone 3
    # in a different group
    backend.update_location(group_id_2, phone_id_2, AEPI)

    time_to_wait = 2
    print '================================================'
    print 'WAITING {0} SECONDS'.format(time_to_wait)
    print '================================================'
    time.sleep(time_to_wait)
    
    # Test updates after waiting past WAIT
    backend.add_user(group_id_1, phone_id_1, phone_name_1)
    #print backend._get_group(group_id_1).phone_loc_map
    backend.add_user(group_id_3, phone_id_3, phone_name_3)
    # First update should notify pairs (1, 2) since 2 already there
    backend.update_location(group_id_1, phone_id_1, AEPI)
    # Second update should not notify (no change)
    backend.update_location(group_id_2, phone_id_2, TOPDOG)
    # Third update should notify pairs (1, 3), (2, 3)
    backend.update_location(group_id_3, phone_id_3, HASTE)

if __name__ == '__main__':
    main()
