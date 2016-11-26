import sys
from flask import Flask, render_template, jsonify, request

from digitalocean import SSHKey, Manager

app = Flask(__name__)
manager = digitalocean.Manager(token="24611cca29682d3d54f8208b67a47dbe8b6ea01b2c8103ba61150ece4b6259b6")
my_droplets = manager.get_all_droplets()
# Check for success
print(my_droplets)


# Get from Chrome extension
user_ssh_key = ''
key = SSHKey(token='secretspecialuniquesnowflake',
             name='uniquehostname',
             public_key=user_ssh_key)
# key is created succesfully.
key.create()



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


# Instantiate ``api`` object to setup authentication for DO API.

@app.route('/')
def index():
    return 'Hello World'

def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    sys.exit(main())