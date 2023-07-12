import argparse
import utils
from http.server import HTTPServer
from http_handler import HttpHandler
from version_maintainer import VersionMaintainer

def run():
    parser = argparse.ArgumentParser(
        description='Python service/cli tool for computing next version value. Source code: https://github.com/malciin/version-counter-py')
    
    parser.add_argument(
        '--versions-dir',
        help=f'(Optional) Where should store versions info data. Default to {utils.accent_text(".versions")}',
        default='.versions',
        required=False)

    subparsers = parser.add_subparsers(
        dest='mode',
        help='mode',
        required=True)
    
    cli_parser = subparsers.add_parser('get')
    cli_parser.add_argument('job')

    cli_parser = subparsers.add_parser('bump')
    cli_parser.add_argument('job')

    cli_parser = subparsers.add_parser('show')
    
    listen_parser = subparsers.add_parser('listen')
    listen_parser.add_argument(
        'address',
        help=f'On which address and port should listen. Eg. {utils.accent_text("--listen :8080")}, {utils.accent_text("--listen localhost:8080")}',
        default=False)

    args = parser.parse_args() 

    version_maintainer = VersionMaintainer(args.versions_dir, silent_mode = args.mode != 'listen')

    if args.mode == 'listen':
        ip, port = args.address.split(':')

        server_address = (ip, int(port))
        handler = HttpHandler(version_maintainer=version_maintainer)
        with HTTPServer(server_address, handler) as httpd:
            address = f'{ip}:{port}'
            print(f'Started listening on {utils.accent_text(address)}')
            print(f'Use CTRL+C to close')

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print('Closing... ', end='')
        print('Gracefully closed')
    elif args.mode == 'bump':
        next_version = version_maintainer.bump_version_number(args.job)
        print(f'Next version for {utils.accent_text(args.job)} will be {utils.accent_text(str(next_version))}')
    elif args.mode == 'get':
        print(version_maintainer.get_version_number(args.job))
    else:
        version_maintainer.print_current_versions_values()

if __name__ == '__main__':
    run()
