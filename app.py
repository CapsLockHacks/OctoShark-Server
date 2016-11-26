import sys
import base64
import getpass
import os
#import paramiko

from flask import Flask, render_template, jsonify, request, abort
import subprocess
from digitalocean import SSHKey, Manager, Droplet


app = Flask(__name__)


@app.route('/login')
def login():
    if request.args.get('code') is None:
        abort(404)
    # Get from Chrome extension
    token = request.args.get('code')
    manager = Manager(token=token)

    # Instantiate ``api`` object to setup authentication for DO API.
    my_droplets = manager.get_all_droplets()
    # Check for success
    print(my_droplets)

    user_ssh_key = request.args.get('ssh')
    key = SSHKey(token='bb7f9e5b82a17b7304efde1b9cd886fc329f09340fa172c3c27d890b099c25cb',
                 name='uniquehostname',
                 public_key=user_ssh_key)
    # key is created succesfully.
    key.create()
    return "Login Success"

manager = Manager(token= 'bb7f9e5b82a17b7304efde1b9cd886fc329f09340fa172c3c27d890b099c25cb')


@app.route('/create')
def create():
	
	user = getpass.getuser()
	user_ssh_key = open('/home/{}/.ssh/id_rsa.pub'.format(user)).read()
    key = SSHKey(token='bb7f9e5b82a17b7304efde1b9cd886fc329f09340fa172c3c27d890b099c25cb',
                 name='uniquehostname',
                 public_key=user_ssh_key)
    key.create()
    print ("key stored in DO account")
    print (key.name)

    # Create Droplet
    keys = manager.get_all_sshkeys()

    droplet = Droplet(token=requests.args.get('token'),
                                   name=requests.args.get('name'),
                                   region=requests.args.get('region'), # Bangalore
                                   image='docker-16-04', # Docker
                                   size_slug='512mb',  # 512MB
                                   ssh_keys=keys, #Automatic conversion
                                   backups=False)
    droplet.create()
    return "DO Created"
'''
@app.run('/run')
def run():
    # Need SSH Key in req.args
    key = paramiko.RSAKey(data=base64.decodestring('AAA...'))
    client = paramiko.SSHClient()
    client.get_host_keys().add('ssh.example.com', 'ssh-rsa', key)
    client.connect('ssh.example.com', username='strongbad', password='thecheat')
    stdin, stdout, stderr = client.exec_command('ls')
    for line in stdout:
        print ('... ' + line.strip('\n'))
    client.close()
'''

@app.route('/')
def index():
    return 'Hello World'

def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    sys.exit(main())
