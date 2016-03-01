#!/usr/bin/env python
'''
To make random teams
'''

import random
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import getpass
import socket
from itertools import izip_longest
from players import PLAYERS # PLAYERS is a list of tuples (name, email).

PEOPLE_PER_GROUP = 4

def grouper(iterable, n_per_group, fillvalue=None):
    '''
    Makes groups of n elements per group
    '''

    args = [iter(iterable)] * n_per_group
    return izip_longest(*args, fillvalue=fillvalue)

def suffles_and_group(players):
    '''
    Shuffles the list of players and makes groups according to PEOPLE_PER_GROUP
    variable. If the number is odd then it uses as substitute.
    '''

    random.shuffle(players)

    # Remove one player if odd number of players and use it as substitute
    substitute = ""
    if len(players) % 2 != 0:
        substitute = players.pop()

    half = len(players) / 2
    teams = []
    for companion in zip(players[0:half], players[half:]):
        teams.append(' - '.join(companion))

    groups = grouper(teams, PEOPLE_PER_GROUP, '---')

    return groups, substitute

def send_email(sender, recipients, subject, body):
    '''
    Function to send emails.
    sender and recipients can be a list or a string.
    '''

    msg = MIMEText(body)
    msg['Subject'] = Header(subject) #for python 2.6  http://bugs.python.org/issue1974
    msg['From'] = sender 

    if type(recipients) is list:
        msg['To'] = ", ".join(recipients)

    if type(recipients) is str:
        msg['To'] = recipients

    server = smtplib.SMTP('localhost')
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()

def body_formater(groups, substitute):
    '''
    Transform the groups into a nice string.
    '''

    body = "Teams and groups for this week's championship:\n\n"
    for index, group in enumerate(groups):
        body += 'Group %d:\n' % (index + 1)
        body += '\n'.join(group)
        body += '\n\n'

    if substitute:
        body += 'Substitute player: %s\n' % substitute 

    body += '\n\nMay the force be with you...\n'

    return body

if __name__ == '__main__':

    fussballers = [x[0] for x in PLAYERS]
    teams, sub = suffles_and_group(fussballers)

    user = getpass.getuser()
    sender = user + '@ebi.ac.uk'
    recipients = [x[1] for x in PLAYERS]
    recipients =['eduardo@ebi.ac.uk']
    msg = body_formater(teams, sub)
    subject = 'Cron <%s@%s> Fussball: results of the draw -- %s' \
            % (user, socket.gethostname(), date.today().isoformat())
    send_email(sender, recipients, subject, msg)
