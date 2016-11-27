import sys
import base64
import getpass
import os
from threading import Thread

import paramiko
from flask import Flask, render_template, jsonify, request, abort
from flask.ext.cors import CORS, cross_origin

from digitalocean import SSHKey, Manager, Droplet
import requests

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/login')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
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
repo_url = 'https://github.com/CapsLockHacks/dockerfile_test'
manager = Manager(token=token)


@app.route('/create')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
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
	print ("key stored in Digital Ocean account")
	print (key.name)

	# Create Droplet
	# get all ssh keys stored in the digitalocean account
	keys = manager.get_all_sshkeys()

	droplet = Droplet(token='bb7f9e5b82a17b7304efde1b9cd886fc329f09340fa172c3c27d890b099c25cb',
								name='dockerhelloworld',
								region='blr1', # Bangalore
								image='docker-16-04', # Docker
								size_slug='512mb',  # '512mb'
								ssh_keys=keys, #Automatic conversion
								backups=False)


	# from chrome extension
	# repo_url = request.args.get['repo_url']
	# droplet = Droplet(token=request.args.get['token'],
	# 					name=request.args.get['name'],
	# 					region=request.args.get['region'],
	# 					image='docker-16-04',
	# 					size_slug=request.args.get['size'],
	# 					ssh_keys=keys,
	# 					backups=False)

	droplet.create()
	
	thread = Thread(target=commandrun, args=[droplet])
	return ("DO Created & ssh tested")

def commandrun(droplet):

	# get IP address using droplet.id
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
	stdin, stdout, stderr = client.exec_command('git clone {}'.format(repo_url))
	repo_name =  repo_url.split('/') 
	repo_name = repo_name[4].split('.')[0]

	print ('clone sucessful')
	


	# stdin, stdout, stderr = client.exec_command('docker run -d -p 80:5000 training/webapp python app.py')
	# for line in stdout:
	# 	print ('... ' + line.strip('\n'))

	# stdin, stdout, stderr = client.exec_command('docker ps')
	# for line in stdout:
	# 	print ('... ' + line.strip('\n'))
	
	# do all 3 commands in one line
	print ('going into {}'.format(repo_name))
	stdin, stdout, stderr = client.exec_command('cd {};pwd;docker build -t octoshark . ;'.format(repo_name))

	print ('stdout of the following')
	for line in stdout:
		print ('... ' + line.strip('\n'))

	if('webapp' in repo_name):
		stdin, stdout, stderr = client.exec_command('cd {};pwd;docker run -d -P octoshark;'.format(repo_name))

	print ('closing client ssh client')
	client.close()
	print ('ssh client closed')
	return "Success"


@app.route('/')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def index():
	return 'Hello, cross-origin-world!'

def main():
	port = int(os.environ.get('PORT',5000))
	app.run(host="0.0.0.0", port = port, debug=True)


if __name__ == '__main__':
	sys.exit(main())


"""
139.59.28.189
stdin, stdout, stderr = client.exec_command('cd {}; ls'.format(repo_name))
cmds = ['cd {}'.format(repo_name); 'docker build -t "{}" .'.format('octocat'); 'docker run {}'.format('octocat')]
"""