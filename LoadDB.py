import urllib2
import sqlite3
import zipfile
import csv
import re

import cStringIO as StringIO

update_url = 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.zip'
as_update_url = 'http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum2.zip'


def DBInit():
    try:
        cursor.execute('DELETE FROM Blocks')
    except sqlite3.OperationalError, E:
        if E.message.startswith('no such table'):
            cursor.execute('CREATE TABLE Blocks (startIpNum int, endIpNum int, locId int)')
        else:
            raise


    try:
        cursor.execute('DELETE FROM Location')
    except sqlite3.OperationalError, E:
        if E.message.startswith('no such table'):
            cursor.execute('CREATE TABLE Location (locId int, country char, region char, city char, postalCode char, latitude int, longitude int, metroCode int, areaCode int)')
        else:
            raise

    try:
        cursor.execute('DELETE FROM ASN')
    except sqlite3.OperationalError, E:
        if E.message.startswith('no such table'):
            cursor.execute('CREATE TABLE ASN (startIpNum int, endIpNum int, Org char)')
        else:
            raise


def fetchURL(url, filehandle):
    response = urllib2.urlopen(url)
    filehandle.write(response.read())


database = sqlite3.connect('data.db')
database.text_factory = lambda x: x.decode('cp1252')
cursor = database.cursor()
DBInit()

reBlockRow = re.compile('^"(\d*)","(\d*)","(\d*)"$')
reLocationRow = re.compile('^(\d*),"(.*?)","(.*?)","(.*?)","(.*?)",(.*?),(.*?),(\d*),(\d*)$')

tempfile = StringIO.StringIO()
fetchURL(update_url, tempfile)
zf = zipfile.ZipFile(tempfile, 'r')
for i in zf.namelist():
    if i.lower().find('blocks') != -1:
        blocks = {}
        tempf = StringIO.StringIO(zf.read(i))
        for row in tempf.readlines():
            result = reBlockRow.findall(row)
            if result:
                result = result[0]
                cursor.execute('INSERT INTO Blocks VALUES (?, ?, ?)', tuple(result))

    database.commit()

    if i.lower().find('location') != -1:
        blocks = {}
        tempf = StringIO.StringIO(zf.read(i))
        for row in tempf.readlines():
            result = reLocationRow.findall(row)
            if result:
                result = result[0]
                cursor.execute('INSERT INTO Location VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple(result))

    database.commit()

del tempfile

tempfile = StringIO.StringIO()
reBlockRow = re.compile('^(\d*),(\d*),"(.*?)"$')
fetchURL(as_update_url, tempfile)
zf = zipfile.ZipFile(tempfile, 'r')
for i in zf.namelist():
    if i.lower().find('asn') != -1:
        blocks = {}
        tempf = StringIO.StringIO(zf.read(i))
        for row in tempf.readlines():
            result = reBlockRow.findall(row)
            if result:
                result = result[0]
                cursor.execute('INSERT INTO ASN VALUES (?, ?, ?)', tuple(result))


database.commit()
