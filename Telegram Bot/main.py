'''
This script compiles the requirements for the bot and runs it on a loop
It should also contain the functions of the bot
'''

from env import *
from core import *
import utils
import messages
import telegram
import datetime
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
ConversationHandler, CallbackQueryHandler
import logging
from pytz import timezone
import argparse
import configparser
import logging

def cli():
    parser = argparse.ArgumentParser(description='Runs the leobot service')
    parser.add_argument('-t', '--testing', type=bool, help='Whether you want to run in testing env')
    parser.add_argument('-d', '--debug', type=bool, help='Whether you want to run in debug mode')
    args = parser.parse_args()
    return args

def get_log_level(args):
    if args.debug:
        return logging.DEBUG
    return logging.INFO

def get_bot_cfg(args):
    config = configparser.ConfigParser()
    config.read('bot.cfg')
    if args.testing:
        msg = 'Running on testing environment'
        bot_config = config['test_bot']
    else:
        msg = 'Running on live environment'
        bot_config = config['live_bot']
    
    # print messages
    logging.debug(msg)
    if args.debug:
        print(msg)

    return config, bot_config

print('initialising')
args = cli()

config, bot_config = get_bot_cfg(args) 

updater = Updater(token=bot_config['token'], use_context=True)
dispatcher = updater.dispatcher # for quicker access to the dispatcher object
jobqueuer = updater.job_queue # for quicker access to JobQueue object
utils.core.set_default_bot_data(dispatcher, default_bot_data)
utils.core.set_user_data_to_default(dispatcher, default_user_data)


description_menu = ConversationHandler(
    entry_points=[CommandHandler('description_menu', description_menu)],
    states={
        #additional questions here
        MENU: [CommandHandler('course', menu),
               CommandHandler('matriculation_year', menu),
               CommandHandler('hobby', menu),
               MessageHandler(Filters.text & ~Filters.command, show_details)
            ],
        #NAME: [MessageHandler(Filters.text, name)],
        #CONTACT: [MessageHandler(Filters.text, contact)],
        COURSE: [MessageHandler(Filters.text & ~Filters.command, course)],
        MATRICULATION_YEAR: [MessageHandler(Filters.text & ~Filters.command, matriculation_year)],
        HOBBY: [MessageHandler(Filters.text & ~Filters.command, hobby)]
    },
    fallbacks = [CommandHandler('quit', back),
                 CommandHandler('end', end)],
    map_to_parent={
        BACK: MENU,
        END: END
    },
)

conversation_menu = ConversationHandler(
    entry_points=[CommandHandler('conversation_menu', conversation_menu)],
    states={
        MENU: [CommandHandler('Convo_with_Enhui_Jr', convo_with_enhui),
            CommandHandler('pair',pair),
            CommandHandler('unpair', unpair),
            CommandHandler('request_telehandle', request_telehandle),
            CommandHandler('share_telehandle', share_telehandle),
            utils.core.FileHandler(forward_text)
                #add more command handlers here next time
                ],
        REQUEST_TELEHANDLE: [MessageHandler(Filters.text & ~Filters.command, request_telehandle)],
    },
    fallbacks = [CommandHandler('quit', back),
                 CommandHandler('end', end)],
    map_to_parent={
        BACK: MENU,
        END: END
    },
)


start_menu = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={ 
        MENU: [CommandHandler('Bored', bored_menu),
               CommandHandler('Sad', sad_menu),
               MessageHandler(Filters.command, handle_menu)
               ],
        SHAREMENU: [MessageHandler(Filters.text & ~Filters.command, sharing_things)],
        IMYMENU: [MessageHandler(Filters.text & ~Filters.command, imy_free_dates)],
        WORDLEMENU: [CommandHandler('play_again', wordle_play_again)],
        LETTERS: [MessageHandler(Filters.text & ~Filters.command, wordle_letters)],
        GAME: [MessageHandler(Filters.text & ~Filters.command, wordle_main),
               CommandHandler('play_again', wordle_play_again)],

        END: [CommandHandler('start', start)],
    },
    fallbacks= [CommandHandler('back', back_menu),
                CommandHandler('end', end)]
)

dispatcher.add_handler(start_menu)

updater.start_polling()