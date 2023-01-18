from telegram.message import Message
from env import BACKEND_URL
from os import remove
#import requests
import utils.logic as logic
from telegram.ext import Filters, MessageHandler
import logging
from collections import defaultdict
import telegram
import datetime
import time
from functools import wraps
import messages as msgs
import re

# quick send owners
def inform_owners(msg, context):
    owner = context.bot_data['owner']
    context.bot.send_message(owner, str(msg))

def bot_print(update, text):
    '''
    replies a certain msg to the sender
    #! USUALLY FOR DEBUGGING
    '''
    if type(text) != str:
        text = str(text)
    update.message.reply_text(text=text)

def clean_msg(msg):
    '''
    Checks the message for formatting issues that are not ok with telegram tingz
    '''
    assert isinstance(msg, str), 'Message input must be a string!'
    msg = msg.replace('\\', '')
    msg = msg.replace('!', '\!')
    msg = msg.replace('*', '')
    msg = msg.replace('_', '')
    msg = msg.replace('(', '\(')
    msg = msg.replace(')', '\)')
    msg = msg.replace('-', '\-')
    return msg

def set_user_data_to_default(context, default_user_data):
    '''
    Recursively sets user_data['temp'] of this user to default user_data['temp']
    '''
    assert isinstance(default_user_data, (dict, defaultdict)), \
        'default user data must be a defaultdict or dict'
    # recursively add the attributes of the dictionary
    for key in default_user_data.keys():
        # make the list or dictionary immutable
        if isinstance(default_user_data[key], (dict, list)):
            context.user_data[key] = default_user_data[key].copy()
        else:
            context.user_data[key] = default_user_data[key]

def set_default_bot_data(dispatcher, default_bot_data):
    assert isinstance(default_bot_data, (dict, defaultdict)), \
        'default user data must be a defaultdict or dict'
    # recursively add the attributes of the dictionary
    for key in default_bot_data.keys():
        # make the list or dictionary immutable
        if isinstance(default_bot_data[key], (dict, list)):
            dispatcher.bot_data[key] = default_bot_data[key].copy()
        else:
            dispatcher.bot_data[key] = default_bot_data[key]

def restart_user(context, user_id=None): 
    '''
    Wrapper around @set_user_data_to_default
    to clear all data and reset
    '''
    from env import default_user_data
    queue = context.bot_data['queues']['main']
    #remove users from queue
    if user_id in queue:
        remove_user_from_queue(user_id, queue)

    #remove users from conv
    if 'convo_ids' in context.user_data:
        if not context.user_data['convo_ids'] == []:
            user_ids = context.user_data['convo_ids']
            user_ids.append(user_id)
            remove_users_from_conv(user_ids, context)
    #clear user data and set back to default
    context.user_data.clear()
    set_user_data_to_default(context, default_user_data)
    if user_id in context.bot_data['active']:
        del context.bot_data['active'][user_id]


def clear_temp_data(context):
    '''
    Clears all temp data saved by user
    '''
    context.user_data['temp_data'].clear()

# FOR CONVERSATIONS
####################

def find_match(queue):
    if len(queue) >= 1:
        return list(queue.keys())[0]
    return None

def add_user_to_queue(user_id, queue):
    #not sure what the plans are for this
    if not user_id in queue.keys():
        queue[user_id] = datetime.datetime.now()

def remove_user_from_queue(user_id, queue, queue_name='main'):
    if user_id in queue:
        del queue[user_id]
    return

def get_users_id(user_ids):
    data = {
        'user_id': user_ids
    }
    #ids = requests.get(BACKEND_URL + '/user/id/fromUserId', data=data).json()
    ids = [id['_id'] for id in ids]
    return ids

def bd_join_conv(user_id, conv_id, bot_data):
    bot_data['active'][user_id] = conv_id

def start_conversation(user_ids, queue, context):
    '''
    Starts a conversation between all the users taken as input
    '''
    user_ids.sort()

    for user_id in user_ids:
        personal_version = user_ids.copy()
        if user_id in personal_version:
            personal_version.remove(user_id)
        context.dispatcher.user_data[user_id]['convo_ids'] = personal_version

        # send pairing message to all users
        context.bot.send_message(chat_id=user_id, **msgs.functions.pair_found)

        # remove user from queue
        remove_user_from_queue(user_id, queue)
    
    # send to backend
    users= get_users_id(user_ids)
    # TODO: prepare for exception
    data = {
        'participants': users
    }
    #res = requests.post(BACKEND_URL + '/convo', data=data)
    for user_id in user_ids:
        bd_join_conv(user_id, res.json()['_id'], context.bot_data)

def remove_users_from_conv(user_ids, context):
    convo_id = context.bot_data['active'][user_ids[0]]
    for user_id in user_ids:
        context.bot_data['active'][user_id] = True
        context.dispatcher.user_data[user_id]['convo_ids'] = []
        context.bot.send_message(user_id, msgs.core.conv_ended)
        context.bot.send_message(user_id, **msgs.menu.conversation)
    
    payload = {
        "id": convo_id
    }
    #requests.post(BACKEND_URL + '/convo/endById', json=payload)

def get_telegram_file_types_dict(telegram, bot, file_type):
    '''
    WARNING: 
    - GAME IS NOT WORKING
    - MEDIA GROUP IS NOT 100% clean
    '''
    
    telegram_file_types = {
        telegram.PhotoSize: {
            'allow_caption': True,
            'function': bot.send_photo,
            'specific_param': False},
        telegram.Video: {
            'allow_caption' : True,
            'function': bot.send_video,
            'specific_param': False},
        telegram.Audio: {
            'allow_caption': True,
            'function': bot.send_audio,
            'specific_param': False},
        telegram.Voice: {
            'allow_caption': True,
            'function': bot.send_voice,
            'specific_param': False},
        telegram.Document: {
            'allow_caption': True,
            'function': bot.send_document,
            'specific_param': False},
        telegram.Animation: {
            'allow_caption': True,
            'function': bot.send_animation,
            'specific_param': False},
        telegram.Sticker: {
            'allow_caption': False,
            'function': bot.send_sticker,
            'specific_param': False},
        # this requires game short name
        telegram.Game: {
            'allow_caption': False,
            'function': bot.send_game,
            'specific_param': 'game_short_name'},
        # these require specific param name
        telegram.Contact: {
            'allow_caption': False,
            'function': bot.send_contact,
            'specific_param': 'contact'},
        telegram.Location: {
            'allow_caption': False,
            'function': bot.send_location,
            'specific_param': 'location'},
        telegram.Venue: {
            'allow_caption': False,
            'function': bot.send_venue,
            'specific_param': 'venue'},
        telegram.VideoNote: {
            'allow_caption': False,
            'function': bot.send_video_note,
            'specific_param': False},
        "media_group": {
            'allow_caption': True,
            'function': bot.send_photo,
            'specific_param': False},
        None: {
            'allow_caption': False,
            'function': bot.send_message,
            'specific_param': False}
    }
    return telegram_file_types[file_type]

def get_text_from_message(message: telegram.Message, file_type, bot):
    telegram_file_types = get_telegram_file_types_dict(telegram, bot, file_type)
    allow_caption = telegram_file_types['allow_caption']
    if allow_caption:
        return message.caption
    else:
        return message.text

def send_universal(bot, chat_id, message: str= None, file=None, file_type=None):
    function_dict = get_telegram_file_types_dict(telegram, bot, file_type) # moved this to env
    # if it is a game or media group, ignore
    if type(file) == telegram.Game:
        return bot.send_message(chat_id, text= 'Sending games is currently not allowed... Please inform the developers if you want to see it')
    fn = function_dict['function']
    # if it is a normal message just forward
    if not file:
        return fn(chat_id = chat_id, text = message)
    params = {}
    # everything else
    if function_dict['allow_caption']:
        params['caption'] = message
    if function_dict['specific_param']:
        params[function_dict['specific_param']] = file
        msg = fn(chat_id, **params)
    elif params: 
        msg = fn(chat_id, file, **params)
    else: 
        msg = fn(chat_id, file)
    
    return msg

def send_message_to_group(bot, chat_ids, message: str, file=None, file_type=None, owner_id=None):
    for chat_id in chat_ids:
        if chat_id == owner_id:
            continue
        send_universal(bot, chat_id, message, file, file_type)
    if owner_id:
        bot.send_message(owner_id, "Message succesfully sent")

def get_msg_file(message: telegram.Message):
    if message.media_group_id:
        input_photo = message.photo[-1]
        return input_photo, "media_group"
    file_type = None
    file = message.photo or message.video or message.audio or \
           message.voice or message.document or message.animation or \
           message.sticker or message.game or message.contact or message.location or\
           message.venue or message.video_note
    if isinstance(file, list):
        file = file[-1]
    elif isinstance(file, dict):
        pass
    if file is None:
        pass
    else:
        file_type = type(file)

    return file, file_type

def generate_options(options, msg=''):
    msg += '\n\n'
    if isinstance(options, list):
        for option in options:
            i, details = option[0], option[1:]
            # ensures that all values are strings
            details = list(map(str, details))
            details = ' | '.join(details)
            line =f'{i}: {details}\n'
            msg += line
    elif isinstance(options, (dict, defaultdict)):
        for key in options.keys():
            i, details = key, options[key]
            # ensures that all values are strings
            details = list(map(str, details))
            details = ' | '.join(details)
            line =f'{i}: {details}\n'
            msg += line
    return msg

def generate_menu(menu, dbi, user_id, msg=''):
    menus = ['sleep_menu', 'start_menu', 'admin_menu', 'backend', 'in_action']
    if isinstance(menu, int):
        menu = menus[menu]
    else:
        assert menu in menus, 'Invalid Menu'
    fns = dbi.menu_fns(menu, user_id)
    for fn in fns:
        line = ' -- '.join(fn)
        line = '/{}\n'.format(line)
        msg += line
    return msg

def FileHandler(fn):
    return MessageHandler((Filters.text | Filters.photo | Filters.document \
            | Filters.video | Filters.audio | \
            Filters.voice | Filters.attachment) & ~Filters.command, fn)

########################
# IMPORTANT DECORATORS #
########################

def send_typing_action(func):
    '''Sends typing action while func command.
    Just: 
    @send_typing_action
    def my_handler(update, context):
        pass
    '''
    
    @wraps(func)
    def typing_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, \
            action=telegram.ChatAction.TYPING)
        return func(update, context)

    return typing_func

def time_execution(fn):
    '''
    This function is meant to be a decorator to time any function that is happening
    Prints the time taken to complete function in second(s)
    '''
    def timer(*args, **kwargs):
        start = time.time()
        # run the function
        fn(*args, **kwargs)
        end = time.time()
        time_taken = end - start
        print(time_taken)
    return timer