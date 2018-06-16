from CheckPoint import CheckPoint
from PyCmdSched import PyCmdSched
import private
from private import slackURL, doc_id, spreadPath

config = {"slackURL": slackURL, "logName": "log/log"}

cm = PyCmdSched(config)

cp = CheckPoint(doc_id, spreadPath, private)
cm.addTaskFromClass(cp)

cm.procedure()
