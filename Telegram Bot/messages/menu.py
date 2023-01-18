import keyboards as kbds

conversation = {
    "text": "You are in conversation menu now. Select your action.",
    "reply_markup": kbds.conversation_menu_keyboard
}

description = {
    "text": "You are in description menu now. Select the description you want to edit\n1. /course\n2. /matriculation_year\n3. /hobby\n\nType \'My current details\' to check your details and /quit to return back to the main menu",
    "reply_markup": kbds.description_menu_keyboard
}

menu = {
    "text": "You are going to the main menu now.",
    "reply_markup": kbds.menu_keyboard
}

share = {
    "text": "So what's that something that I don't already know huh?\n\nType /back when you are done"
}

sharing_replies = ['Interesting...', \
                   'I didnt know that meh',\
                   'I should have known better :(',\
                   'Dont worry, these are all taken down somewhere!'
                   ]

bored_replies = ['That\'s the whole point of the bot...']

sad_replies = ['Why are you sad!?! @EngEnHui right now!', \
               'WHO BULLY YOU THIS TIME :\ I GO POUNCE ON HIM. SEND THE @ TO @EngEnHui NOW', \
               'Cheer up pls, ure a pretty girl!',\
               'Storms doesn’t last forever, so cheer up and never give up!',\
               'Things will get better. It may be today or tomorrow, but stay cheerful!',\
               '@EngEnHui to redeem your meetup voucher',\
               ]

imy_replies = ['I miss you too. Tell me when you wanna meet me!']

imy_menu_back = "Type /back when you are done"

wordle = {
    "text": "Welcome to the wordle game!"
}

wordle_letters = {
    "text": "How many letters of word would you like to play?",
    "reply_markup": kbds.number_keyboard
}
