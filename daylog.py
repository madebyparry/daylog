#!/usr/bin/env python3
import sys
import os
import time
import random
import argparse
import data.settings as daylog_settings
from datetime import datetime
from colorama import init as colorama_init, Fore, Style

colorama_init()
print(daylog_settings.user_paths['daylog_root'])

def splash_screen():
    possible_greetings = [
        'Hello bb ', 
        "It's time to get choppin'",
        "Welcome to Daylog",
        "Productive or not, it's logging time.",
        "How was your day?", 
        '* rat zone * ']
    greeting_splash = possible_greetings[random.randint(0, len(possible_greetings) - 1)]
    left_side_frame = '|'
    right_side_frame = '|'
    top_bottom_frame = '='
    term_size = os.get_terminal_size()
    print('/ ' + (top_bottom_frame * (term_size.columns - 4)) + ' \\')
    for i in range(0,int((term_size.lines - 10) / 2)):
        print(left_side_frame + (' ' * (term_size.columns - 2)) + right_side_frame)
    print(left_side_frame + (' ' * int((term_size.columns / 2) - (len(greeting_splash) / 2) - 1)) + greeting_splash + (' ' * int((term_size.columns / 2) - (len(greeting_splash) / 2) - 1)) + right_side_frame)
    for i in range(0,int((term_size.lines - 10) / 2)):
        print(left_side_frame + (' ' * (term_size.columns - 2)) + right_side_frame)
    print('\\ ' + (top_bottom_frame * (term_size.columns - 4)) + ' /')
    time.sleep(2)

def get_current_time():
    now = datetime.now() 
    current_time = {}
    current_time['time'] = {}
    current_time['date'] = {}
    current_time['time']['hour'] = now.strftime("%H")
    current_time['time']['minute'] = now.strftime("%M")
    current_time['time']['second'] = now.strftime("%S")
    current_time['time']['time_full'] = now.strftime("%H:%M:%S")
    current_time['date']['weekday'] = now.strftime("%A")
    current_time['date']['day'] = now.strftime("%d")
    current_time['date']['month'] = now.strftime("%m")
    current_time['date']['month_long'] = now.strftime("%B")
    current_time['date']['year'] = now.strftime("%y")
    current_time['date']['year_long'] = now.strftime("%Y")
    current_time['date']['date_full'] = now.strftime("%A -- %m / %d / %y")
    return current_time

def get_args():
    parser = argparse.ArgumentParser('daylog')
    parser.add_argument('-n', '--new', action='store_true')
    parser.add_argument('-t', '--task', type=str)
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-a', '--append', type=str)
    parser.add_argument('-e', '--edit', action='store_true')
    args = parser.parse_args()
    return args

def triage_args():
    args = get_args()
    if not (args.new or args.list  or args.task or args.append or args.edit):
        new_log_list()
    if args.new:
        new_log_list()
    if args.list:
        print('todo: list... ' + str(args.list) )
    if args.task:
        print('todo: task... ' + str(args.task) )
    if args.append != None:
        print('todo: append... ' + str(args.append) )
    if args.edit:
        print('todo: edit... ' + str(args.edit) )

def new_log_list():
    global done
    done = []
    interactive_prompt()


def new_log_item():
    greeting = "\nWhat'd ya do?"
    print(greeting)
    did = input(">> " + Fore.YELLOW)
    done.append(did)
    print(Style.RESET_ALL)

def list_log_items(color=Fore.CYAN):
    print("\n")
    i = 0
    while i < len(done):
        c = i + 1
        print(color + str(c) + ": " + done[i] + ";" + Style.RESET_ALL)
        i = i + 1
    print("\n")


def undo_last_log_item(i):
    if i == "u":
        done.pop()
    else: 
        done.pop(int(i) - 1)

def reset_new_log():
    del done[:]

def new_task_item():
    print('boop - todo')

def mark_task_done():
    print('beep - todo')

# def initial_prompt():
#     print(Style.DIM + "h [help], n [new], l [list], o [out], e [edit], t [new task], v [view task], c [cancel]" + Style.RESET_ALL)
#     conf = input('How can we get started today?')
#     conf = conf.lower()
#     if conf[0] == 'n':
#         new_log_item()
#     if conf[0] == 'c':
#         os.abort()
#         final_confirmation()
#     if conf[0] == 'u':
#         undo_last_log_item(conf[-1])
#     if conf[0] == 'r':
#         reset_new_log()
#     if conf[0] == 't':
#         new_task_item()

def interactive_prompt():
    valid_selections = ['y', 'n', 'u', 'l', 't', 'a', 'c']
    continue_prompt = True
    def get_conf():
        confIn = input(Style.RESET_ALL + "Have stuff? " + Style.DIM + "\n(y [yes], n [no], u [undo done], l [list done], t [view tasks], a [add task to done]), c[cancel] \n" + Style.RESET_ALL + ":: ")
        conf = confIn.lower()
        return conf
    while continue_prompt == True:
        conf = get_conf()
        if len(conf) > 1:
            conf = conf.split() 
        if conf[0] not in valid_selections:
            print('\nplease pick a valid selection!\n')
        if conf[0] == 'y':
            new_log_item()
        if conf[0] == 'n':
            continue_prompt = False
            final_confirmation()
        if conf[0] == 'u':
            undo_last_log_item(conf[-1])
            list_log_items(Fore.LIGHTRED_EX)
        if conf[0] == 'r':
            reset_new_log()
        if conf[0] == 't':
            new_task_item()
        if conf[0] == 'a':
            new_task_item()
        if conf[0] == 'c':
            print('Bye bye!')
            sys.exit()
        if conf[0] == 'l':
            list_log_items(Fore.CYAN)

def final_confirmation():
    list_log_items(Fore.MAGENTA)
    conf = input("Looks good? \n" + Style.DIM + "(y [submit], n [reset], u [undo], c [cancel])" + Style.RESET_ALL + "\n:: ")
    if (conf == "n"):
        reset_new_log()
        interactive_prompt()
    elif (conf == "y"):
        writeResults()
    elif (conf == "u"):
        undo_last_log_item(-1)
        final_confirmation()
    elif (conf == "c"):
        print('Bye bye!')
        sys.exit()
    else:
        print(":(")
        final_confirmation()


def writeResults():
    current_time = get_current_time()
    # Var to store formatted data
    doneList = []
    #Format header and footer
    listHeader = '''

    ==================================================================
    {}
    ==================================================================
    '''.format(current_time['date']['date_full'])

    listFooter = '''
    ------------------------------------------------------------------
    {}
    ------------------------------------------------------------------


    '''.format(current_time['time']['time_full'])


    # set dest folder
    user_paths = get_directories(current_time)

    # Set header
    doneList.append(listHeader)
    # Set body
    i = 0
    print(Fore.MAGENTA + "\n\tLogged: \n" + Style.RESET_ALL)
    while i < len(done):
        c = i + 1
        doneList.append("\t" + str(c) + ": " + done[i] + ";")
        print(Fore.MAGENTA + Style.BRIGHT + doneList[-1] + Style.RESET_ALL)
        i = i + 1
    # Make footer
    doneList.append(listFooter)
    print(Fore.MAGENTA + "\n\t=== end ===\n" + Style.RESET_ALL)

    print(Fore.MAGENTA + Style.DIM + '(' + user_paths['log_file'] + ")\n" + Style.RESET_ALL)
    # Write content
    with open(user_paths['log_file'], "a") as f:
        try:
            for i in doneList:
                f.write("%s\n" % i)
        except:
            print("Error in path " + user_paths['log_dir'])
            # with open(errorCatch, "a") as f:
            #     try: 
            #         for i in doneList:
            #             f.write("%s\n" % 1)
            #     except:
            #         print("Shit is fucked, yo.")


def get_directories(current_time):
    user_paths = {}
    user_paths['daylog_root'] = daylog_settings.user_paths['daylog_root']
    user_paths['log_dir'] = user_paths['daylog_root'] + daylog_settings.user_paths['log_directory']
    user_paths['log_file'] = user_paths['log_dir'] + '/' + current_time['date']['year_long'] + '_' + current_time['date']['month_long'] + '.log'
    user_paths['task_dir'] = user_paths['daylog_root'] + daylog_settings.user_paths['task_directory'] 
    user_paths['task_file'] = user_paths['task_dir'] + daylog_settings.user_paths['task_file'] 
    return user_paths

# def new_log_list():
    # confIn = input(Style.RESET_ALL + "Did anything else? " + Style.DIM + "\n(y [yes], n [no], u [undo done], l [list done], t [view tasks], a [add task to done]) \n" + Style.RESET_ALL + ":: ")
    # conf = confIn.lower()
    # if len(conf) > 1:
    #     conf = conf.split()        
    # if (conf[0] == "n" or conf == "no" or conf == "nah"):
    #     lastConfirm()
    # elif (conf[0] == "y" or conf == "yes" or conf == "yeah"):
    #     whatDo()
    # elif (conf[0] == "u" or conf == "undo"):
    #     if conf[-1] == None:
    #         resetLastDo(conf[0])
    #     else:
    #         resetLastDo(conf[-1])
    # elif (conf[0] == "l" or conf == "list"):
    #     listLogs()
    #     moreCheck()
    # elif (conf[0] == "t" or conf == "tasks"):
    #     viewTasks()
    #     moreCheck()
    # elif (conf[0] == "a" or conf == "add"):
    #     if conf[-1] == "a":
    #         viewTasks()
    #         print("What task did you do? (-a [NUM])")
    #         moreCheck()
    #     else:
    #         didTask(conf[-1])
    #         listLogs()
    #         moreCheck()
    # elif (conf[0] == "c"):
    #     sys.exit()
    # else:
    #     print(":(")
    #     moreCheck()


def main():
    triage_args()

if __name__ == "__main__":
    splash_screen()
    print(Style.DIM + "-h [help], -l [list], -o [out], -e [edit], -t [new task], -v [view task]\n" + Style.RESET_ALL)
    main()