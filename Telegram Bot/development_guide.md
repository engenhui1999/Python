# Guide for developers
Last edit: 23 June 2021 

# Branches
As a general rule of thumb, **PLEASE ALWAYS CHECK IF YOU ARE COMMITTING/ PUSHING TO THE RIGHT BRANCH**, if unsure, please check with me. Although it is always possible to rebranch it, it is a very tedious and annoying process which i hope i never need to. As another general rule of thumb, **NO ONE** should be pushing to master branch, except the project manager.

## develop
For now, opnly ill merge here, you can merge into telebot-ui branch

## backend
as simple as it sounds all the jd/ db management will go there

## info
Meant for changed in **TEXTUAL** stuff for information relay such as patch notes, development guide. This branch has the update version of all these.

# Folder Structure
This folder structure has been highly deliberated on, optimized for cleanliness. It is as follows

## Backend
This is purely for the database management + express api portion. It functions as a semi-different repo in itself. There should be minimal cross-overs

## Logs
This is meant to contain all logs from:
- docker containers
- express backend
- mongodb
- python telegram bot itself

## Messages
All the messages to be used for the bot. Instead of writing them individually in the python files, please collate them all in the messages folder to be used 

## core.py vs utils.core.py
Basically the main difference is that utils.core should be utility functions, things that can be used anywhere, whereas core.py should **ONLY** be stuff to be used in main.py.

Any major difference when thinking which to put it under is whether it is a function that takes only update and/or context as parameters. If yes, highly likely it should be in core.py, otherwise just throw it into utils.core at a reasonable position

## utils.logic
This should mostly be mathy/ algorithmy stuff

# Dependencies
If you want to add anymore dependencies, please make sure to inform me on telegram as I need to check if it is compatible with the deployment server. I'm trying to limit any resource expended as possible as we deploy so it might not have any many stuff as you hope it would. 