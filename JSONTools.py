"""
Used for various JSON messages that need to be sent back to the client after they make an api request.
Ruben Arellano
github.com/rarellano00
University of Utah
"""
import json


def create_rehearsal_reply(rehearsal_id, name, hostname):
    """
    Returns the ID of the rehearsal created.
    """
    reply = {
        "action": "rehearsalinfo",
        "rehearsalid": rehearsal_id,
        "name": name,
        "host": hostname
    }
    reply_json = json.dumps(reply)
    return reply_json


def join_rehearsal_reply(status, rehearsal, user_info_dict, personalidentifier):
    """
    Returns whether or not the joining of a rehearsal was successful.
    """
    if status == "fail":
        reply = {
            "action": "rehearsalinfo",
            "status": status
        }
        reply_json = json.dumps(reply)
        return reply_json
    else:
        reply = {
            "action": "rehearsalinfo",
            "status": status,
            "rehearsalid": rehearsal.id,
            "name": rehearsal.name,
            "host": rehearsal.hostname,
            "usercount": len(user_info_dict),
            "identifier": personalidentifier,
            "users": user_info_dict
        }
        reply_json = json.dumps(reply)
        return reply_json


def create_account_reply(status, fname, email):
    """
    Returns whether or not the creation of the account was successful.
    """
    if status == 'fail':
        reply = {
            "action": "createaccountreply",
            "status": status
        }
        reply_json = json.dumps(reply)
        return reply_json
    else:
        reply = {
            "action": "createaccountreply",
            "status": status,
            "fname": fname,
            "email": email
        }
        reply_json = json.dumps(reply)
        return reply_json


def close_rehearsal_reply(status, rehearsal_id):
    """
    Returns whether or not the closing of the rehearsal was successful.
    """
    reply = {
        "action": "closerehearsalreply",
        "status": status,
        "rehearsalid": rehearsal_id
    }
    reply_json = json.dumps(reply)
    return reply_json


def login_reply(status, request_dict, fname, lname, email):
    """
    Returns whether or not the login was successful as well as the users information.
    """
    if status == "success":
        reply = {
            "action": "loginreply",
            "status": status,
            "fname": fname,
            "lname": lname,
            "email": email
        }
        reply_json = json.dumps(reply)
        return reply_json
    else:
        reply = {
            "action": "loginreply",
            "status": status
        }
        reply_json = json.dumps(reply)
        return reply_json


def logout_reply(status, request_dict, email):
    """
    Returns whether or not the logout was successful.
    """
    reply = {
        "action": "logoutreply",
        "status": status,
        "email": email
    }
    reply_json = json.dumps(reply)
    return reply_json


def rehearsal_list_reply(rehearsals_list):
    """
    Puts the list of rehearsals into JSON format and returns the list.
    """
    rehearsal_dict = dict()
    for rehearsal in rehearsals_list:
        rehearsal_dict[rehearsal.id] = {
            "name": rehearsal.name,
            "hostname": rehearsal.hostname
        }

    reply = {
        "action": "rehearsallistreply",
        "rehearsals": rehearsal_dict
    }
    reply_json = json.dumps(reply)
    return reply_json


def user_list_reply(users_list):
    """
    Puts the list of users into JSON format and returns the list.
    """
    user_dict = dict()
    for user in users_list:
        user_dict[user.id] = {
            "fname": user.fname,
            "lname": user.lname,
            "email": user.email,
            "ip": user.ip,
            "port": user.port,
            "rehearsalid": user.rehearsal_id
        }

    reply = {
        "action": "userlistreply",
        "users": user_dict
    }
    reply_json = json.dumps(reply)
    return reply_json


def get_rehearsal_user_ips_reply(status, ips):
    """
    Puts the list of IPS into JSON format and returns them.
    """
    reply = {
        "action": "rehearsalipsreply",
        "status": status,
        "ips": ips
    }
    reply_json = json.dumps(reply)
    return reply_json


def request_port_reply(new_port):
    """
    Returns the new port number that has been assigned to the user.
    """
    reply = {
        "action": "requestportreply",
        "port": new_port
    }
    reply_json = json.dumps(reply)
    return reply_json
