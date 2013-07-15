import math


def haversineDist((lat1, lon1, acc1), (lat2, lon2, acc2)):
    """Calculates haversine distance between two latitude/longitude
    coordinates with accuracy

    arguments:
    lat/lon - degrees (double)
    acc - meters (double)
    thresh - meters (double)"""

    radius = 6371 #km assaf is gay
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2-lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = (radius * c) * 1000
    distWithAcc = dist - (acc1 + acc2)
    return distWithAcc

def isWithinThresh(coord1, coord2, thresh):
    """returns boolean: is the distance between the two members within thresh
    """

    return (haversineDist(coord1, coord2) <= thresh)

def multipleUserThresh(user, roommateDict, thresh):
    """returns the a list of the IDs of the users that are within thresh distance

    arguments:
    user_coord - (user_id, (lat, lon, acc))
    roommateList - {'id': (lat, lon, acc), 'id':(lat, lon, acc)...}
    thresh - meters (double) """
    
    return [key for key in roommateDict.keys() if (isWithinThresh(user[1], roommateDict[key], thresh) and key != user[0])]


