bot_init = 'Energise!'
daily = 'Yo sup today is a good day'
# start = f"""Welcome {update.message.from_user.username}!
# Select:
# 1. description_menu to fill up your personal details.
# 2. conversation_menu to start talking to someone.
# """

admin_menu = """Welcome Admin {username}! What would you like to do today?

{}"""

# when a user initialises the bot for the first time
# first_start = """Hello {username} This must be your first time here.
#
# Looks like this is your first time here. Do head over to /description_menu to fill up your personal details first before starting a conversation!
#
# Select:
# 1. description_menu to fill up your personal details.
# 2. conversation_menu to start talking to someone."""

first_start = """ Hello {username}. Looks like you are bored huh?

What do you wanna do this time?

Select:
1. /Share - I want you to know something about me
2. /Bored - Entertain me now!
3. /Sad - I wanna be my happy...
4. /IMY - Only if you miss me pls
5. /Wordle - Self - explanatory"""

start = """Welcome {username}!
Select:
1. description_menu to fill up your personal details.
2. conversation_menu to start talking to someone."""

timeout="Sorry sir/ma\'am, this session has automatically been ended. \
Goodbye..."

end = 'Goodbye! Do /start to use the bot again next time!'

conv_ended = "The conversation has ended"

end_list = ['Going so soon.... Alright... Bye then...',\
    'Cheerio',\
    'Have nice day',\
    'Thank you for your time. Goodbye',\
    'k thx bai'
    ]

quit_msg = 'Going back to start menu'

# TODO: What is displayed when asked for the info of the bot
BOT_DESCRIPTION = ''