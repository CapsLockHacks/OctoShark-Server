import sys
from flask import Flask, render_template, jsonify, request, abort
import subprocess
from digitalocean import SSHKey, Manager, Droplet


app = Flask(__name__)


@app.route('/login')
def login():
    if request.args.get('token') is None and request.args.get('ssh') is None:
        abort(404)
    # Get from Chrome extension
    token = request.args.get('token')
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

    # Create Droplet
    keys = manager.get_all_sshkeys()

    droplet = Droplet(token="bb7f9e5b82a17b7304efde1b9cd886fc329f09340fa172c3c27d890b099c25cb",
                                   name='DropletWithSSHKeys',
                                   region='blr1', # Bangalore
                                   image='docker-16-04', # Docker
                                   size_slug='512mb',  # 512MB
                                   ssh_keys=keys, #Automatic conversion
                                   backups=False)
    droplet.create()
    return "DO Created"


@app.route('/')
def index():
    return 'Hello World'

def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    sys.exit(main())