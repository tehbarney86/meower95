# Meower95!
Meower95 is the new lightweight, cute, Windows-styled and heckin' hackin' Python Meower client designed for low-end hardware, with features like:
* Selecting your own server and account on start up;
* Simple IRC-like layout and design;
* Pure Python;
* New "hacked-in" features (that might even get you banned!)
* Locally setting up avatars for other accounts;
* Standard emojis like ":3" converting to image emojis;
* Good-old Windows 95 simple look (unless you're on windows 10/11 lol).
## Looks & Feels
Using the good ol' tkinter python library, Meower95 is lightweight and inspired by late 90s design language, and we have worked hard to make it look as nice and fair to 90s designs, while providing modern features.
### Simple design
Meower95 is simple too - every action is just a few clicks away:
* Click on someone's message to reply to it, or on your own to edit it;
* Click on a username or profile on the right sidebar to see their quote and see in what group chats you both are in.
Since Meower95 is still in development, more simplistic features are coming in the future, like:
* Right clicking on a user profile or their message opens up a window to report them;
* Right clikcing on your messages allows you to quickly delete them;
* Pressing the up arrow will allow you to edit your last typed message.
## Hacks
Meower95 is written with pure python, so it cannot be blacklisted - python's urllib doesn't send any unnecessary information to any servers, except for a random useragent.

In return this blocks any servers from banning this client, which allows it to use any hacks included in the program without any hussle, like
* Leaving *(basically not removing)* deleted messages from channels;
* Autoeditng messages so to not appear in "webhook-like" bridges like the Discord Bridge;
* Encrypting your messages to Base64 so only clients that support it can see it.;
> **WARNING - it is not our responsibility if you get banned for using such features. Using them has a high risk of getting banned from any server if the moderation deems it as harmful or violating a ToS.** (especially expect getting banned from the main 1984 meower server lmao)
## Privacy Notice
**Meower95 nor it's creators or contibutors store your data anywhere on our machines**, but *valuable information is stored locally on your computer*, so we advice you to not share these files to someone you do not trust:
* `meower95.conf` (this file stores your passwords for logging in);
* `meower95.log` (this file logs websocket transmissions which contain a lot of information like your token, password, etc.)
If any issue is encountered, never send the contents of these files.

# Setting up
*(Meower95 is just in development and sometimes unstable, so please if any bugs appear, report them to our issues page)*

Run `meower95.py` using your python executable. Make sure you have all modules listed in `requrements.txt`, or just run `pip3 install -i requirements.txt` in your console.

##Hardware requirements:
Currently the pure minimum is unkown, yet the least powerful machine specs that can run this program probably bare down to:
* Processor - Intel Celeron;
* Video Resolution - Not enforced, but smaller resolution from 800x600 to 1400x900 recommended as the program is designed for low resolution screens;
* RAM - 2 Gb, although smaller amounts haven't been tested yet.
* OS - Anything can run Python 3 basically (untested, Linux works perfectly, while Windows is only from Windows 10-11, although might be not true).

***We hope you enjoy!***
