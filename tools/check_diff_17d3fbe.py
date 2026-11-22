import subprocess

res = subprocess.run(['git', 'diff', '9496b4e', '17d3fbe', '--', 'assets/B1Nq4Kq6.js'], capture_output=True, text=True)
for line in res.stdout.splitlines():
    if line.startswith(('+', '-')) and not line.startswith(('+++', '---')):
        print(line[:120])
