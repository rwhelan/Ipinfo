
import sqlite3

from Utils import ipv4ToInit

database = sqlite3.connect('data.db')
cursor = database.cursor()

def _getLocId(ip):
    cursor.execute('SELECT locId FROM Blocks WHERE startIpNum <= {iip} and endIpNum >= {iip}'.format(iip=ipv4ToInit(ip)))
    result = cursor.fetchall()

    if result:
        return result[0][0]

    return 0


def _getLocation(locid):
    cursor.execute('SELECT * FROM Location WHERE locId == %s' % locid)
    result = cursor.fetchall()

    if result:
        return result[0]

    return (locid, u'', u'', u'', u'', 0, 0, u'', u'')


def getAS(ip):
    cursor.execute('SELECT Org FROM ASN WHERE startIpNum <= {iip} and endIpNum >= {iip}'.format(iip=ipv4ToInit(ip)))
    result = cursor.fetchall()

    if result:
        result = result[0][0]
        assert result.startswith('AS')

        return result

    return u''


def getLocation(ip):
    locid = _getLocId(ip)
    return _getLocation(locid)
