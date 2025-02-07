import os

# directories
PATH = os.path.dirname(os.path.realpath(__file__))
VIDEOS_DIR = os.path.join(PATH, "videos")
AUDIO_PROCESSING_DIR = os.path.join(PATH, "audio-processing")
METADATA_DIR = os.path.join(PATH, "metadata")
# scripts
SCRIPT_UPDATE_YTDL = os.path.join(PATH, "UpdateYTDL.bat")
# configs
FETCHER_CONFIG_FILEPATH = os.path.join(PATH, "config_fetcher.txt")
PLAYLIST_CONFIG_FILEPATH = os.path.join(PATH, "config_pods_playlist.txt")
USERNAME_CONFIG_FILEPATH = os.path.join(PATH, "config_pods_username.txt")
CHERRYPICK_CONFIG_FILEPATH = os.path.join(PATH, "config_pods_cherrypick.txt")
BATCH_URLS_FILEPATH = os.path.join(PATH, "batchURLs.txt")
# output files
LOG_FILEPATH = os.path.join(PATH, "episode-log.txt")
ARCHIVE_FILEPATH = os.path.join(PATH, "archive.txt")

class fonts:
  BOLD = '\033[1m'
  ITALIC = '\033[3m'
  ULINE = '\033[4m'
  INVERT = '\033[7m'
  STRIKE = '\033[9m'
  RESET = '\033[0m'

  GREY = '\033[90m'
  RED = '\033[91m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  BLUE = '\033[94m'
  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  WHITE = '\033[97m'

  BACKBLACK = '\033[40m' #\m/
  BACKGREY = '\033[100m'
  BACKPURPLE = '\033[45m'
  BACKWHITE = '\033[47m'
  BACKBLUE = '\033[44m' #ew
  BACKYELLOW = '\033[43m'
  BACKRED = '\033[41m'
  BACKGREEN = '\033[42m'
  BACKCYAN = '\033[46m'

validFonts = [ #(F,B) Organized to be as distinguishable as possible
  (0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),
  (7,0),(4,8),(0,5),(3,3),(4,2),(3,7),(0,6),
  (0,4),(2,2),(5,8),(1,5),(4,3),(6,2),(4,7),
  (6,4),(7,2),(3,8),(5,3),(5,2),(6,6),(5,7),
  (3,2),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)
]

class Config:
  _instance = None
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(Config, cls).__new__(cls)
      cls._instance.__defaults = {
        # state
        "YTDL_FOUND": False,
        "FFMPEG_FOUND": False,
        "DESTINATION_FOUND": False,
        "FILES_VALIDATED": False,
        "VALIDATION_ERRORS": [],
        # directories
        "DEST_DIR": "", # Set at runtime from config file
        # programs
        "YTDL_PATH": "", # Set at runtime from config file, can be set to %PATH% if it exists
        "FFMPEG_PATH": "", # Set at runtime from config file, can be set to %PATH% if it exists
        # other configs
        "LOCKFILE_MAX_AGE_SECONDS": 60 * 60 * 6
      }
    return cls._instance
  
  def get(self, key: str, default_value=None):
    return self.__defaults.get(key, default_value)

  def set(self, key: str, value):
    self.__defaults[key] = value
  
  def addError(self, value):
    self.__defaults["VALIDATION_ERRORS"].append(value)

  def hasErrors(self):
    return len(self.__defaults["VALIDATION_ERRORS"]) > 0
  
  def printErrors(self):
    message = ", ".join(self.__defaults["VALIDATION_ERRORS"])
    return message
Config = Config()