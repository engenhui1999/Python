import datetime
from re import L
import json

from telegram import message, replykeyboardmarkup
from utils.core import send_message_to_group, start_conversation
import telegram
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from env import *
import messages as msgs
import utils
import random
#import requests
import keyboards as kbds
import datetime

word_to_guess = ""
num_tries = 0
letters_used = ""

def main(update, context):
    global word_to_guess
    global num_tries
    global letters_used
    user_guess = update.message.text.lower()

    print("user_guess: " + user_guess + "\tword_to_guess: " + word_to_guess)

    if len(user_guess) != len(word_to_guess):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"You should be guessing a {len(word_to_guess)}-letter word. Try again!")
        return GAME


    if user_guess == word_to_guess:
        context.bot.send_message(chat_id=update.effective_chat.id, text="CONGRATS YOU GOT IT!\n\nWould you like to play again?",
                                 reply_markup = kbds.play_again_keyboard)
        restart_game()
        return WORDLEMENU

    for letter in user_guess:
        if letter in letters_used:
            string2 = letter + " - letter is not in the word\n\nTry again without using these letter:\n" + letters_used
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{string2}")
            return GAME

    i = 0
    string = f"Your guess: {user_guess}\n\n"
    for letter in user_guess:
        if word_to_guess[i] == letter:
            string += letter + " - Correct\n"
        elif letter in word_to_guess:
            string += letter + " - Wrong position\n"
        else:
            string += letter + " - Wrong letter\n"
            if letter not in letters_used:
                letters_used += letter + " "
        i += 1

    num_tries += 1
    if num_tries == 8:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"You ran out of tries! The word is {word_to_guess}. NICE TRY!\n\nWould you like to play again?",
                                 reply_markup = kbds.play_again_keyboard)
        restart_game()
        return WORDLEMENU

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{string}\nYou have {8 - num_tries} tries left.\n/back to leave")
    return GAME

def restart_game():
    global word_to_guess
    global num_tries
    global letters_used
    word_to_guess = ""
    num_tries = 0
    letters_used = ""

def set_word(word):
    global word_to_guess
    word_to_guess= word
    return

def select_word_randomly(seed, word_dict):
    random.seed()
    word = random.choice(word_dict)
    return word

def list_of_words(num_of_letters):
    word_dict = []
    for line in open('./database/easier_words.txt', 'r'):
        if len(line) - 1 == num_of_letters:
            word_dict.append(line.strip())
    return word_dict

# word_dict = list_of_words(5)
# print(len(word_dict))
# word = select_word_randomly(5, word_dict)
# set_word(word)
# main(1,1)