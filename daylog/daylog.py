#!/usr/bin/env python3
import sys
import getopt
import os.path
from datetime import datetime
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

def main(opts, args):
    if opts:
        checkArgs(opts, args)
    else:
        setConst()
        whatDo()

def setConst():
    global done
    done = []
    

def checkArgs(opts, args):
    for opt, args in opts:
        if opt in ("-h", "--help", "?"):
            print(Style.DIM + "-h [help], -l [list], -o [out], -e [edit], -t [new task], -v [view task]" + Style.RESET_ALL)
        elif opt in ("-l", "--list"):
            setDirs()
            os.system("cat " + currentLog)
        elif opt in ("-o", "--out"):
            setDirs()
            print(Style.DIM + "\nCurrent log output:" + Style.RESET_ALL)
            print("\n\t" + Fore.MAGENTA +  currentLog + Style.RESET_ALL + "\n")
        elif opt in ("-e", "--edit"):
            print("[TODO]: " + args + " args")
        elif opt in ("-t", "--task"):
            newTask(args)
        elif opt in ("-v", "--view"):
            viewTasks()



def setTime():
    now = datetime.now() 
    strNowTime = now.strftime("%H:%M:%S")
    strNowDate = now.strftime("%m / %d / %y -- %A")
    strNowMo = now.strftime("%Y_%B")
    global currentTime
    global currentDate
    global currentMonth
    currentTime = strNowTime
    currentDate = strNowDate
    currentMonth = strNowMo

def setDirs():
    setTime()
    global currentLog
    global daylogRoot
    global logRoot
    global taskFile
    global errorCatch
    homeRoot = os.path.expanduser('~')
    daylogRoot = homeRoot + "/daylog"
    logRoot = "/logs"
    monthLog = "/" + currentMonth + ".log"
    taskFile = daylogRoot + "/tasks/taskfile.txt"
    currentLog = daylogRoot + logRoot + monthLog
    errorCatch = homeRoot + "/daylog/err.log"


def whatDo():
    did = input("What'd ya do? \n>> " + Fore.YELLOW)
    global done
    done.append(did)
    moreCheck()

def resetLastDo(i):
    global done
    if i == "u":
        done.pop()
        listLogs()
        moreCheck()
    else: 
        done.pop(int(i) - 1)
        listLogs()
        moreCheck()

def resetDoAll():
    global done
    del done[:]
    whatDo()

def moreCheck():
    confIn = input(Style.RESET_ALL + "Did anything else? " + Style.DIM + "\n(y [yes], n [no], u [undo done], l [list done], t [view tasks], a [add task to done]) \n" + Style.RESET_ALL + ":: ")
    conf = confIn.lower()
    if len(conf) > 1:
        conf = conf.split()        
    if (conf[0] == "n" or conf == "no" or conf == "nah"):
        lastConfirm()
    elif (conf[0] == "y" or conf == "yes" or conf == "yeah"):
        whatDo()
    elif (conf[0] == "u" or conf == "undo"):
        if conf[-1] == None:
            resetLastDo(conf[0])
        else:
            resetLastDo(conf[-1])
    elif (conf[0] == "l" or conf == "list"):
        listLogs()
        moreCheck()
    elif (conf[0] == "t" or conf == "tasks"):
        viewTasks()
        moreCheck()
    elif (conf[0] == "a" or conf == "add"):
        if conf[-1] == "a":
            viewTasks()
            print("What task did you do? (-a [NUM])")
            moreCheck()
        else:
            didTask(conf[-1])
            listLogs()
            moreCheck()
    elif (conf[0] == "c"):
        sys.exit()
    else:
        print(":(")
        moreCheck()

def listLogs(color=Fore.CYAN):
    print("\n")
    i = 0
    while i < len(done):
        c = i + 1
        print(color + str(c) + ": " + done[i] + ";" + Style.RESET_ALL)
        i = i + 1
    print("\n")

def lastConfirm():
    listLogs(Fore.MAGENTA)
    conf = input("Looks good? " + Style.DIM + "(y [submit], n [reset], u [undo], c [cancel])" + Style.RESET_ALL + " : ")
    if (conf == "n"):
        resetDoAll()
        whatDo()
    elif (conf == "y"):
        writeResults()
    elif (conf == "u"):
        resetLastDo()
    elif (conf == "c"):
        sys.exit()
    else:
        print(":(")
        lastConfirm()


def writeResults():
    setTime()
    # pull globals
    global done
    global currentTime
    global currentDate
    global currentMonth
    # Var to store formatted data
    doneList = []
    #Format header and footer
    listHeader = '''

    ==================================================================
    {}
    ==================================================================
    '''.format(currentDate)

    listFooter = '''
    ------------------------------------------------------------------
    {}
    ------------------------------------------------------------------


    '''.format(currentTime)

    # Make header
    doneList.append(listHeader)
    # Make body
    i = 0
    print(Fore.MAGENTA + "\nLogged: \n" + Style.RESET_ALL)
    while i < len(done):
        c = i + 1
        doneList.append("\t" + str(c) + ": " + done[i] + ";")
        print(Fore.MAGENTA + doneList[-1] + Style.RESET_ALL)
        i = i + 1
    # Make footer
    doneList.append(listFooter)
    print(Fore.MAGENTA + "\t=== end ===\n" + Style.RESET_ALL)


    # set dest folder
    setDirs()

    # Write content
    with open(currentLog, "a") as f:
        try:
            for i in doneList:
                f.write("%s\n" % i)
        except:
            print("Error in path " + daylogRoot + logRoot + "printing to " + errorCatch)
            with open(errorCatch, "a") as f:
                try: 
                    for i in doneList:
                        f.write("%s\n" % 1)
                except:
                    print("Shit is fucked, yo.")

# Tasks
def newTask(x):
    setDirs()
    if x == "view":
        viewTasks()
    else:
        with open(taskFile, "a") as f:
            f.write(x + '\n')
        print("New task: " + Fore.YELLOW + x + Style.RESET_ALL)

def viewTasks():
    setDirs()
    print('\n' + 'Tasks:')
    with open(taskFile, 'r') as f:
        i = 0
        for line in f:
            i = i + 1
            print('\t' + str(i) + ') ' + line, end='')
    print('\n')

def didTask(n):
    x = int(n)
    f_lines = []
    if type(x) is int:
        setDirs()
        with open(taskFile, 'r') as f:
            f_lines = f.readlines()
            done.append(f_lines[x - 1][0:-1])
            f_lines.pop(x - 1)
        with open(taskFile, 'w') as fw:
            fw.writelines(f_lines)
    else: 
        print("set the number to add task")
        moreCheck()
#
# woohoo.
# alias daylog="/home/%USER/scripts/daylog/daylog.py"
#
try:
    inputOpts, inputArgs = getopt.getopt(sys.argv[1:], "hloe:t:v", ["help","out","edit"])
    main(inputOpts, inputArgs)
except:
    print("daylog out.")