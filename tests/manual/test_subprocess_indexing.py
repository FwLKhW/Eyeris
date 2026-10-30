import subprocess

result = subprocess.run(["bin/iie", "index", "fixtures/imgs/", "-e"], check=False)

print(result)
