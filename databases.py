from subprocess import Popen, PIPE, check_output
from sys import argv
import getpass

def main():

    directive = argv[1]

    if directive == 'stop':
        check_output(['docker', 'rm', '-f', 'mysql'])
        check_output(['brew', 'services', 'stop', 'mongodb-community@4.2'])
    elif directive == 'start':
        p = getpass.getpass(prompt='password: ')
        check_output(['docker', 'run', '--name=mysql', '-d', '-e', 'MYSQL_ROOT_PASSWORD=' + p, 'mysql/mysql-server:5.7.17'])
        check_output(['brew', 'services', 'start', 'mongodb-community@4.2'])

if __name__ == "__main__":
        main()
