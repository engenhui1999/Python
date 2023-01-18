from telegram import ReplyKeyboardMarkup

yes_no_keyboard = [['Yes'], ['No']]
yes_no_keyboard = ReplyKeyboardMarkup(yes_no_keyboard, one_time_keyboard=True)

menu_keyboard = [['/Share'],['/Bored'], ['/Sad'], ['/IMY'], ['/Wordle']]
menu_keyboard = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)

description_menu_keyboard = [['/course'],['/matriculation_year'],['/hobby'],['My current details'],['/quit']]
description_menu_keyboard = ReplyKeyboardMarkup(description_menu_keyboard, one_time_keyboard=True)

conversation_menu_keyboard = [['/convo_with_enhui'],['/pair'],['/quit']]
conversation_menu_keyboard = ReplyKeyboardMarkup(conversation_menu_keyboard, one_time_keyboard=True)

pair_found = [['/unpair'], ['/share_telehandle'], ['/request_telehandle'],['/quit']]
pair_found = ReplyKeyboardMarkup(pair_found)

start_keyboard = [['/start']]
start_keyboard = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

number_keyboard = [['3'],['4'],['5'],['6'],['7']]
number_keyboard = ReplyKeyboardMarkup(number_keyboard, one_time_keyboard=True)

play_again_keyboard = [['/play_again'],['/back']]
play_again_keyboard = ReplyKeyboardMarkup(play_again_keyboard, one_time_keyboard=True)

start_game_keyboard = [['/start_game'],['/back']]
start_game_keyboard = ReplyKeyboardMarkup(start_game_keyboard, one_time_keyboard=True)