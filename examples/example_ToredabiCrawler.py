from CommandScheduler.Commander import Commander
from ToredabiCrawler.TradeDerby import TradeDerby

from private import username, password, slackURL
from schedule import schedule


config_command = {"slackURL": slackURL, "logFile": "log/log"}
cm = Commander(config_command)

# login
account = {"username": username, "password": password}
config_toredabi = {"headless": True, "debug": True}
td = TradeDerby(account, config_toredabi)
td.open()
td.login()

# make schedule
cm.addTaskFromClass(td)
cm.makeSchedule(schedule)

cm.procedure()
