# Arma3-Mod-Manager
Parse Preset File, install, restart Arma 3's server

## What's A3MM ?
A3MM permit you to manage your mod in the easiest way with [LGSM](https://linuxgsm.com/) which doesn't provide mods support for Arma 3.

## Requirement :
- Python3
- Steamcmd
- LGSM Install
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

## Installation
Git clone the project.
Create your config file from the example.
Allow your LGSM's user to use it.
Create upload's folder.

## How do I use it ? 

Create your server's preset with Arma 3 Client and export it as HTML's file, beautifulSoup will manage this part.
![armaLauncher](https://i.ibb.co/CPsdbKS/armalauncher.jpg)
![save](https://i.ibb.co/hVG95kT/save.jpg)

Just upload this HTML's file to your folder : upload.

Run the script 
```bash
python3 A3modmanager.py
```

A3MM will : 

- Get your HTML's file
- Parse it
- Delete HTML's file
- loop and install mods
- Change the mods's value from LGSM config's file
- Restart LGSM Arma's server
