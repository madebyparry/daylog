#!/usr/bin/env python3
import os

def getShell():
    shell = input("Are you using a fish shell? (y, n) >> ")
    if shell == "y":
        fishInstall()
    else:
        bashInstall()

def fishInstall():
    homeRoot = os.path.expanduser('~')
    dl_path = os.path.dirname(os.path.realpath("./")) + '/daylog/daylog/daylog.py'
    fish_path = homeRoot + "/.config/fish/functions/daylog.fish"
    def installOnFish():
        fish_write = '''function daylog
{dir} $argv
end'''.format(dir = dl_path)
        with open(fish_path, "a") as f:
            try:
                f.write(fish_write)
                print("daylog installed on fish")
            except: 
                print("Error in writing to " + fish_path)

    if os.path.getsize(fish_path) == 0: 
       installOnFish()
    else:
        os.remove(fish_path)
        installOnFish()

def bashInstall():
    homeRoot = os.path.expanduser('~')
    rc = homeRoot + "/.bashrc"
    dl_path = os.path.dirname(os.path.realpath("./")) + '/daylog/daylog/daylog.py'
    bash_alias = "alias daylog='" + dl_path + "'"
    def installOnBash():
        try:
            with open(rc, "a") as f:
                f.write("\n" + bash_alias)
                print("daylog installed on bash")
        except: 
            print("Error in writing to .bashrc")
    with open(rc) as f:
        if bash_alias in f.read():
            print("already installed on bash")
        else:
            installOnBash()

def getDeps():
    lib_folder = os.path.dirname(os.path.realpath(__file__))
    requirement_path = lib_folder + '/requirements.txt'
    os.system('pip install -r '  + requirement_path)
    # install_requires = [] 
    # if os.path.isfile(requirement_path):
    #     with open(requirement_path) as f:
    #         install_requires = f.read().splitlines()
    # setup(install_requires=install_requires)

getShell()
getDeps()
