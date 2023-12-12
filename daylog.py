#!/usr/bin/env python3
import sys
import os
import time
import random
import readline
import argparse
import data.settings as daylog_settings
from datetime import datetime
from colorama import init as colorama_init, Fore, Style

colorama_init()

def splash_screen():
    possible_greetings = [
        'Hello bb ', 
        "It's time to get choppin'",
        "Welcome to Daylog",
        "Productive or not, it's logging time.",
        "How was your day?", 
        '* rat zone * ',
        'wikki wacci',
        'Ride on, cowboy'
    ]
    greeting_splash = possible_greetings[random.randint(0, len(possible_greetings) - 1)]
    left_side_frame = '|'
    right_side_frame = '|'
    top_bottom_frame = '='
    term_size = os.get_terminal_size()
    print('/ ' + (top_bottom_frame * (term_size.columns - 4)) + ' \\')
    for i in range(0,int((term_size.lines - 10) / 2)):
        print(left_side_frame + (' ' * (term_size.columns - 2)) + right_side_frame)
    print(left_side_frame + (' ' * int((term_size.columns / 2) - (len(greeting_splash) / 2) - 1)) + greeting_splash + (' ' * int((term_size.columns / 2) - (len(greeting_splash) / 2))) + right_side_frame)
    for i in range(0,int((term_size.lines - 10) / 2)):
        print(left_side_frame + (' ' * (term_size.columns - 2)) + right_side_frame)
    print('\\ ' + (top_bottom_frame * (term_size.columns - 4)) + ' /')

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
        new_task_item(args.task)
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

def new_task_list():
    global session_tasks
    session_tasks = []

def prompt_tasks(recursive_prompt=True):
    print(Fore.GREEN + Style.DIM + '\n--------')
    print('| Tasks')
    print('--------\n' + Style.RESET_ALL)
    def get_new_task():
        greeting = "\nWhatya wanna do?"
        print(greeting)
        task = input(">> " + Fore.GREEN)
        session_tasks.append(task)
        print(Style.RESET_ALL)
    while recursive_prompt == True:
        if recursive_prompt == True:
            confIn = input(Style.RESET_ALL + Fore.GREEN + "[task] New task? " +  Style.DIM + "\n(y [yes], n [no], u [undo task], l [list session], v [view tasks], a [move task to done], d [delete task], c[cancel] \n" + Style.RESET_ALL + ":: ")
            conf = confIn.lower()
            if conf == 'n':
                write_tasks(session_tasks)
                recursive_prompt = False
            if conf == 'l':
                list_tasks()
            if conf == 'v':
                view_tasks()
            if conf[0] == 'd':
                delete_task(conf)
            if conf[0] == 'u':
                undo_task(conf)
            if conf[0] == 'a':
                mark_task_done(conf)
            if conf == 'y':
                get_new_task()
            if conf == 'c':
                print('bye bye!')
                break

def new_task_item(argtask='',recursive_prompt = True):
    if argtask != '':
        session_tasks.append(argtask)
        print('\nadded task\n')
        argtask = ''

def write_tasks(tasks:list, file_operator='a'):
    current_time = get_current_time()
    user_paths = get_directories(current_time)
    with open(user_paths['task_file'], file_operator) as f:
        try:
            for i in tasks:
                f.write("%s\n" % i)
            print('\nTasks written: ' + user_paths['task_file'] + '\n')
        except:
            print("Error in path " + user_paths['task_file'])

def view_tasks():
    current_time = get_current_time()
    user_paths = get_directories(current_time)
    print('\n')
    print('\tTasks in file: \n')
    with open(user_paths['task_file'], "r") as f:
        count = 0
        try:
            while True:
                count += 1
                line = f.readline()
                if not line:
                    break
                print(Fore.GREEN + Style.BRIGHT + '\t' + '{} - {}'.format(count, line) + Style.RESET_ALL)
        except:
            print("Error in path " + user_paths['task_file'])
    print('\n')

def list_tasks():
    tasks_list = session_tasks
    print('\n')
    print('\tTasks in current list: (unwritten)')
    for i in tasks_list:
        print('\t' + Fore.GREEN + i + Style.RESET_ALL)
    print('\n')

def undo_task(i):
    tasks_list = session_tasks
    if i == "u":
        tasks_list.pop()
    else: 
        tasks_list.pop(int(i) - 1)

def delete_task(input):
    current_time = get_current_time()
    user_paths = get_directories(current_time)
    task_list = []
    input = input.strip()
    if len(input) >= 1:
        with open(user_paths['task_file'], "r") as f:
            count = 0
            while True:
                count += 1
                if count == int(input[1]):
                    line = f.readline()
                    print(Fore.RED + '\n\tDeleted ' + Style.BRIGHT + line + Style.NORMAL + ' from taskfile\n' + Style.RESET_ALL)
                else:
                    line = f.readline()
                    task_list.append(line.strip())
                if not line:
                    task_list = list(filter(None, task_list))
                    write_tasks(task_list, 'w')
                    break
    else:
        print('no arguments!')
        list_tasks()

def mark_task_done(input):
    current_time = get_current_time()
    user_paths = get_directories(current_time)
    selected_task = ''
    task_list = []
    if len(input) >= 1:
        with open(user_paths['task_file'], "r") as f:
            count = 0
            try:
                while True:
                    count += 1
                    if count == int(input[1]):
                        line = f.readline()
                        selected_task = line.strip()
                        print(Fore.GREEN + '\n\tMoved ' + Style.BRIGHT + selected_task + Style.NORMAL + ' to done list\n' + Style.RESET_ALL)
                    else:
                        line = f.readline()
                        task_list.append(line.strip())
                    if not line:
                        task_list = list(filter(None, task_list))
                        write_tasks(task_list, 'w')
                        break
            except:
                print("Error in path " + user_paths['task_file'])
        if selected_task != '':
            done.append(selected_task)
    else:
        print('no arguments!')
        list_tasks()

def interactive_prompt():
    valid_selections = ['y', 'n', 'u', 'l', 't', 'a', 'c', 'v']
    continue_prompt = True
    def get_conf():
        global direct_to_new_task
        conf = []
        if direct_to_new_task:
            conf.append('y')
            direct_to_new_task = False
        else:
            confIn = input(Style.RESET_ALL + "Have stuff? " + Style.DIM + "\n(y [yes], n [no], u [undo done], l [list done], t [tasks], v [view tasks], a [add task to done], c[cancel]) \n" + Style.RESET_ALL + ":: ")
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
            prompt_tasks()
        if conf[0] == 'a':
            mark_task_done(conf)
        if conf[0] == 'v':
            view_tasks()
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

def main():
    global direct_to_new_task
    direct_to_new_task = False 
    new_task_list()
    triage_args()

if __name__ == "__main__":
    splash_screen()
    print(Style.DIM + "-h [help], -l [list], -o [out], -e [edit], -t [new task], -v [view task]\n" + Style.RESET_ALL)
    main()
