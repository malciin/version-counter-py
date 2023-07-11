def read_utf8(path: str) -> str:
    with open(path, mode='rb') as f:
        return f.read().decode(encoding='utf8')

def format_text(str: str) -> str:
    return f'\033[1m\033[92m{str}\033[0m'

