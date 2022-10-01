import datetime
import os
import subprocess

first_run = not os.path.exists("config/logs/initial-setup.log")
sports_monthly_run = os.path.exists("config/logs/sports-" + datetime.datetime.now().strftime("%B").lower() + ".log")


def pull_sports(first_setup=False):
    print("Pulling sports schedules for " + datetime.date.today().strftime("%B") + "...")
    print(
        subprocess.run(["./manage.py", "import_sports", str(datetime.date.today().month)], check=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
    )

    print("Writing to new sports log file...")
    with open("config/logs/sports-" + datetime.datetime.now().strftime("%B").lower() + ".log", "w", encoding="utf8") as f:
        f.write("Sports schedules have been pulled for " + datetime.date.today().strftime("%B") + ".")
        f.write("\nDelete this file to re-pull sports schedules on next startup.")

    if not first_setup:
        today = datetime.date.today()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        print("Removing old sports log file...")
        os.remove("config/logs/sports-" + last_month.strftime("%B").lower() + ".log")


def initial_setup():
    print("---- Running initial setup tasks -----")
    subprocess.run(["chmod", "+x", "config/docker/initial_setup.sh"], check=True, stdout=subprocess.PIPE)
    subprocess.run(["chmod", "+x", "config/data/generate_data.sh"], check=True, stdout=subprocess.PIPE)
    print(subprocess.run(["config/docker/initial_setup.sh"], check=True, stdout=subprocess.PIPE).stdout.decode("utf-8"))

    pull_sports(first_setup=True)

    with open("config/logs/initial-setup.log", "w", encoding="utf8") as f:
        f.write("Initial setup: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        f.write("\nDelete this file to re-run initial setup tasks on next startup.")

    print()
    print("Run './create-users.py -a [USERNAME]' to create an admin user for yourself.")
    print("Alternatively, login with username 'admin' and password 'notfish'")
    print("---- Completed initial setup. ----")


if first_run:
    initial_setup()

if not sports_monthly_run and not first_run:
    pull_sports()

print("Starting web server...")
welcome = """
    ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗     ██╗                   ██╗
    ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ██║ ██████╗ ███╗   ██╗██║
    ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗         ██║   ██║   ██║    ██║██║   ██║██╔██╗ ██║██║
    ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝         ██║   ██║   ██║    ██║██║   ██║██║╚██╗██║╚═╝
    ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝    ██║╚██████╔╝██║ ╚████║██╗
     ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝         
"""
print(welcome)
subprocess.run(["config/docker/entrypoint.sh"], check=True, stdout=subprocess.PIPE)
