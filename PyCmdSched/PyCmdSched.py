import sys
import os
import traceback
from datetime import datetime, timedelta
import requests
import json
if os.name == "nt":
    import msvcrt
    import time
else:
    from select import select


class PyCmdSched(object):

    def __init__(self, config):
        # task
        self.taskList = []
        self.functionList = []
        self.numberTask = 0

        # schedule
        self.scheduleList = []
        self.previous = []
        self.cycle = []
        self.numberSchedule = 0

        self.addTask("showTask", self.showTask)
        self.addTask("addTask", self.addTask)
        self.addTask("showSchedule", self.showSchedule)
        self.addTask("addSchedule", self.addSchedule)
        self.addTask("end", self.end)

        self.loadConfig(config)

    def loadConfig(self, config):
        if "slackURL" not in config.keys() or config["slackURL"] == "":
            self.slack = False
        else:
            self.slack = True
            self.slackURL = config["slackURL"]
            self.sendSlack("Connected to slack")

        if "logName" not in config.keys() or config["logName"] == "":
            self.log = False
        else:
            self.log = True
            self.logName = config["logName"]
            self.writeLog(self.timeStamp() + "start log")

    def timeStamp(self):
        return datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")

    def writeLog(self, message):
        import csv
        f = open(self.logName, "a")
        writer = csv.writer(f)
        writer.writerow([message])
        f.close()

    def sendSlack(self, message):
        if not self.slack:
            print("slack URL not found")
        else:
            try:
                requests.post(self.slackURL, data=json.dumps({
                    "text": message,
                    "username": os.uname()[1],
                    "icon_emoji": u":ghost",
                    "link_names": 1,
                }))
            except ConnectionError:
                print("Error : Could not send message to slack")

    def showTask(self):
        print("-------------------------")
        print("-----   Task list   -----")
        print("-------------------------")
        for i in range(self.numberTask):
            print(self.taskList[i], "/ ", end="")
            if (i + 1) % 5 == 0 and (i + 1) != self.numberTask:
                print()
        print()
        print("-------------------------")

    def showSchedule(self):
        print("-------------------------")
        print("---   Schedule list   ---")
        print("-------------------------")
        for i in range(self.numberSchedule):
            print(
                self.scheduleList[i],
                self.previous[i].strftime("%Y-%m-%d %H:%M:%S"),
                self.cycle[i]
            )
        print("-------------------------")

    def raw_input_with_timeout(self, timeout=60.0):
        if os.name == "nt":
            timer = time.monotonic
            endtime = timer() + timeout
            line = ""
            while timer() < endtime:
                if msvcrt.kbhit():
                    c = msvcrt.getwche()
                    if c in ["\n", "\r"]:
                        print()
                        return line
                    elif c == "\b":
                        line = line[:-1]
                    else:
                        line += c
                time.sleep(0.04)
            return False
        else:
            rlist, _, _ = select([sys.stdin], [], [], timeout)
            if rlist:
                return sys.stdin.readline()[:-1]
            else:
                return False

    def addSchedule(self, name, minutes, execute=False):
        if name not in self.taskList:
            print(name, ": Not Found")
            return False

        if execute:
            self.functionList[self.taskList.index(name)]()

        self.scheduleList.append(name)
        self.previous.append(datetime.now())
        self.cycle.append(int(minutes))
        self.numberSchedule += 1

    def addTask(self, name, function):
        self.taskList.append(name)
        if isinstance(function, str):
            self.functionList.append(eval(function))
        else:
            self.functionList.append(function)
        self.numberTask += 1

    def addTaskFromClass(self, classObject):
        names = dir(classObject)
        for name in names:
            if name[0] != "_" and callable(classObject.__getattribute__(name)):
                self.addTask(
                    classObject.__class__.__name__ + "." + name,
                    classObject.__getattribute__(name)
                    # classObject.__class__.__name__
                )

    def makeSchedule(self, schedule):
        for sch in schedule.keys():
            if sch not in self.taskList:
                print(sch, ": Not Found")
            else:
                self.addSchedule(sch, schedule[sch])

    def end(self):
        sys.exit(0)

    def routine(self):
        for i in range(self.numberSchedule):
            name = self.scheduleList[i]
            diff = datetime.now() - self.previous[i]
            if timedelta(minutes=self.cycle[i]) <= diff:
                ret = self.functionList[self.taskList.index(name)]()
                self.previous[i] = datetime.now()
                if self.slack:
                    self.sendSlack(ret)
                if self.log:
                    self.writeLog(ret)

    def procedure(self):
        self.showTask()
        self.showSchedule()
        while True:
            cmd = self.raw_input_with_timeout()
            if cmd is False or len(cmd) == 0:
                pass
            else:
                cmd = cmd.split()
                if cmd[0] in self.taskList:
                    try:
                        ret = ""
                        if len(cmd) == 1:
                            ret = self.functionList[
                                self.taskList.index(cmd[0])]()
                        else:
                            ret = self.functionList[
                                self.taskList.index(cmd[0])](*cmd[1:])
                        if isinstance(ret, str) and self.slack:
                            self.sendSlack(ret)
                    except TypeError as e:
                        print(traceback.format_exc())
                else:
                    print(cmd, ": not registered.")

            self.routine()
