from PyCmdSched import PyCmdSched
from private import slackURL

config = {"slackURL": slackURL, "logName": "log/log"}

cm = PyCmdSched(config)

cm.procedure()
