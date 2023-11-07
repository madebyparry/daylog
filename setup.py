import os


def confirm_folder():
    daylog_dir = os.path.dirname(os.path.realpath(__file__))
    log_directory = daylog_dir + '/logs'
    print('how does the directory look to store your logs?')
    user_in = input(log_directory + ' - (y, n) >> ')    
    if user_in == 'y':
        settings_alter(daylog_dir)
    else:
        daylog_dir = set_daylog_dir()
        settings_alter(daylog_dir)

def settings_alter(daylog_dir):
    sed_cmd = "sed -i 's#%REPLACE1%#" + daylog_dir + "#' " + daylog_dir + '/data/settings.py'
    print('\nrewriting settings.py\n')
    os.system(sed_cmd)

def set_daylog_dir():
    daylog_dir = input('What dir would you like to set as your daylog root? (+/logs)')
    return daylog_dir

def getDeps():
    lib_folder = os.path.dirname(os.path.realpath(__file__))
    requirement_path = lib_folder + '/requirements.txt'
    os.system('pip install -r '  + requirement_path)
    # install_requires = [] 
    # if os.path.isfile(requirement_path):
    #     with open(requirement_path) as f:
    #         install_requires = f.read().splitlines()
    # setup(install_requires=install_requires)

def main():
    confirm_folder()
    getDeps()

main()