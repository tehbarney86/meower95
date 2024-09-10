# DISCLAIMER: this client is very silly ;3
i have been banned from meower for very silly (and kinda fake) reasons, so, since im bored, im turning hacks back lol

feel free to annoy everybody in chat once again, because `ec[Meower95!]aSBmZWx0IGxpa2UgaXQgbG9sIGZ1Y2sgdGhlIHJmYyBM`

# Meower95!

<p align="center"><i>"the spy has already breached our defences"</i></p>

![License Badge](https://img.shields.io/github/license/tehbarney86/meower95)
![Repo Size Badge](https://img.shields.io/github/repo-size/tehbarney86/meower95)
![Sigma Badge](https://raw.githubusercontent.com/tehbarney86/meower95/d61d881017637b2b7b5fe56e4188e8ff0e45d3bb/assets/screenshots/license_%20MIT.svg)

Meower95 is the new lightweight, cute, Windows 95-styled and heckin'-hackin' Meower client designed for low-end hardware, with features like:
* Selecting your own server and account on start up;
* Simple IRC-like layout and design;
* New "hack" features (that will probably also get you banned with meower's 1984 moderation :P)
* Locally setting up avatars for other accounts;
* Silly and cutesy pre-built avatars for regular users;
* Text emoticons like ":3" converting to normal emojis;
* Good-old Windows 95 simple look.

![](https://github.com/tehbarney86/meower95/blob/main/assets/screenshots/1.png?raw=true)
![](https://github.com/tehbarney86/meower95/blob/main/assets/screenshots/2.png?raw=true)
![](https://github.com/tehbarney86/meower95/blob/main/assets/screenshots/3.png?raw=true)
## Looks & Feels
Using the good ol' `tkinter` python library, Meower95 is lightweight and inspired by the late 90's design language, and we've worked hard to make it look as nice and fair to 90's designs, while still providing modern features.
### Simple design
Meower95 is simple too - every action is just a few clicks away:
* Click on someone's message to reply to it, or on your own to edit it;
* Click on a username or profile on the right sidebar to see their quote and see in what group chats you both are in.
* Right clicking on your messages allows you to quickly delete them;
* Pressing the up arrow will allow you to edit your last typed message.

Since Meower95 is still in development, more simplistic features are coming in the future, like: (TODO)
* Right clicking on a user profile or their message opens up a window to report them;
## Hacks
Meower95 is written with pure Python, so it cannot be blacklisted - Python's urllib doesn't send any unnecessary information to any servers, except for a random useragent.

In return this blocks any servers from banning this client, which allows it to use any hacks included in the program without any hassle, like
* Not removing deleted messages from channels;
* Encoding your messages into Base64 so only clients that support it can see it.;
> **WARNING - it is not our responsibility if you get banned for using such features. Using them you take a high risk of getting banned from any server if the moderation deems it as harmful or violating a ToS.**
> Using Meower95's hack features is fully compatible with Meower's Terms of Service and don't use any prohibitied actions.
> Here's a "FAQ" of actions that are not against the ToS (lemme turn on my saul goodman):
> * **Spam - by using Base64 encryption, you're spamming gibberish for other clients** - It is an issue of any client not supporting it, the messages are not a part of Meower's service and can be whatever you want as long as it follows the ToS. Plus, by Meower's ToS definition of Spam (an unsolicited message posted with rapid succession), no rapid succession is in sight.
> * **Data leakage - by leaving messages after their deletion, you're exposing the owner's unwanted information** - by sending the message they wanted, they already consented to leave the information from that message in the public consciousness of Meower's users, and it is not a data leak if it already publicly known information (e.g., if someone screenshotted a part of a chat, a user could've maliciously delete messages included in a screenshot and request banning that person afterwards)
> * **Turning the lights off - by using Base64 encoding, you're inhibiting Meower's services** - your messages are not a part of Meower's services, nor is it a part of any unsupported client's "experience", and they can be whatever the contents you want to as long as they follow the ToS - e.g. if this rule would be true, banning/kicking a person would be inhibiting Meower's services, since that user cannot send messages - "a part of Meower's services";
## Privacy Notice
**Meower95 nor it's creators or contibutors store your data anywhere on our machines**, but *valuable information is stored locally on your computer*, so we advise you to not share these files to someone you don't trust:
* `meower95.conf` (this file stores your passwords for logging in);
* `meower95.log` (this file logs websocket transmissions which contain a lot of information like your token, password, etc.)
If any issue is encountered, never send the contents of these files.

# Setting up
*(Meower95 is still in development and can sometimes be unstable, so if any bugs appear, please report them to our [issues page](https://github.com/tehbarney86/meower95/issues/))*

Run `meower95.py` using your Python executable. Make sure you have all modules listed in `requirements.txt` installed, or just run `pip3 install -i requirements.txt` in a console environment.

## Hardware requirements:
Currently the bare minimum is untested, yet the least powerful machine specs that can run this program probably go down to:
* Processor - Intel Celeron (tested on an Intel Atom N270 and Core i5-4440);
* RAM - 2 Gb (tested on 2 and 4 Gb);
* Internet Speed - 50 Kb/S
* Video Resolution - Not enforced, but smaller resolutions like 1280x768 are recommended as the program is designed for low resolution displays (tested on 1024x600, 1440x900, 1920x1080, etc.);
* OS - Anything that can run Python 3.xx and modules required by Meower95 as listed in `requirements.txt` (Tested on Debian 12, Pop!_OS and Windows 10).

***We hope you enjoy!***
