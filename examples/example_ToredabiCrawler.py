from CommandScheduler.Commander import Commander
from ToredabiCrawler.TradeDerby import TradeDerby

from private import username, password, slackURL
from schedule import schedule


cm = Commander(slackURL)

# login
account = {"username": username, "password": password}
config = {"headless": True, "debug": True}
td = TradeDerby(account, config)
td.open()
td.login()

# make schedule
cm.addTaskFromClass(td)
cm.makeSchedule(schedule)

cm.procedure()
