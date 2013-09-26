
import os, sys, json

# Only real hackers hardcode paths...
# TODO
sys.path.insert(0, '/var/wsgi')
os.chdir('/var/wsgi')

from Model import OrgRecord 

def application(environ, start_response):
    status = '200 OK'

    # We don't need no stinkin input validation-
    # 500 errors are for winners!
    # TODO

    ipaddr = str(environ['PATH_INFO'].split('/')[1])

    org = OrgRecord(ipaddr)

    output = json.dumps(dict(org), encoding = 'cp1252', indent = 4)

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
