import sys
import os
from select import select
# from threading import Timer
import msvcrt
import time


class Commander(object):
    def __init__(self):
        self.nameList = []
        self.functionList = []
        self.number = 0

        self.addTask("info", self.showInformation)
        self.addTask("end", self.end)

    def showInformation(self):
        print("-------------------------")
        print("---   Command list    ---")
        print("-------------------------")
        for i in range(self.number):
            print(self.nameList[i], "/ ", end="")
            if (i + 1) % 5 == 0:
                print()
        print()
        print("-------------------------")

    def raw_input_with_timeout(self, timeout=60.0):
        timer = time.monotonic
        if os.name == "nt":
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
                return sys.stdin.readline()
            else:
                return False

    def addTask(self, name, function):
        self.nameList.append(name)
        self.functionList.append(function)
        self.number += 1

    def addTaskFromClass(self, classObject):
        names = dir(classObject)
        for name in names:
            if name[0] != "_" and callable(classObject.__getattribute__(name)):
                self.addTask(name, classObject.__getattribute__(name))

    def end(self):
        sys.exit(0)

    def procedure(self):
        self.showInformation()
        while True:
            cmd =  self.raw_input_with_timeout()
            if cmd == False:
                pass
            elif cmd in self.nameList:
                self.functionList[self.nameList.index(cmd)]()
            else:
                print(cmd, ": not registerd.")
