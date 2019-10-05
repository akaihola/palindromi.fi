import argparse
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class PalindromiHttpRequestHandler(SimpleHTTPRequestHandler):
    extensions_map = SimpleHTTPRequestHandler.extensions_map
    extensions_map[''] = 'text/html'


def test(directory: str, port: int = 8000, bind: str = '') -> None:
    """Serve given directory with an HTTP server on given address and port"""
    handler_class = partial(PalindromiHttpRequestHandler, directory=directory)
    with ThreadingHTTPServer((bind, port), handler_class) as httpd:
        host, port = httpd.socket.getsockname()
        print(f'Serving HTTP on {host} port {port} '
              f'(http://{host}:{port}/) ...')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                        '[default:current directory]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    args = parser.parse_args()
    test(args.directory, port=args.port, bind=args.bind)


if __name__ == '__main__':
    main()
