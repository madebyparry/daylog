#!/usr/bin/env python3
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
    strNowMo = now.strftime("%m_%B")
    global currentTime
    global currentDate
    global currentMonth
    currentTime = strNowTime
    currentDate = strNowDate
    currentMonth = strNowMo

def whatDo():
    did = input("What'd ya do? \n>> " + Fore.YELLOW)
    conf = input(Style.RESET_ALL + "Did you do " + Fore.YELLOW + "'" + did + Style.RESET_ALL + "'" + "? " + Style.DIM + "(y, n)" + Style.RESET_ALL + " : ")
    if (conf == "n"):
        whatDo()
    elif (conf == "y"):
        global done
        done.append(did)
        moreCheck()
    else:
        print(":(")
        whatDo()

def resetDo():
    global done
    del done[:]
    whatDo()

def moreCheck():
    conf = input("Did anything else? " + Style.DIM + "(y, n)" + Style.RESET_ALL + " : ")
    if (conf == "n"):
        lastConfirm()
    elif (conf == "y"):
        whatDo()
    else:
        print(":(")
        moreCheck()

def lastConfirm():
    print("\n")
    i = 0
    while i < len(done):
        c = i + 1
        print(Fore.MAGENTA + str(c) + ": " + done[i] + ";" + Style.RESET_ALL)
        i = i + 1
    print("\n")
    conf = input("Looks good? " + Style.DIM + "(y [submit], n[reset])" + Style.RESET_ALL + " : ")
    if (conf == "n"):
        resetDo()
        whatDo()
    elif (conf == "y"):
        writeResults()
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


    # Write content
    with open("logs/daylog.txt", "a") as f:
        for i in doneList:
            f.write("%s\n" % i)



#
# woohoo.
# alias daylog="/home/%USER/scripts/daylog/daylog.py"
#
main()
