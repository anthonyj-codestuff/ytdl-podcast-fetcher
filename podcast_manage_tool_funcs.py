import subprocess
import os
import re
from datetime import datetime, timedelta
import math
from decimal import Decimal
import funcs as funcs
import funcs_core as corefuncs
import constants as c

##################
## Download Video

def downloadVideo():
  printOptionHeader("Download Video to Existing Feed")
  urlIsValid = False
  rUrlForms = '^((?:https?:\/\/)?)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
  folderNames = next(os.walk(c.Config.get("DEST_DIR")))[1]
  while not urlIsValid:
    videoUrl = input("Input video to download: ")
    if not re.match(rUrlForms, videoUrl):
      print("This URL does not match Youtube format")
    else:
      urlIsValid = True
  for index, file in enumerate(folderNames):
    print(index, file)
  print()
  folderIsValid = False
  while not folderIsValid:
    folderSelection = input("Select a folder for this video: ")
    if not folderSelection.isnumeric() or not 0 <= int(folderSelection) < len(folderNames):
      print("This is not a valid selection")
    else:
      folderIsValid = True

  customDate = ""
  customDateSelect = input("use a custom date? y/N: ")
  if customDateSelect in ["y", "Y"]:
    isValid = False
    while not isValid:
      customDate = input("Input the date to use (format: MMDDYYYY): ")
      if re.match('^[01][0-9][01][0-9][12][0-9]{3}$', customDate):
        isValid = True
      else:
        print("This is not a valid date")
  else:
    print("Using existing upload date as publish date")

  print(f"You have selected:\n\t{folderNames[int(folderSelection)]}")
  if customDate:
    print(f"\tCustom date _pd_{customDate}")
  input("Press Enter to continue...")
  if videosFolderFileCount() > 0:
    printFatalError(f"Expected 0 files in \\videos, found {str(videosFolderFileCount())}")
    return
  # download the video, embed data, skip playlists
  if funcs.checkLockfile():
    print("lockfile is present.  Please check that the update script is not running and try again")
  else:
    subprocess.run([c.SCRIPT_UPDATE_YTDL])
    funcs.createLockfile()
    subprocess.run([
      c.YTDL_PATH,
      "-o",
      os.path.join(c.VIDEOS_DIR, folderNames[int(folderSelection)], "%(title)s_pd_%(upload_date>%m%d%Y)s.%(ext)s"),
      "-f",
      "bestaudio[ext=m4a]",
      "--add-metadata",
      "--embed-thumbnail",
      "--no-playlist",
      videoUrl,
      "--download-archive",
      os.path.join(c.PATH, "archive.txt"),
      "--extractor-args", "youtube:player-skip=js",
      "--sponsorblock-remove", "intro,outro,sponsor,selfpromo,preview,interaction,music_offtopic"
    ])
    # at this point, we have one video waiting in the videos folder
    # if we do NOT have one file waiting, something is wrong or the updater has started running
    if videosFolderFileCount() > 1:
      print("ERROR: Unexpected number of files. Updater may have started running since download began")
      printFatalError("Expected 1 files in \\videos, found " + str(videosFolderFileCount()))
      return
    
    # if a custom date was selected, rename the file
    if customDate:
      videoArr = funcs.getFiles(os.path.join(c.VIDEOS_DIR, folderNames[int(folderSelection)]))
      videoFilepath = videoArr[0]
      videoLocation = os.path.dirname(videoFilepath)
      videoFilename = os.path.basename(videoFilepath)
      videoFilenameNew = re.sub(r"_pd_\d{8}", f"_pd_{customDate}", videoFilename)
      old = videoFilepath
      new = os.path.join(videoLocation, videoFilenameNew)
      os.rename(old, new)

    corefuncs.processAudioFiles()
    print("done")
    return

#####################
## Download Playlist - TODO

def downloadPlaylist():
  printOptionHeader("Download Playlist to Existing Feed")
  printFatalError("this option is not ready yet")
  return

#####################
## Download Batch URLs

def downloadBatchURLs():
  printOptionHeader("Download Custom URLs to Misc Feed")
  if funcs.checkLockfile():
    print("lockfile is present.  Please check that the update script is not running and try again")
  else:
    funcs.createLockfile()
    corefuncs.downloadMiscVideoList()
    corefuncs.processAudioFiles()
    print("done")
  return

###################
## Add New Podcast - TODO Double-check this
patternPlaylist = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/playlist\?list=(.+)$'
patternUsername = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/@(.+)$'
def addNewPodcast():
  printOptionHeader("Add new Podcast Feed")
  feedNameIn = input("Paste new channel URL: ")
  # get playlist ID or username if they exist
  gotYTPlaylist = re.search(patternPlaylist, feedNameIn).group(3) if re.search(patternPlaylist, feedNameIn) else ""
  gotYTUsername = re.search(patternUsername, feedNameIn).group(3) if re.search(patternUsername, feedNameIn) else ""
  if not gotYTPlaylist and not gotYTUsername:
    print("This URL must match either a playlist or a profile.")
    return
  # check for existing playlist
  if gotYTPlaylist:
    key = gotYTPlaylist
    configs = corefuncs.parseConfigFile(c.PLAYLIST_CONFIG_FILEPATH)
    configFile = c.PLAYLIST_CONFIG_FILEPATH
  elif gotYTUsername:
    key = gotYTUsername
    configs = corefuncs.parseConfigFile(c.USERNAME_CONFIG_FILEPATH)
    configFile = c.USERNAME_CONFIG_FILEPATH

  # check if this id already exists in the config
  for i in configs:
    if i[1] == key:
      printFatalError("This podcast already exists in config file. Skipping")
      return
  
  # new podcast is not already configured. Get other inputs
  podName = funcs.getValidatedInput("Name of this podcast? (does not affect functionality if you specify a folder later) ", r'^[\w\-. ]+$')
  # TODO Double-check this. It should not accept weird |s
  podRejectPrase = funcs.getValidatedInput("Discard files containing phrases (delimit with | or leave blank): ", r'^$|^(?:[^\|]+\|)*[^\|]+$')
  podMaxSeconds = funcs.getValidatedInput("Maximum number of seconds per episode? ", r'^$|^(?!0\d+)\d+$')
  podFolder = funcs.getValidatedInput("Which folder will this podcast go in? (blank defaults to podcast name) ", r'^[\w\-. ]*$')
  if not podFolder:
    podFolder = podName

  # Write new pod configuration to file
  toAppendLine = f"{podFolder},{key},{podRejectPrase},{podMaxSeconds},{podName}"
  funcs.appendToTextFile(toAppendLine, configFile, False)

  # Create new Dropbox folder if needed
  dir = os.path.join(c.Config.get("DEST_DIR"), podFolder)
  if not os.path.exists(dir):
      os.makedirs(dir)
      print(f"New folder \"{podFolder}\" created")

  
  input("Press Enter to continue (process will be locked while the new podcast downloads)")
  # download the new podcast as normal
  if funcs.checkLockfile():
    print("lockfile is present.  Please check that the update script is not running and try again")
  else:
    subprocess.run([c.SCRIPT_UPDATE_YTDL]) #TODO Why is this a regex string?
    funcs.createLockfile()
    if gotYTPlaylist:
      corefuncs.downloadVideosByPlaylistId(podFolder, key, podRejectPrase, podMaxSeconds, True)
    else:
      corefuncs.downloadVideosByUsername(podFolder, key, podRejectPrase, podMaxSeconds, True)

    if videosFolderFileCount() < 1:
      funcs.deleteLockfile()
      print("No videos found, if this is unexpected, consult the following debug information")
      print(f"Feed Name Input: {feedNameIn}")
      print(f"Got YT Playlist: {gotYTPlaylist}")
      print(f"Got YT Username: {gotYTUsername}")
      print(f"Pod Name:        {podName}")
      print(f"Pod RejectPrase: {podRejectPrase}")
      print(f"Pod MaxSeconds:  {podMaxSeconds}")
      print(f"Pod Folder:      {podFolder}")
      return
    corefuncs.processAudioFiles()

    print("\nCOMPLETE! No problems were detected creating your new feed.")
    print("To complete this feed, you must still")
    print("1. Save a 1400x1400 logo in the JustCast control panel")
    print("2. Set the JustCast feed to Private")
    print("3. Subscribe to the new feed")
    return

###############
## Update Feed

def updateFeed():
  printOptionHeader("Update Podcast Feed")
  # get all current podcast feeds
  playlistNames = []
  playlistConfigs = corefuncs.parseConfigFile(c.PLAYLIST_CONFIG_FILEPATH)
  for x in playlistConfigs:
    playlistNames.append(x[4])
  usernameConfigs = corefuncs.parseConfigFile(c.USERNAME_CONFIG_FILEPATH)
  for x in usernameConfigs:
    playlistNames.append(x[4])
  # print all podcast feeds
  for index, file in enumerate(playlistNames):
    print(index, file)
  # ask user for selection
  folderIsValid = False
  while not folderIsValid:
    folderSelectionNum = input("Select a feed to refresh: ")
    if not folderSelectionNum.isnumeric() or not 0 <= int(folderSelectionNum) < len(playlistNames):
      print("This is not a valid selection")
    else:
      folderIsValid = True
  # todo ???
  isPlaylist = int(folderSelectionNum) < len(playlistConfigs)
  if isPlaylist:
    folderSelectionConfig = playlistConfigs[int(folderSelectionNum)]
  else:
    folderSelectionConfig = usernameConfigs[int(folderSelectionNum)-len(playlistConfigs)]
  print("You have selected: " + folderSelectionConfig[4])
  input("Press Enter to continue...")
  
  if videosFolderFileCount() > 0:
    printFatalError("Expected 0 files in \\videos, found " + str(videosFolderFileCount()))
    return

  if funcs.checkLockfile():
    print("lockfile is present.  Please check that the update script is not running and try again")
  else:
    subprocess.run([c.SCRIPT_UPDATE_YTDL])
    funcs.createLockfile()
    if isPlaylist:
      corefuncs.downloadVideosByPlaylistId(folderSelectionConfig[0], folderSelectionConfig[1], folderSelectionConfig[2], folderSelectionConfig[3])
    else:
      corefuncs.downloadVideosByUsername(folderSelectionConfig[0], folderSelectionConfig[1], folderSelectionConfig[2], folderSelectionConfig[3])

    if videosFolderFileCount() < 1:
      funcs.deleteLockfile()
      return
    funcs.cleanFilenames(c.VIDEOS_DIR)
    funcs.moveFilesToDestination(c.VIDEOS_DIR, c.LOG_FILEPATH, c.Config.get("DEST_DIR"))
    funcs.logAllFiles(c.VIDEOS_DIR, c.LOG_FILEPATH)
    funcs.deleteFiles(c.VIDEOS_DIR)
    funcs.deleteLockfile()
    return

####################
## Datespread Files

def validateFilenames(files):
  filesNotPassedNameCheck = []
  numPassedNameCheck = 0
  
  ## count files that match the title format
  for file in files:
    if re.match('^[0-9]{8}-.*$', file):
      numPassedNameCheck += 1
    else:
      filesNotPassedNameCheck.append(file)
  print(''.join([str(numPassedNameCheck), "/", str(len(files)), " files passed name check"]))

  if numPassedNameCheck != len(files):
    print("\nPlease fix the filenames of the following files")
    for file in filesNotPassedNameCheck:
      print(file)
    printFatalError("Files should conform to 'YYYYMMDD-NAME'")
    return False
  else:
      return True

def validateDate(str):
  if not re.match('^[0-9]{8}$', str):
    printFatalError("Date format is invalid")
    return False
  try:
    datetime(int(str[0:4]),int(str[4:6]),int(str[6:8]))
  except ValueError as e:
    printFatalError(e)
    return False
  return True

def datespreadFiles():
  printOptionHeader("Date-Spread Files")
  filesForDatespread = os.listdir(c.AUDIO_PROCESSING_DIR)
  print("Found", len(filesForDatespread), "files to be processed")

  if len(filesForDatespread) < 1:
    printFatalError("Need at least 1 file in " + c.AUDIO_PROCESSING_DIR)
    return
  # Get and validate input
  success = validateFilenames(filesForDatespread)
  if success == False:
      return
  startStr = input("Start Date (YYYYMMDD): ")
  if not validateDate(startStr):
    return
  endStr = input("End Date (YYYYMMDD): ")
  if not validateDate(endStr):
    return
  startDate = datetime(int(startStr[0:4]),int(startStr[4:6]),int(startStr[6:8]))
  endDate = datetime(int(endStr[0:4]),int(endStr[4:6]),int(endStr[6:8]))
  daysTotal = (endDate - startDate).days + 1
  if daysTotal <= 0:
    printFatalError("Start date must be earlier than end date")
    return
  if daysTotal < len(filesForDatespread):
    printFatalError("Time frame must allow for at least one day per file")
    # TODO Maybe add a block here to change to a valid end date
    return
  
  # split up time delta into equal chunks, set date to floor(increment)
  L = daysTotal
  n = len(filesForDatespread)
  p = Decimal(str((L-1)/(n-1))) # point-inclusive distribution formula
  dateArray = []
  value = Decimal('0.0')
  for i in range(n):
    dateArray.append((startDate + timedelta(days=math.floor(value))).strftime("%m%d%Y"))
    value += p

  # rename files
  print(str(len(dateArray)), "dates queued up.")
  print(str(len(filesForDatespread)), "files ready to rename")

  if(len(filesForDatespread) != len(dateArray)):
    print("L =", str(L), "days")
    print("n =", str(n), "files")
    print("p =", str(n), "period")
    printFatalError("The date spread algorithm has produced an incorrect number of dates. Fix the algorithm or change the start/end dates")
    return

  print("Dates range from", dateArray[0], "to", dateArray[-1])
  proceed = input("Proceed? Y/N: ")
  if proceed not in ["y", "Y"]:
    print("quitting")
    return
  else:
    # User has committed to renaming. Re-validate files just in case things have changed
    filesForValidation = os.listdir(c.AUDIO_PROCESSING_DIR)
    success = validateFilenames(filesForValidation)
    if success == False or not filesForValidation == filesForDatespread:
      printFatalError("File structure was changed prior to renaming. Please do not change files that are being operated on")
      return

    for i in range(len(filesForDatespread)):
      date = dateArray[i]
      file = filesForDatespread[i]
      extDotIndex = file.rfind(".")

      extStr = file[extDotIndex:]
      file = file[0:extDotIndex]
      file = file[9:]
      file = file + "_pd_" + date + extStr
      old = os.path.join(c.AUDIO_PROCESSING_DIR, filesForDatespread[i])
      new = os.path.join(c.AUDIO_PROCESSING_DIR, file)
      print(filesForDatespread[i], "->", file)
      os.rename(old, new)
    print("Files renamed")

##################
## Process Videos

def processDownloads():
  funcs.createLockfile()
  printOptionHeader(f"Process Downloads\n(this will manually handle the files in {c.VIDEOS_DIR})")
  print("\nFound {} files in \\videos".format(str(videosFolderFileCount())))

  if videosFolderFileCount() > 0:
    option = input("Clean file names (emojis, etc)? Y/n: ")
    if option not in ["n", "N"]:
      funcs.cleanFilenames(c.VIDEOS_DIR)

    option = input("Copy audio files to Dropbox? Y/n: ")
    if option not in ["n", "N"]:
      funcs.moveFilesToDestination(c.VIDEOS_DIR, c.LOG_FILEPATH, c.Config.get("DEST_DIR"))

    option = input("Log files? Y/n: ")
    if option not in ["n", "N"]:
      funcs.logAllFiles(c.VIDEOS_DIR, c.LOG_FILEPATH)

    option = input("Delete audio files? Y/n: ")
    if option not in ["n", "N"]:
      funcs.deleteFiles(c.VIDEOS_DIR)
  funcs.deleteLockfile()
  return

#########
## Utils

def printFatalError(str):
  print("\nError:", str)
  input("Press Enter to continue")

def printOptionHeader(str):
  print("\n============================")
  print(str)
  print("============================")

def videosFolderFileCount():
  fileCount = 0
  for (root, dirs, file) in os.walk(c.VIDEOS_DIR):
    if file:
      fileCount += len(file)
  return fileCount
