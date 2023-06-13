#!/usr/bin/env python3
import sys
import os.path
from datetime import datetime
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

def main():
    setConst()
    whatDo()

def setConst():
    global done
    done = []

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
    confIn = input(Style.RESET_ALL + "Did anything else? " + Style.DIM + "(y [yes], n [no], u [undo], l [list])" + Style.RESET_ALL + " : ")
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
    conf = input("Looks good? " + Style.DIM + "(y [submit], n [reset], u #[undo], c [cancel])" + Style.RESET_ALL + " : ")
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
    homeRoot = os.path.expanduser('~')
    daylogRoot = homeRoot + "/daylog"
    logRoot = "/logs"
    monthDir = "/" + currentMonth + ".log"
    currentLog = daylogRoot + logRoot + monthDir
    errorCatch = homeRoot + "/daylog/err.log"

    # Write content
    with open(currentLog, "a") as f:
        try:
            for i in doneList:
                f.write("%s\n" % i)
        except:
            print("Error in path " + daylogRoot + logRoot + "printing to " + errorCatch)
            with open(currentLog, "a") as f:
                try: 
                    for i in doneList:
                        f.write("%s\n" % 1)
                except:
                    print("Shit is fucked.")

#
# woohoo.
# alias daylog="/home/%USER/scripts/daylog/daylog.py"
#
main()
