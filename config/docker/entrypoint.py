import os
import subprocess
import datetime

first_run = not os.path.exists("config/docker/first-run.log")

if first_run:
    print("---- Running initial setup tasks -----")
    subprocess.run(["chmod", "+x", "config/docker/initial_setup.sh"], check=True, stdout=subprocess.PIPE)
    print(subprocess.run(["config/docker/initial_setup.sh"], check=True, stdout=subprocess.PIPE).stdout.decode("utf-8"))

    print("Pulling sports schedules for " + datetime.date.today().strftime("%B") + "...")
    print(
        subprocess.run(["./manage.py", "import_sports", str(datetime.date.today().month)], check=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
    )

    with open("config/docker/first-run.log", "w", encoding="utf8") as f:
        f.write("Initial setup: " + datetime.date.today().strftime("%Y-%m-%d %H:%M:%S") + " UTC")

    print("Run './create-users.py -a [USERNAME]' to create an admin user for yourself.")
    print("Alternatively, login with username 'admin' and password 'notfish'")
    print("---- Completed initial setup. ----")

if datetime.date.today().day == 1:
    print("Pulling sports schedules for " + datetime.date.today().strftime("%B") + "...")
    print(
        subprocess.run(["./manage.py", "import_sports", str(datetime.date.today().month)], check=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
    )

print("Starting web server...")
print("Welcome to Ion!")
subprocess.run(["config/docker/entrypoint.sh"], check=True, stdout=subprocess.PIPE)
