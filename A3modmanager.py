##########################################################
# Parse Arma's Preset file + install mods + restart LGSM
#
# Alexis TARUSSIO  : alexis.tarussio@gmail.com
# 24/10/2020
#
# 24/10/20 V1.00  Creation
#
#
##########################################################

import subprocess
import os
import shutil
import re
import sys
import fileinput
from bs4 import BeautifulSoup
import configparser
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT



if not Path("lgsm/config-lgsm/arma3server/arma3mods.cfg").is_file():
    print("lgsm/config-lgsm/arma3server/arma3mods.cfg Does not exist check your file location")
    exit(1)

configParser = configparser.RawConfigParser()
configFilePath = r'lgsm/config-lgsm/arma3server/arma3mods.cfg'
configParser.read(configFilePath)

LGSM_CONFIG_FILE    = configParser.get('arma-config', 'LGSM_CONFIG_FILE')
steamUser           = configParser.get('arma-config', 'steamUser')
steamPassword       = configParser.get('arma-config', 'steamPassword')
modDirectory        = os.environ["HOME"] + "/" + configParser.get('arma-config', 'modDirectory')
steamCmdBin         = configParser.get('arma-config', 'steamCmdBin')
armaServerBin       = os.environ["HOME"] + "/" + configParser.get('arma-config', 'armaServerBin')
armaServerBin       = os.environ["HOME"] + "/" + configParser.get('arma-config', 'armaServerBin')
uploadFolder        = os.environ["HOME"] + "/" + configParser.get('arma-config', 'uploadFolder')
serverMods          = "mods=\""
modList             = {}



if not Path(uploadFolder).is_dir():
    print(uploadFolder + " Does not exist you must create the folder.")
    exit(1)

# Search for preset html file
for f_name in os.listdir(uploadFolder):
    if f_name.endswith('.html'):
        PRESET_FILE= uploadFolder + f_name
        if not Path(PRESET_FILE).is_file():
            print(PRESET_FILE + " Does not exist, PRESET_FILE must be a html\'s file ")
            exit(1)

with open(PRESET_FILE) as pf:
    soup = BeautifulSoup(pf, 'html.parser')
table = soup.find("table")

tr = table.findAll(['tr'])[0:]

for data in tr:
    td = data.find_all('td', attrs={"data-type":"DisplayName"})
    tdData = [col.text.strip('\n') for col in td]
    modName = tdData[0].lower().replace(" ", "_")
    for specialchar in [".", ":", "(", ")", "+", "'", "/"]:
        modName = modName.replace(specialchar, "")
    url = data.find_all('a')
    urlData = [col.text.strip('\n') for col in url]
    modId = urlData[0].split("=",1)[1]
    modList[modName] = modId

# Delete PRESET_FILE to maintain uploadDir clean.
os.remove(PRESET_FILE)

steamcmd_data = ""
# Install Mods
for key, value in modList.items():
    steamcmd_data += "workshop_download_item 107410 " + value + "\n"
    # Create Symlink
    workshopDir= modDirectory + "steamapps/workshop/content/107410/" + value
    targetDir= modDirectory +"@" + key
    if not os.path.exists(targetDir):
        os.symlink(workshopDir, targetDir)
    serverMods += "mods/@" + key + "\;"

serverMods += "\""

steamcmd_data += "quit"
p = subprocess.run([steamCmdBin, "+login", steamUser,  steamPassword, "+force_install_dir", modDirectory], input=steamcmd_data, encoding='ascii')

print(p.returncode)


print('\n=============== Lowercase Mods\s Files  ===============\n')

for path, subdirs, files in os.walk(modDirectory):
    for name in files:
        oldFile = path + "/" + name
        newFile = path + "/" + name.lower()
        os.rename(oldFile, newFile)

print('\n=============== Now let\'s poush config  ===============\n')

for line in fileinput.input([LGSM_CONFIG_FILE], inplace=True):
    if line.strip().startswith('mods='):
        line = serverMods
    sys.stdout.write(line)

print('\n=============== Restart Server  ===============\n')

subprocess.call([armaServerBin, "restart"])