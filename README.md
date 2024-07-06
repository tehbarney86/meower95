# Meower95!
Meower95 is the new lightweight, cute, Windows-styled and heckin' hackin' Python Meower client designed for low-end hardware, with features like:
* Selecting your own server and account on start up;
* Simple IRC-like layout and design;
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
> **WARNING - it is not our responsibility if you get banned for using such features. Using them you take a high risk of getting banned from any server if the moderation deems it as harmful or violating a ToS.**
> Using Meower95's hack features is fully compatible with Meower's Terms of Service and don't use any prohibitied actions.
> Here's a "FAQ" of actions that are not against the ToS (lemme turn on my saul goodman):
> * **Spam - by using Discord message corruption, you're spamming for Bridge users** - it is a problem of the Discord Bridge, and not a violation of the client, proof being every other client receiving messages without the repeated autoedited message. Additionaly, autoediting is not intented to be spam nor is it in rapid succession as the ToS would suggest by it's terminology of "Spam";
> * **Spam - by using Base64 encryption, you're spamming gibberish for other clients** - again, it is technically an issue of any client not supporting it, and no rapid succession is in sight.
> * **Data leakage - by leaving messages after their deletion, you're exposing the owner's unwanted information** - by sending the message they wanted, they already consented to leave the information from that message in the public consciousness of Meower's users, and it is not a data leak if it already publicly known information (e.g., if someone screenshotted a part of a chat, a user could've maliciously delete messages included in a screenshot and request banning that person afterwards)
> * **Turn the lights off - by using Discord message corruption or Base64 encryption, you're inhibiting Meower's services (i even got banned for this one wow)** - your messages are not a part of Meower's services, nor is it a part of any unsupported client's "experience", and they can be whatever the contents you want to as long as they follow the ToS - e.g. if this rule would be true, banning/kicking a person would be inhibiting Meower's services, since that user not sending messages - "a part of Meower's services";
> * **Sharing advertisements - by adding a link to Meower95's github in the autoedit message (if Discord message corruption is enabled) you're advertising** - (this is obvious, yet has been frequently mentioned) the ToS specifically mentions that only commercial products are disallowed from being advertised, and Meower95 is (and will be) a non-commercial and open-source project, therefore fully allowed being advertised like all other Meower clients.
## Privacy Notice
**Meower95 nor it's creators or contibutors store your data anywhere on our machines**, but *valuable information is stored locally on your computer*, so we advice you to not share these files to someone you do not trust:
* `meower95.conf` (this file stores your passwords for logging in);
* `meower95.log` (this file logs websocket transmissions which contain a lot of information like your token, password, etc.)
If any issue is encountered, never send the contents of these files.

# Setting up
*(Meower95 is just in development and can be sometimes unstable, so if any bugs appear, please report them to our [issues page](https://github.com/tehbarney86/meower95/issues/))*

Run `meower95.py` using your python executable. Make sure you have all modules listed in `requrements.txt` installed, or just run `pip3 install -i requirements.txt` in a console environment.

## Hardware requirements:
Currently the pure minimum is untested, yet the least powerful machine specs that can run this program probably bare down to:
* Processor - Intel Celeron (tested on Intel Atom N270);
* RAM - 512 Mb, (tested on 2 Gb);
* Internet Speed - 50 Kb/S
* Video Resolution - Not enforced, but smaller resolutions like 1280x768 recommended as the program is designed for low resolution displays (tested on 1024x600);
* OS - Anything that can run Python 3 and modules required by Meower95 listed in `requirements.txt` (Tested on Xfce4 Debian 12).

***We hope you enjoy!***
