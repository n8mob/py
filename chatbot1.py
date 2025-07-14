import random

def handle_input(text):
    commands = {
        'tape': lambda *args: '📼 Be kind, rewind.',
        'hello': lambda name='stranger': f'👋 Hello, {name}!',
        'wordle': lambda *args: '🟩🟨⬜ Starting Wordle clone... (not really)',
        'random': lambda *args: str(random.randint(1, 100)),
        'bitpunk': lambda *args: random.choice([
            '🧠✨ Neurodisk online.',
            '🔓 TapeDeck access granted.',
            '📡 Scrambling magstripe comms...',
            '🔦 Neon-lit hallway echoes.',
            '🗝️ Unlocking cassette vault...',
        ]),
        'decode': lambda *args: (
            f'Decoding: {" ".join(args)}\n'
            f'→ {"".join(chr(int(b, 2)) for b in args if b.isdigit() and len(b) == 8)}'
            if args else '⚠️ Usage: /decode 01001000 01101001'
        ),
    }

    if not text.startswith('/'):
        return '⚠️ Not a slash command.'

    parts = text[1:].split()
    cmd = parts[0]
    args = parts[1:]

    func = commands.get(cmd)
    if func:
        try:
            return func(*args)
        except Exception as e:
            return f'💥 Error: {e}'
    else:
        return f'❓ Unknown command: /{cmd}'


if __name__ == '__main__':
    print("📼 Bitpunk Bot — type /help or /quit to exit.\n")
    while True:
        cmd = input('> ')
        if cmd.strip() in ('/quit', '/exit'):
            break
        elif cmd.strip() == '/help':
            print("Available commands: /tape /hello /wordle /random /bitpunk /decode")
        else:
            print(handle_input(cmd))
