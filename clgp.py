import argparse
import getpass
import os
import subprocess
import textwrap
from shutil import which


def is_tool(name):
    """
    Check package in your system
    :param name: str
    :return: None
    """
    return which(name) is not None


def set_cmd(command=None):
    """
    Install git
    :return: None
    """
    if command is None:
        command = ['apt-get', 'install', 'git']
    sudo_pass = getpass.getpass('This needs administrator privileges: ')

    proc = subprocess.Popen(['sudo', '-kS'] + command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    o, e = proc.communicate(input=sudo_pass + '\n')
    if proc.returncode:
        print('command failed')
    else:
        print('success')
    print(o)
    print(e)


def get_remote_origin():
    """
    Run console command "git config --list" and selects a link 'origin' from the list
    :return: str
    """
    out = subprocess.getoutput('git config --list')
    for url in out.split('\n'):
        if url.startswith("remote.origin.url"):
            return url.split('=')[1]
    return False


def set_remote_origin(remote_repo):
    command = ['git', 'remote', 'add', 'origin', remote_repo]
    set_cmd(command)


def is_git_repository(l_repo):
    """
    checks if this directory exists
    is there a git repository in this directory
    :param l_repo:
    :return: None
    """
    if os.path.isdir(l_repo):
        print(f"path to local repository found ==> {l_repo}")
        if subprocess.call(["git", "branch"], stderr=subprocess.STDOUT, stdout=open(os.devnull, 'w')) != 0:
            print("Not found git repository")
            return False
        else:
            print("local repository found")
            return True
    else:
        print(f"path to local git repository {l_repo} not dir")


if __name__ == '__main__':
    # Example command: python clpg.py
    # -p "~/home/src/example"
    # -r "https://github.com/user/example.git"
    # -c "--global http.proxy http://proxyUsername:proxyPassword@proxy.server.com:port"

    parser = argparse.ArgumentParser(prog='C.L.G.P.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''
                                     Command Line Git Pull
                                     ----------------------
                                     Checks for git in the system
                                     if necessary establishes and execute pull
                                     to learn more see -h or --help
                                     '''))
    parser.add_argument('-p', dest='local_repo', default=os.getcwd(), type=str, required=False)
    parser.add_argument('-r', dest='remote_repo', type=str, required=False)
    parser.add_argument('-proxy', dest='http_proxy', type=str, required=False)
    parser.add_argument('-debug', '--debug', action='store_true')

    args = parser.parse_args()
    while True:
        if is_tool("git"):
            if is_git_repository(args.local_repo):
                if args.remote_repo:
                    set_remote_origin(args.remote_repo)
                    cmd = ['git', 'pull', args.remote_repo, args.http_proxy]
                    set_cmd(cmd)
                    break
                else:
                    remote_url = get_remote_origin()
                    if remote_url is False:
                        print("not found remote repository")
                        break
                    cmd = ['git', 'pull', remote_url, args.http_proxy]
                    set_cmd(cmd)
                    break
            else:
                answ = input("init git? Y/N\n")
                if answ.lower() == "y":
                    set_cmd(['git', 'init'])
                    continue
                else:
                    break
        else:
            print("==============ERROR=================\n"
                  "no git was found in the system,\n"
                  "install it yourself or \n"
                  "run a program with elevated privileges\n"
                  "for automatic installation\n"
                  "=====================================")
            answ = input("install git?\n[Y]es/[N]o\n")
            if answ.lower() == "y":
                set_cmd()
                continue
            else:
                break
