import argparse
import utils
from http.server import HTTPServer
from http_handler import HttpHandler
from version_maintainer import VersionMaintainer

def run():
    parser = argparse.ArgumentParser(
        description='Python service/cli tool for computing next version value')
    
    parser.add_argument(
        '--versions-dir',
        help=f'(Optional) Where should store versions info data. Default to {utils.format_text(".versions")}',
        default='.versions',
        required=False)

    subparsers = parser.add_subparsers(
        dest='mode',
        help='mode',
        required=True)
    
    cli_parser = subparsers.add_parser('cli')
    cli_parser.add_argument('-u', '--update', action='store_true')
    cli_parser.add_argument('job')
    
    listen_parser = subparsers.add_parser('listen')
    listen_parser.add_argument(
        'address',
        help=f'On which address and port should listen. Eg. {utils.format_text("--listen :8080")}, {utils.format_text("--listen localhost:8080")}',
        default=False)

    args = parser.parse_args() 

    version_maintainer = VersionMaintainer(args.versions_dir, silent_mode = args.mode == 'cli')

    if args.mode == 'listen':
        ip, port = args.address.split(':')

        server_address = (ip, int(port))
        handler = HttpHandler(version_maintainer=version_maintainer)
        with HTTPServer(server_address, handler) as httpd:
            address = f'{ip}:{port}'
            print(f'Started listening on {utils.format_text(address)}')
            print(f'Use CTRL+C to close')

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print('Closing... ', end='')
        print('Gracefully closed')
    else:
        if args.update:
            next_version = version_maintainer.bump_version_number(args.job)
            print(f'Next version for {utils.format_text(args.job)} will be {utils.format_text(str(next_version))}')
        else:
            print(version_maintainer.get_version_number(args.job))

if __name__ == '__main__':
    run()
