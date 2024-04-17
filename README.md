# OBS-Recording-Organizer
## Description
### 
This is an updated and improved version of [francdv23's OBS Recordings Organizer](https://github.com/francdv23/OBS-Recordings-Organizer/) Python script, that, similarly to NVidia ShadowPlay, allows OBS to rename and organize into folders video recordings based on the window title on focus whenever a replay buffer or a recording is saved. 

I fixed the issues that this script has and added some additional feature to make it easier to use.
## How to install
### Requirements
#### 
Python 3.6+ [(3.11 recommended)](https://www.python.org/downloads/release/python-3110/), as well as [pywin32](https://pypi.org/project/pywin32/) and [psutil](https://pypi.org/project/psutil/) libraries which can be installed via command line:
```
pip install pywin32
pip install psutil
```
Python can now be loaded in OBS by `Tools > Scripts > Python Settings` and choosing Python311 path.
### Next steps
#### 
After the previous indications the actiual script can be now installed. It doesn't need to be placed in a specific directory, for convenience the scripts folder located at `C:\Program Files\obs-studio\data\obs-plugins\frontend-tools\scripts\obs-rec-organizer` is ideal. It can be loaded into OBS by `Tools > Scripts` hit the *__"+"__* sign and search for _OBS-RecOrganizer-better.py_ from the previous path.
## Settings and configurations
### Basic
#### 
From OBS' Scripts window choose your main recordings folder by clicking *Browse* and write in the *Extension* box your videos extension of without the "." sign.
### Overrides
#### 
Within the scripts are included two *cfg* files named *DesktopOverride.cfg* and *FullscreenOverride.cfg*, you can write the executable name in them to respectively override a windowed game targetting it correctly or to tweak a fullscreen program in *"Desktop"* recording.

**padii's edit:** I did not test it, as I did not need it, so let me know if anything's wrong with this.
## Common problems
#### 
1) If you experience any problems installing the libraries, the first thing I recommend to do is update pip with: 
```
python -m pip install --upgrade pip
```
2) If Pywin32 gives you any troubles, first uninstall it with ```pip uninstall pywin32``` and then download it from [here](https://github.com/mhammond/pywin32/releases/tag/b305) choosing *py36* version.
####
3) Recordings not organized into subfolder or not renamed: it can occur in the first/second recording or buffer replay, but no more further because the script only needed to create its cache.
