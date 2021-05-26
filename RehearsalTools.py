"""
Used for any sort of rehearsal requests and rehearsal management.
Ruben Arellano
github.com/rarellano00
University of Utah
"""
from project.models import User, Rehearsal
from project import db
import JSONTools
import bcrypt
import string
import random


def create_rehearsal(request_dict):
    """
    Creates a rehearsal with the given name and host.
    """
    # grab the request information and make a new rehearsal
    rehearsal_name = request_dict['rehearsalname']
    host_name = request_dict['hostname']
    password = request_dict['password']

    hash_and_salt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    new_rehearsal = Rehearsal(name=rehearsal_name, hostname=host_name, active=True,
                              password=hash_and_salt)
    db.session.add(new_rehearsal)
    db.session.commit()

    return JSONTools.create_rehearsal_reply(new_rehearsal.id, new_rehearsal.name, new_rehearsal.hostname)


def generate_random_identifier():
    """
    Generates 15 random characters and returns them as a string. Logic is independent of database and the string
    may need to be checked in the future.
    """
    letters = string.ascii_letters
    ret_string = ''.join(random.choice(letters) for i in range(15))
    return ret_string


def join_rehearsal(request_dict):
    """
    Puts a user into the requested rehearsal.
    """
    rehearsal_id = request_dict['rehearsalid']
    password = request_dict['password']
    email = request_dict['email']
    publicip = request_dict['publicip']

    # grab rehearsal and check if the credentials match up
    rehearsal = Rehearsal.query.filter_by(id=rehearsal_id).first()
    status = 'success'
    if not rehearsal or not rehearsal.active or not bcrypt.checkpw(password.encode(), rehearsal.password):
        status = 'fail'
        return JSONTools.join_rehearsal_reply(status=status, rehearsal=None,
                                              user_info_dict=None, personalidentifier=None)

    user = User.query.filter_by(email=email).first()
    user.publicip = publicip

    # on login custom identifier should be blank so if they haven't been a part of a room before give a new identifier
    # NOTE: should probably shift towards using a separate action for requesting users in room
    if user.customidentifier == "" or None:
        rand_string = generate_random_identifier()
        user.customidentifier = rand_string

    # make sure the ip gets updated
    db.session.add(user)
    # credentials matched up so add user to the rehearsal and return the reply
    rehearsal.users.append(user)
    db.session.commit()
    # generate a dictionary of all the people in the rehearsal
    users = rehearsal.users
    user_info_dict = dict()
    for reh_user in users:
        # make sure we are using private ip if two users share the same ip
        reh_user_ip = reh_user.publicip
        if reh_user_ip == user.publicip:
            reh_user_ip = reh_user.privateip

        user_info_dict[reh_user.id] = {
            "name": reh_user.fname + ' ' + reh_user.lname,
            "ip": reh_user_ip,
            "port": reh_user.port,
            "identifier": reh_user.customidentifier
        }

    return JSONTools.join_rehearsal_reply(status, rehearsal, user_info_dict, user.customidentifier)


def leave_rehearsal(request_dict):
    """
    Removes a user from the rehearsal they are a part of.
    """
    user = User.query.filter_by(email=request_dict['email']).first()

    if not user:
        return 'not great success'

    # remove any sort of connection between the user and the rehearsal
    user.customidentifier = ""
    user.rehearsal_id = None
    db.session.add(user)
    db.session.commit()

    # just return nothing (that is what the protocol states)
    return 'great success'


def close_rehearsal(request_dict):
    """
    Sets the requested rehearsal to inactive.
    """
    status = "success"
    rehearsal_id = request_dict['rehearsalid']

    rehearsal = Rehearsal.query.filter_by(id=rehearsal_id).first()
    if not rehearsal:
        status = "fail"
        JSONTools.close_rehearsal_reply(status, rehearsal_id)

    rehearsal.active = False
    db.session.commit()

    return JSONTools.close_rehearsal_reply(status, rehearsal_id)
