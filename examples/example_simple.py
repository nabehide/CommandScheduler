from CommandScheduler.Commander import Commander
from private import slackURL


cm = Commander(slackURL)

# import numpy as np
# cm.addTaskFromClass(np)

cm.procedure()
