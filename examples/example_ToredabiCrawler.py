from CommandScheduler.Commander import Commander
from ToredabiCrawler.TradeDerby import TradeDerby

from private import username, password


cm = Commander()

account = {"username": username, "password": password}
config = {"headless": False, "debug": True}
td = TradeDerby(account, config)
cm.addTaskFromClass(td)

cm.procedure()
