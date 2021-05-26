"""
Entry point for api requests that are then routed elsewhere.
Ruben Arellano
github.com/rarellano00
University of Utah
"""
from flask import Blueprint, request
import json
import RehearsalTools as rehtools
import AccountTools as acctools
import AdminTools as admntools

api = Blueprint('api', __name__)


@api.route('/api', methods=['POST'])
def reroute():
    """
    This reroutes the request to the appropriate class and function.
    """
    # grab the json request and follow the correct route
    request_dict = json.loads(request.data)
    action = request_dict['action']

    publicip = request.remote_addr
    request_dict["publicip"] = publicip
    if action == "createrehearsal":
        return rehtools.create_rehearsal(request_dict)
    elif action == "joinrehearsal":
        return rehtools.join_rehearsal(request_dict)
    elif action == "leaverehearsal":
        return rehtools.leave_rehearsal(request_dict)
    elif action == "closerehearsal":
        return rehtools.close_rehearsal(request_dict)
    elif action == "login":
        return acctools.login(request_dict)
    elif action == "logout":
        return acctools.logout(request_dict)
    elif action == "createaccount":
        return acctools.create_account(request_dict)
    elif action == "rehearsallist":
        return admntools.rehearsal_list(request_dict)
    elif action == "userlist":
        return admntools.user_list(request_dict)
    elif action == "rehearsalips":
        return admntools.get_rehearsal_user_ips(request_dict)
    elif action == "requestport":
        return acctools.get_free_port(request_dict)
    elif action == "test":
        return 'great test success'
    else:
        return 'api request not found'
