"""
Used for various account actions and authorization.
Ruben Arellano
github.com/rarellano00
University of Utah
"""
from project.models import User, Rehearsal
from project import db
import JSONTools
import bcrypt
import random


def create_account(request_dict):
    """
    Creates an account with the given information from the user.
    """
    fname = request_dict['fname']
    lname = request_dict['lname']
    email = request_dict['email']
    password = request_dict['password']
    publicip = request_dict["publicip"]
    privateip = request_dict['ip']
    # port = request_dict['port']

    # first we need to check if a user already exists with the email, if  they do return a fail message
    user = User.query.filter_by(email=email).first()
    if user:
        # let the user know an account exists with those credentials
        return JSONTools.create_account_reply(status='fail', fname=None, email=None)

    # user has a valid email so make an account and send the success reply
    new_user = User(email=email, fname=fname, lname=lname, publicip=publicip, privateip=privateip, customidentifier="",
                    password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
    db.session.add(new_user)
    db.session.commit()

    return JSONTools.create_account_reply(status='success', fname=fname, email=email)


def login(request_dict):
    """
    Logs the user in as well as updates any IP and PORT information.
    """
    status = "success"
    email = request_dict['email']
    password = request_dict['password']
    privateip = request_dict['ip']
    publicip = request_dict['publicip']
    # port = request_dict['port']

    user = User.query.filter_by(email=email).first()

    # checks to see if the credentials are valid, if not gets sent through the "fail" route
    if not user or not bcrypt.checkpw(password.encode(), user.password):
        status = "fail"
        return JSONTools.login_reply(status, request_dict, None, None, None)

    found_fname = user.fname
    found_lname = user.lname
    # update ip and port information
    user.publicip = publicip
    user.privateip = privateip
    user.customidentifier = ""
    db.session.add(user)
    db.session.commit()

    return JSONTools.login_reply(status, request_dict, found_fname, found_lname, email)


def logout(request_dict):
    """
    Logs the user out as well as invalidates any IP and PORT information.
    """
    status = "success"
    email = request_dict['email']

    # invalidate ip and port since logging out
    user = User.query.filter_by(email=email).first()
    user.privateip = 0
    user.publicip = 0
    user.port = 0
    db.session.add(user)
    db.session.commit()

    return JSONTools.logout_reply(status, request_dict, email)


def get_free_port(request_dict):
    """
    Looks through the given rehearsal and returns a port that is not already used.
    """
    rehearsalid = request_dict['rehearsalid']
    email = request_dict['email']
    user = User.query.filter_by(email=email).first()
    rehearsal = Rehearsal.query.filter_by(id=rehearsalid).first()
    users = rehearsal.users

    # make sure port is not already in use in the room
    new_port = random.randint(30000, 31000)
    while True:
        for reh_user in users:
            if new_port == reh_user.port:
                new_port = random.randint(30000, 31000)
                break
        break

    # update port and return json
    user.port = new_port
    db.session.add(user)
    db.session.commit()

    return JSONTools.request_port_reply(new_port)
