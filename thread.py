import subprocess


files = ["app.py", "main.py"]  # файлы, которые нужно запустить
for file in files:
    subprocess.Popen(args=["start", "python", file], shell=True, stdout=subprocess.PIPE)
