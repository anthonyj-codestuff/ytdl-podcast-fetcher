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