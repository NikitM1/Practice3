import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer, _get_best_family
def test(HandlerClass=SimpleHTTPRequestHandler,
         ServerClass=ThreadingHTTPServer,
         protocol="HTTP/1.0",port=8000,bind=None):

    ServerClass.address_family,addr=_get_best_family(bind,port)
    HandlerClass.protocol_version=protocol
    with ServerClass(addr, HandlerClass) as httpd:
        post,port=httpd.socket.getsockname()[:2]
        hostinfo=socket.gethostbyname(socket.gethostname())
        print(
                f'ServingHTTP on {hostinfo} port {port} '
                f'(http://{hostinfo}:{port}/) ...'
            )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nKeyboard interrupt recieved, existing.')
            exit(0)

if __name__=='__main__':
    import sys
    port=int(sys.args[1]) if len(sys.argv)>1 else 8000
    test(port=port)
