from subprocess import Popen, PIPE, check_output
from sys import argv

def main():

    directive = argv[1]

    if directive == 'stop':
        check_output(['docker', 'rm', '-f', 'mysql'])
    elif directive == 'start':
        check_output(['docker', 'run', '-d', '--name=mysql', '-p', '3306:3306', localhost])
