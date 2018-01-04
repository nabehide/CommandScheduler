from PyCmdSched import PyCmdSched
from TradeDerPy import TradeDerPy

from private import username, password, slackURL
from schedule import schedule


config_command = {"slackURL": slackURL, "logFile": "log/log"}
cm = PyCmdSched(config_command)

# toredabi login
account = {"username": username, "password": password}
config_toredabi = {
    "headless": True,
    "debug": True,
    "driverPath": "./chromedriver",
}
td = TradeDerPy(account, config_toredabi)
td.open()
td.login()

# make schedule
cm.addTaskFromClass(td)
cm.makeSchedule(schedule)

cm.procedure()
