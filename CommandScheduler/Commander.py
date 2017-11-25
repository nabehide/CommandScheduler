import sys
import os
from datetime import datetime
if os.name == "nt":
    import msvcrt
    import time
else:
    from select import select


class Commander(object):
    def __init__(self):
        # task
        self.taskList = []
        self.functionList = []
        self.numberTask = 0

        # schedule
        self.scheduleList = []
        self.previous =  []
        self.cycle = []
        self.numberSchedule = 0

        self.addTask("info", self.showInformation)
        self.addTask("addSchedule", self.addSchedule)
        self.addTask("end", self.end)

    def showInformation(self):
        print("-------------------------")
        print("---   Command list    ---")
        print("-------------------------")
        for i in range(self.numberTask):
            print(self.taskList[i], "/ ", end="")
            if (i + 1) % 5 == 0 and (i + 1) != self.numberTask:
                print()
        print()
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
        self.functionList.append(function)
        self.numberTask += 1

    def addTaskFromClass(self, classObject):
        names = dir(classObject)
        for name in names:
            if name[0] != "_" and callable(classObject.__getattribute__(name)):
                self.addTask(name, classObject.__getattribute__(name))

    def end(self):
        sys.exit(0)

    def routine(self):
        for i in range(self.numberSchedule):
            name = self.scheduleList[i]
            diff = datetime.now() - self.previous[i]
            if self.cycle[i] * 60 <= diff.seconds:
                self.functionList[self.taskList.index(name)]()
                self.previous[i] = datetime.now()

    def procedure(self):
        self.showInformation()
        while True:
            cmd = self.raw_input_with_timeout()
            if cmd is False or len(cmd) == 0:
                pass
            else:
                cmd = cmd.split()
                if cmd[0] in self.taskList:
                    if len(cmd) == 1:
                        self.functionList[self.taskList.index(cmd[0])]()
                    elif len(cmd) == 2:
                        self.functionList[self.taskList.index(cmd[0])](cmd[1])
                    elif len(cmd) == 3:
                        self.functionList[self.taskList.index(cmd[0])](cmd[1], cmd[2])
                    else:
                        print("too many args")
                else:
                    print(cmd, ": not registerd.")

            self.routine()
