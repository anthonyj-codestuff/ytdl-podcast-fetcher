import podcast_manage_tool_funcs as func 

cont = True
while cont:
  print("1: Add a video to an existing feed")
  print("2: Add a playlist to an existing feed - IN PROGRESS")
  print("3: Download URLS in 'batchURLs.txt' to 'Misc Stuff'")
  print("4: Create a new podcast")
  print("5: Update a specific podcast feed now")
  print("6: Spread an array of audio files over a time frame")
  print("7: Rename, log, and move videos folder")
  print("8: Exit")
  option = input("Pick an option: ")

  if option == "1":
    func.downloadVideo()
  elif option == "2":
    func.downloadPlaylist()
  elif option == "3":
    func.downloadBatchURLs()
  elif option == "4":
    func.addNewPodcast()
  elif option == "5":
    func.updateFeed()
  elif option == "6":
    func.datespreadFiles()
  elif option == "7":
    func.processDownloads()
  elif option == "8":
    break
  else:
    func.printFatalError("invalid selection")

  cont = input("Press Enter to exit or enter 'Y' to go back to the menu: ")
  if cont not in ["y", "Y"]:
    cont = False
