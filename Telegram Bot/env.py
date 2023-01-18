default_user_data = {
    'callsign': None,
    'convo_ids': [],
    'status': {
        # for members
        'initiated': False, 'action': False, 'report': False,
        # for admins
        'admin_menu': False,
        # for devs
        'backend': False
        },
    'group_id': None,
    'temp_data': {
        'settings': dict(),
        'convo': {
            'media_groups': []
        }
    },
    'telehandle': False
}


# TODO: Create an hourly garbage collector to clear afk peeps
default_bot_data = {
    'conversations': [], # TODO: convert this into a dictionary when we implement creating groups
    'active': {}, # key: user_id, value: conversation_id
    'queues': {
        'main': {} # in case we want to scale up different queues for different people
    },
    'telehandle': {
        'requested_for_telehandle': [],
        'requesting_for_telehandle': []
    }
}

# This is currently how I create the menu when i /help. TBH there could be a cleaner way to do this, i just
commands = {
    'sleep' : { # the default mode
        # 'events': 'shows the list of upcoming events',
        'patch_notes': 'Shows the patch notes of the last update',
        'info': 'Find out more about me and what I do!',
        'start': 'start a conversation with me :)',
        'part1': 'ONLY AVAILABLE FOR ADMINS',
        'backend': 'only for devs',
        'base_menu': ''
        },

    'started' : { # the mode activated after /start
        # 'events': 'shows the list of upcoming events',
        'patch_notes': 'Shows the patch notes of the last update',
        'info': 'Find out more about me and what I do!',
        'feedback': 'Use to enter feedback to the developers',
        'new_thread': 'Starts a new thread',
        'part1': 'FOR ADMINS ONLY',
        # 'admin_menu': 'Opens the menu of functions for admins',
        'end': 'ends the conversation with me :(',
        'base_menu': ''
        }
    }

######################3
# LIST OF EVENT CODES #
#######################

# FOR REPORTING/ FEEDBACK
REPORT, \
CATEGORY, \
MESSAGE = map(chr, range(50, 53))

# BASIC COMMANDS AT ALL POINTS

END, \
TIMEOUT = -1, -2

START, \
CANCEL, \
QUIT, \
INIT, \
COMPLETED, \
YES, \
NO, \
SELECT, \
INVALID, \
MENU = map(chr, range(10))
MATCH = 11
TELEHANDLE = 12
PASSWORD = 13
LOGIN = 14
DESCRIPTION_MENU = 15
CONTACT = 16
CONVERSATION_MENU = 17
NAME = 18
PAIR = 19
UNPAIR = 20
CONVO = 21
MENU1 = 22
BACK = 23
COURSE = 24
MATRICULATION_YEAR = 25
HOBBY = 26
REQUEST_TELEHANDLE = 27
LETTERS = 28
GAME = 29
# selection
USER, \
PERMS = map(chr, range(30, 32))
SHAREMENU = 33
IMYMENU = 34
WORDLEMENU = 35

# SPECIFIC COMMANDS:
FEEDBACK = chr(20)

# backend
BACKEND_URL = 'http://localhost:4200'

# owner
owner = 230527210