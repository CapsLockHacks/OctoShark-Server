import sys
from flask import Flask, render_template, jsonify, request


app = Flask(__name__)

# Instantiate ``api`` object to setup authentication for DO API.

@app.route('/')
def index():
    return 'Hello World'

def main():
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    sys.exit(main())