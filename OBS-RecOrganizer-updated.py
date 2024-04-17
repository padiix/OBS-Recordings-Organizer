import obspython as S
import glob, win32gui, win32process, re, psutil, os, os.path, shutil
from pathlib import Path
from ctypes import windll

def on_event(event):

    if event == S.OBS_FRONTEND_EVENT_RECORDING_STOPPED:

        print("Triggered when the recording stopped.")

        file = File()

        file.create_new_folder()

        file.remember_and_move()
        
        print("Old path: " + file.get_oldPath())
        print("New path: " + file.get_newPath())
        
    
    if event == S.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED:

        print("Triggered when the replay buffer is saved.")
        
        file = File()

        file.create_new_folder()

        file.remember_and_move()
        
        print("Old path: " + file.get_oldPath())
        print("New path: " + file.get_newPath())


def get_window_title():

    user32 = windll.user32

    swd, sht = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Add in fullscreen detection here! 
    w = win32gui
    win_title = w.GetWindowText(w.GetForegroundWindow())
    
    l, t, r, b = w.GetWindowRect(w.GetForegroundWindow())
    wd, ht = r - l, b - t

    tid, pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())
    p = psutil.Process(pid)
    exe = p.name()

    desktopOveride = 0
    fullscreenOveride = 0

    with open(script_path()+'/DesktopOverride.cfg') as dofile:
     if exe in dofile.read():
            desktopOveride = 1
    
    with open(script_path()+'/FullscreenOverride.cfg') as fsfile:
        if exe in fsfile.read():
            fullscreenOveride = 1

    if win_title[:3] == 'OBS':
        title = "Manual Recording"
    elif desktopOveride == 1:
        title = win_title
    else:
        if  wd == swd and ht == sht and fullscreenOveride == 0:
            title = win_title
        else:
            title = "Desktop"

    #Remove non-alphanumeric characters (ex. ':')
    title = re.sub(r'[^A-Za-z0-9 ]+', '', title)
    #Remove whitespaces at the end
    title = "".join(title.rstrip())
    #Remove additional whitespaces
    title = " ".join(title.split())

    title = title[:50]

    return title

def find_latest_file(folder_path, file_type):
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)
    return max_file

def script_load(settings):
    S.obs_frontend_add_event_callback(on_event)

def script_defaults(settings):
    S.obs_data_set_default_string(settings, "extension", "mkv")

def script_update(settings):
    Data.AddTitleBool = S.obs_data_get_bool(settings, "title_before_bool")
    Data.OutputDir = S.obs_data_get_string(settings, "outputdir")
    Data.OutputDir = Data.OutputDir.replace('/','\\')
    Data.Extension = S.obs_data_get_string(settings, "extension")
    Data.ExtensionMask = '\*' + Data.Extension

def script_description():
    desc = ("<h3>OBS Recording Organizer Upgraded <br> (<u>04.2024</u> update)</h3>"
            "<hr>"
            "Renames and organizes recordings into subfolders similar to NVIDIA ShadowPlay (<i>NVIDIA GeForce Experience</i>).<br><br>"
            "<small>Original author:</small> <a href='https://obsproject.com/forum/resources/obs-recordings-organizer.1707/'><b>francedv23</b></a><br>"
            "<small>Updated by:</small> <b>padii</b><br><br>"
            "<h4>Settings:</h4>")
    return desc

def script_properties():
    props = S.obs_properties_create()
    bool_p = S.obs_properties_add_bool(props, "title_before_bool", "Add name of the game as a recording prefix"); 
    S.obs_property_set_long_description(bool_p, "Check if you want to have name of the game appended as a prefix to the recording, else uncheck")
    S.obs_properties_add_path(
        props, "outputdir", "Recordings folder", S.OBS_PATH_DIRECTORY,
        None, str(Path.home()))
    S.obs_properties_add_text(
        props,"extension","File extension", S.OBS_TEXT_DEFAULT)

    return props

class Data:
    AddTitleBool = None
    OutputDir = None
    Extension = None
    ExtensionMask = None

class File:
    def __init__(self):
        self.dataExtension = '.' + Data.Extension
        self.path = find_latest_file(Data.OutputDir, '\*')
        self.title = get_window_title()

        self.dir = os.path.dirname(self.path)
        self.rawfile = os.path.basename(self.path)
        self.file = self.rawfile[:-len(self.dataExtension)] + self.dataExtension

        self.newFolder = self.dir + '\\' + self.title

        if Data.AddTitleBool is True:
            self.newfile = self.title + ' - ' + self.file
        else:
            self.newfile = self.file

    def get_oldPath(self):
        return self.dir +'\\'+ self.file
    def get_newPath(self):
        return self.newFolder + '\\' + self.newfile
    
    def create_new_folder(self):
        if not os.path.exists(self.newFolder):
            os.makedirs(self.newFolder)

    def remember_and_move(self):
        oldPath = self.dir +'\\'+ self.file
        newPath = self.newFolder + '\\' + self.newfile
        textFile = (oldPath[:-3] + "txt")

        f = open(oldPath[:-3]+"txt", "w")
        f.write(newPath)
        f.close()

        shutil.move(oldPath, newPath)
        os.remove(textFile)