import os
import logging as log
from math import floor
from random import Random
from flask import Flask, request, jsonify, Response


app = Flask(__name__)

if os.environ.get("SECRET_KEY") is not None:
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
else:
    app.config["SECRET_KEY"] = "key" + str(floor(Random().random() * 1_000_000))


stored_value = []


@app.route("/v1/shoppinglists/open", methods=["GET"])
def get_open_lists():
    if is_authenticated():
        global stored_value
        log.info("Got list request")
        return jsonify(stored_value)
    else:
        return Response(status=401)


@app.route("/v1/shoppinglists/open", methods=["POST"])
def post_open_lists():
    if is_authenticated():
        global stored_value
        stored_value = request.get_json()
        log.info("Stored value was updated!")
        return Response(status=201)
    else:
        return Response(status=401)


@app.route("/v1/system/ready", methods=["GET"])
def check_readiness():
    if is_authenticated():
        log.info("Readiness was checked")
        return Response("jARVIS is ready", status=200)
    else:
        return Response(status=401)


def get_credentials():
    username = os.environ.get("USERNAME", "default_user")
    password = os.environ.get("PASSWORD", "default_password")
    return username, password


def is_authenticated():
    (u_name, pw) = get_credentials()
    return request.authorization["username"] == u_name and pw == request.authorization["password"]


def main():
    log.basicConfig(level=log.INFO)
    app.run(debug=False)


if __name__ == '__main__':
    main()
