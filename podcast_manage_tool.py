import podcast_manage_tool_funcs as func

func.validateFileStructure()

cont = True
while cont:
  messages = [
    ("Add a video to an existing feed", func.downloadVideo),
    ("Add a playlist to an existing feed - IN PROGRESS", func.downloadPlaylist),
    ("Download URLS in 'batchURLs.txt' to 'Misc Stuff'", func.downloadBatchURLs),
    ("Update a specific podcast feed now", func.updateFeed),
    ("Create a new podcast", func.addNewPodcast),
    ("Spread an array of audio files over a time frame", func.datespreadFiles),
    ("Rename, log, and move contents of 'videos' folder", func.processDownloads),
    ("Exit",) # This must be the last option
  ]
  # Print all messages
  for i,j in enumerate(messages):
    print(f"{i+1}: {j[0]}")
  option = input("Pick an option: ")

  # March selection to function
  if option in [str(x) for x in range(1, len(messages)+1)]:
    if option == str(len(messages)):
      # if selection is a valid number AND the last number, exit
      break
    else:
      messages[int(option)-1][1]()
  else:
    func.printFatalError("invalid selection")

  cont = input("Press Enter to exit or enter 'Y' to go back to the menu: ")
  if cont not in ["y", "Y"]:
    cont = False
