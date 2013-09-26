
import sqlite3

from Utils import ipv4ToInit

database = sqlite3.connect('data.db')
database.text_factory = lambda x: x.decode('cp1252')
cursor = database.cursor()

def _getLocId(ip):
    int_ip = ipv4ToInit(ip)
    cursor.execute('SELECT locId FROM Blocks WHERE startIpNum <= ? and endIpNum >= ?', (int_ip, int_ip))
    result = cursor.fetchall()

    if result:
        return result[0][0]

    return 0


def _getLocation(locid):
    cursor.execute('SELECT * FROM Location WHERE locId == ?', (locid,))
    result = cursor.fetchall()

    if result:
        return result[0]

    return (locid, u'', u'', u'', u'', 0, 0, u'', u'')


def getAS(ip):
    int_ip = ipv4ToInit(ip)
    cursor.execute('SELECT Org FROM ASN WHERE startIpNum <= ? and endIpNum >= ?', (int_ip, int_ip))
    result = cursor.fetchall()

    if result:
        result = result[0][0]
        assert result.startswith('AS')

        return result

    return u''


def getLocation(ip):
    locid = _getLocId(ip)
    return _getLocation(locid)
