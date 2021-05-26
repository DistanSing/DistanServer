"""
Used for various database access and information gathering for the p2p connections.
Ruben Arellano
github.com/rarellano00
University of Utah
"""
from project.models import User, Rehearsal
import JSONTools


def rehearsal_list(request_dict):
    """
    Returns a list of all of the current rehearsals.
    """
    rehearsals = Rehearsal.query.all()
    rehearsals_list = list()
    for rehearsal in rehearsals:
        rehearsals_list.append(rehearsal)

    return JSONTools.rehearsal_list_reply(rehearsals_list)


def user_list(request_dict):
    """
    Returns a list of all of the current users.
    """
    users = User.query.all()
    users_list = list()
    for user in users:
        users_list.append(user)

    return JSONTools.user_list_reply(users_list)


def get_rehearsal_user_ips(request_dict):
    """
    Returns the user ips in a given rehearsal.
    """
    rehearsal_id = request_dict['rehearsalid']
    rehearsal = Rehearsal.query.filter_by(id=rehearsal_id).first()
    status = "success"
    if not rehearsal:
        status = "fail"
        return JSONTools.get_rehearsal_user_ips_reply(status, None)

    ips = list()

    for user in rehearsal.users:
        ips.append(user.ip)

    return JSONTools.get_rehearsal_user_ips_reply(status, ips)
