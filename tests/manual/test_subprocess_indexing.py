import subprocess

args = input("Args: ").split(sep=" ")

result = subprocess.run(["bin/image-indexing-engine"] + args, check=False)

print(result)
