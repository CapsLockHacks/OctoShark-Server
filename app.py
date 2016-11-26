import sys
from flask import Flask, render_template, jsonify, request, abort
import subprocess
from digitalocean import SSHKey, Manager


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
    key = SSHKey(token='secretspecialuniquesnowflake',
                 name='uniquehostname',
                 public_key=user_ssh_key)
    # key is created succesfully.
    key.create()
    return "Login Success"

@app.route('/create')
def create():

    # Create Droplet
    keys = manager.get_all_sshkeys()

    droplet = digitalocean.Droplet(token="secretspecialuniquesnowflake",
                                   name='DropletWithSSHKeys',
                                   region='ams3', # Amster
                                   image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
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