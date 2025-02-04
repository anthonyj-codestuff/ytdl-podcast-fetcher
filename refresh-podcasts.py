import subprocess
import funcs as funcs
import funcs_core as corefuncs
import constants as c

# Set this to True while working on the script to stop it from running

DISABLED = False

# Do not run if there is another process running
# TODO: If for some reason this file is not deleted after a run, the tool will never run again
if funcs.checkLockfile():
  DISABLED = True

if not DISABLED:
  # lock the program
  funcs.createLockfile()
  ## TODO: Pre-check justcast folders and make sure all destination folders exist
  ## TODO: Create destination folders if they don't exist?
  print("Step 0: Validate files and folders")
  funcs.validateFileStructure()
  if not c.Config.get("FILES_VALIDATED"):
    log = f"Folder structure failed validation: [{c.Config.printErrors()}]"
    funcs.appendToTextFile(log, c.LOG_FILEPATH)
    funcs.deleteLockfile()
    # exit
  else:
    ## Command takes 4 parameters
    ## 0 = Script path
    ## 1 = Title (make sure there's a folder with this name waiting at DEST_DIR)
    ## 2 = The playlist ID from youtube
    ## 3 = OPTIONAL A list of terms to exclude from download.
    ##     These videos will not be added to the archive, so removing a term will
    ##     cause those videos to be downloaded next time. Delimit all terms with "|"
    ## TODO: Refactor this into powershell scripts. Batch files don't throw errors
    print("Step 1: Downloading and converting new files")
    subprocess.run([c.SCRIPT_UPDATE_YTDL])
    playlistConfigs = corefuncs.parseConfigFile(c.PLAYLIST_CONFIG_FILEPATH)
    for x in playlistConfigs:
      corefuncs.downloadVideosByPlaylistId(x[0], x[1], x[2], x[3])
    usernameConfigs = corefuncs.parseConfigFile(c.USERNAME_CONFIG_FILEPATH)
    for x in usernameConfigs:
      corefuncs.downloadVideosByUsername(x[0], x[1], x[2], x[3])

    print("Step 2: Reformatting file names")
    funcs.cleanFilenames(c.VIDEOS_DIR)
    #TODO: Check for temp files and stray webp files, consider removing these files from the archive?

    listOfFiles = funcs.getFiles(c.VIDEOS_DIR)
    print("Step 3: Moving " + str(len(listOfFiles)) + " files to Dropbox\n")
    funcs.moveFilesToDestination(c.VIDEOS_DIR, c.LOG_FILEPATH, c.Config.get("DEST_DIR"))

    print("Step 4: Logging new files")
    funcs.logAllFiles(c.VIDEOS_DIR, c.LOG_FILEPATH)

    print("Step 5: Deleting local episodes")
    funcs.deleteFiles(c.VIDEOS_DIR)

    print("done")
    funcs.deleteLockfile()
else:
  print("podcast fetcher is disabled. Exiting.")
