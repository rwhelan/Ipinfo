def application(environ, start_response):
    status = '200 OK'
    output = 'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

#    open('/tmp/output.out', 'w').write(str(environ))

    if 'x' in globals():
        x += 1
    else:
        x = 0

    return [str(x)]
