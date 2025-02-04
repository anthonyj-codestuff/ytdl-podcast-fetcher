import subprocess
import constants as c
import funcs as funcs

def downloadVideosByPlaylistId(podName, listId, reject, maxDuration, overridePLLen=False):
    args = [
        c.Config.get("YTDL_PATH"),
        "-c",
        "-i",
        "-R", "3",
        "-o", c.VIDEOS_DIR + "\\" + podName + "\\%(title)s_pd_%(upload_date>%m%d%Y)s.%(ext)s",
        "-f", "bestaudio[ext=m4a]",
        "--match-filter", "!is_live",
        "--reject-title", reject,
        "--add-metadata",
        "--embed-thumbnail",
        "--yes-playlist",
        "https://www.youtube.com/playlist?list=" + listId,
        "--download-archive", c.ARCHIVE_FILEPATH,
        "--sponsorblock-remove", "intro,outro,sponsor,selfpromo,preview,interaction,music_offtopic",
        "--sleep-requests", "1.5",
        "--min-sleep-interval", "15",
        "--max-sleep-interval", "30"
    ]
    if not overridePLLen:
        args.append("--playlist-end")
        args.append("50")
    if maxDuration and int(maxDuration) > 0:
        args.append("--match-filter")
        args.append("duration<{}".format(maxDuration))
    try:
        subprocess.run(args)
        print()
    except Exception as e:
        print(e)
        input("Press Enter to exit")

def downloadVideosByUsername(podName, username, reject, maxDuration, overridePLLen=False):
    args = [
        c.Config.get("YTDL_PATH"),
        "-c",
        "-i",
        "-R", "3",
        "-o", c.VIDEOS_DIR + "\\" + podName + "\\%(title)s_pd_%(upload_date>%m%d%Y)s.%(ext)s",
        "-f", "bestaudio[ext=m4a]",
        "--match-filter", "!is_live",
        "--reject-title", reject,
        "--add-metadata",
        "--embed-thumbnail",
        "--yes-playlist",
        "https://www.youtube.com/@" + username,
        "--download-archive", c.ARCHIVE_FILEPATH,
        "--sponsorblock-remove", "intro,outro,sponsor,selfpromo,preview,interaction,music_offtopic",
        "--sleep-requests", "1.5",
        "--min-sleep-interval", "15",
        "--max-sleep-interval", "30"
    ]
    if not overridePLLen:
        args.append("--playlist-end")
        args.append("50")
    if maxDuration and int(maxDuration) > 0:
        args.append("--match-filter")
        args.append("duration<{}".format(maxDuration))
    try:
        subprocess.run(args)
    except Exception as e:
        print(e)
        input("Press Enter to exit")

def downloadMiscVideoList():
    args = [
        c.Config.get("YTDL_PATH"),
        "-c",
        "-i",
        "-R", "3",
        "--batch-file", c.BATCH_URLS_FILEPATH,
        "-o", c.VIDEOS_DIR + "\\Misc Stuff\\%(title)s_pd_%(upload_date>%m%d%Y)s.%(ext)s",
        "-f", "bestaudio[ext=m4a]",
        "--add-metadata",
        "--embed-thumbnail",
        "--download-archive", c.ARCHIVE_FILEPATH,
        "--sponsorblock-remove", "intro,outro,sponsor,selfpromo,preview,interaction,music_offtopic",
        "--sleep-requests", "1.5",
        "--min-sleep-interval", "5",
        "--max-sleep-interval", "30"
    ]
    try:
        subprocess.run(args)
    except Exception as e:
        print(e)
        input("Press Enter to exit")

def parseConfigFile(filepath):
    parsed = []
    Lines = open(filepath, "r", encoding="utf-8")
    for line in Lines:
        if line and line[0] != "#":
            parsed.append(line.strip().split(","))
    return parsed

def processAudioFiles():
    funcs.cleanFilenames(c.VIDEOS_DIR)
    funcs.moveFilesToDestination(c.VIDEOS_DIR, c.LOG_FILEPATH, c.Config.get("DEST_DIR"))
    funcs.logAllFiles(c.VIDEOS_DIR, c.LOG_FILEPATH)
    funcs.deleteFiles(c.VIDEOS_DIR)
    funcs.deleteLockfile()