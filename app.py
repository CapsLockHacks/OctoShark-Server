import sys
import base64
import getpass
import os

import paramiko
from flask import Flask, render_template, jsonify, request, abort
import subprocess
from digitalocean import SSHKey, Manager, Droplet
import requests

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

token = 'bb7f9e5b82a17b7304efde1b9cd886fc329f09340fa172c3c27d890b099c25cb'
manager = Manager(token=token)

@app.route('/create')
def create():
	
	user = getpass.getuser()
	user_ssh_key = open('/home/{}/.ssh/id_rsa.pub'.format(user)).read()
	key = SSHKey(token='bb7f9e5b82a17b7304efde1b9cd886fc329f09340fa172c3c27d890b099c25cb',
				 name='uniquehostname',
				 public_key=user_ssh_key)

	try:
		key.create()
	except:
		pass
	print ("key stored in DO account")
	print (key.name)

	# Create Droplet
	keys = manager.get_all_sshkeys()

	droplet = Droplet(token='bb7f9e5b82a17b7304efde1b9cd886fc329f09340fa172c3c27d890b099c25cb',
								name='testssh',
								region='blr1', # Bangalore
								image='docker-16-04', # Docker
								size_slug='512mb',  # '512mb'
								ssh_keys=keys, #Automatic conversion
								backups=False)
	droplet.create()
	
	response = requests.get('https://api.digitalocean.com/v2/droplets/'+str(droplet.id), 
		headers={'Authorization': 'Bearer {}'.format(token)})
	droplet_ip = response.json()['droplet']['networks']['v4'][0]['ip_address']
	print ("droplet ip {}".format(droplet_ip))
	
	# get user's ssh key
	user_ssh_key = '/home/{}/.ssh/id_rsa.pub'.format(getpass.getuser())
	
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   
	client.connect(droplet_ip, username='root', key_filename=user_ssh_key)

	# running test command	
	# stdin, stdout, stderr = client.exec_command('ls')
	# print ('running ls command on droplet')
	# for line in stdout:
	# 	print ('... ' + line.strip('\n'))
	# print ('mission complete')

	# run docker
	repo_url = ''
	stdin, stdout, stderr = client.exec_command('git clone {}'.format(repo_url))
	repo_name =  repo_url.split('/') 
	repo_name = repo_name[4].split('.')[0]
	# do all 3 commands in one line
	stdin, stdout, stderr = client.exec_command('cd {};pwd;docker build -t "octoshark" .;docker run octoshark;'.format(repo_name))

	# print stdout of the following
	for line in stdout:
		print ('... ' + line.strip('\n'))

	client.close()

	return "DO Created & ssh tested"

@app.

@app.route('/')
def index():
	return 'Hello World'

def main():
	port = int(os.environ.get('PORT',5000))
	app.run(host="0.0.0.0", port = port, debug=True)


if __name__ == '__main__':
	sys.exit(main())



stdin, stdout, stderr = client.exec_command('cd {}; ls'.format(repo_name))
cmds = ['cd {}'.format(repo_name); 'docker build -t "{}" .'.format('octocat'); 'docker run {}'.format('octocat')]