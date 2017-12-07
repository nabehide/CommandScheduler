from CommandScheduler.Commander import Commander
from private import slackURL

config = {"slackURL": slackURL, "logName": "log/log"}

cm = Commander(config)

cm.procedure()
