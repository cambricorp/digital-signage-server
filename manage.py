'''
Created on Mar 28, 2014

@author: Hugo Lima (https://github.com/hmiguellima)
'''

import sys, subprocess
from cork import Cork

aaa = Cork('etc', email_sender='noreply@codebits.eu', smtp_server='127.0.0.1')

def restart_bottle():
    subprocess.call(["touch", "app.py"])

def add_user():
    if len(sys.argv) != 4:
        invalid_params()

    username = sys.argv[2]
    password = sys.argv[3]

    if username in aaa._store.users:
        print 'user already created'
        exit(1)

    aaa._store.users[username] = {
        'role': 'admin',
        'hash': aaa._hash(username, password),
        'email_addr': None,
        'desc': 'Admin user',
        'creation_date': None,
        'last_login': None
    }

    aaa._store.save_users()
    restart_bottle()

    print 'user created!'

def delete_user():
    if len(sys.argv) != 3:
        invalid_params()

    username = sys.argv[2]

    if not username in aaa._store.users:
        print 'user doesn\'t exist'
        exit(1)

    del aaa._store.users[username]

    aaa._store.save_users()
    restart_bottle()

    print 'user deleted!'

def change_password():
    if len(sys.argv) != 4:
        invalid_params()

    username = sys.argv[2]
    password = sys.argv[3]

    if not username in aaa._store.users:
        print 'user doesn\'t exist'
        exit(1)

    aaa._store.users[username]['hash'] = aaa._hash(username, password)

    aaa._store.save_users()
    restart_bottle()

    print 'user password changed!'

def invalid_params():
    print 'Invalid arguments:\n'
    print 'Syntax: manage.py <command> <args>\n'
    print 'Valid commands:\n'
    print '  add-user <username> <password>'
    print '  delete-user <username>'
    print '  change-password <username> <password>'

    exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        invalid_params()

    command = sys.argv[1]

    commands = {
      'add-user': add_user,
      'delete-user': delete_user,
      'change-password': change_password
    }

    if command not in commands.keys():
        invalid_params()

    commands[command]()
