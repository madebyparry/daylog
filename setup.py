import os
import pickle

user_paths = dict(
    daylog_root = '',
    log_directory = '/logs',
    data_directory = '/data',
    task_directory = '/logs',
    task_file = '/taskfile.log',
    err_file = '/logs/err',
)
user_colors = dict(
        color_primary = '',
        color_secondary = '',
        color_accent = '',
        color_contrast = '',
        color_muted = '',        
)

def confirm_folder(user_paths):
    default_dir = os.path.dirname(os.path.realpath(__file__))
    print('Setup default directories?')
    user_in = input(default_dir + ' - (y, n) >> ')    
    if user_in == 'y':
        user_paths['daylog_root'] = default_dir
        settings_alter(user_paths)
    else:
        user_paths = set_all_directories()
        settings_alter(user_paths)

def settings_alter(user_paths):
    # sed_cmd = "sed -i 's#%REPLACE1%#" + daylog_dir + "#' " + daylog_dir + '/data/settings.py'
    settings_file_path = user_paths['daylog_root'] + user_paths['data_directory'] + '/settings.py'
    with open(settings_file_path, 'w') as settings_f:
        print('user_paths = ', file=settings_f, end='')
        print(user_paths, file=settings_f)
        print('user_colors = ', file=settings_f, end='')
        print(user_colors, file=settings_f)
        # settings_f.write(user_paths)
        # settings_f.write(user_colors)
        # pickle.dump(user_paths,settings_f)
        # pickle.dump(user_colors, settings_f)
    print('\nrewriting settings.py\n')
    # os.system(sed_cmd)

def set_daylog_dir():
    daylog_dir = input('What dir would you like to set as your daylog root? (+/logs)')
    return daylog_dir

def set_all_directories():
    for i in user_paths:
        i = input('What address would you like to set as your ' + i + '? (no trailing slash) \n>> ')
        print(i)
    return user_paths
    # user_paths['daylog_root'] = input('What dir would you like to set as your daylog root? (+/logs)')


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
    confirm_folder(user_paths)
    getDeps()

main()