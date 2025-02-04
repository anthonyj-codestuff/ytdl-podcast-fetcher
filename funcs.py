import os
import re
import shutil
import time
from datetime import datetime #TODO convert this to time
import emoji
import funcs_core as corefuncs
import constants as c

## Lockfile management
def createLockfile():
    file = os.path.join(c.PATH, "lockfile")
    if not os.path.isfile(file):
        open(file, 'a').close()

def deleteLockfile():
    file = os.path.join(c.PATH, "lockfile")
    if os.path.isfile(file):
        os.remove(file)
        
def checkLockfile():
    file = os.path.join(c.PATH, "lockfile")
    if not os.path.isfile(file):
        return False
    else:
        ageSeconds = time.time() - os.path.getmtime(file)
        appendToTextFile("INFO: Lockfile age: " + str(ageSeconds) + " seconds", c.LOG_FILEPATH)
        if ageSeconds > c.Config.get("LOCKFILE_MAX_AGE_SECONDS"):
            appendToTextFile("WARN: Lockfile has exceeded configured max age. Deleting to free up process", c.LOG_FILEPATH)
            deleteLockfile()
        return True


## Misc

def validateFileStructure():
    # Check and set YTDL
    # Check and set FFMPEG
    # Check and set DEST
    # check for "Misc Stuff" within DEST
    # Check for "audio-processing" or create it
    # Check for "videos" or create it
    # Check for "metadata" or create it
    # Check for all configs or create
    # Check for batchURLs or touch
    # Check for archive or touch
    # Check for episode-log or touch
    ytdlPath = shutil.which("yt-dlp") or shutil.which("yt-dl")
    ffmpegPath = shutil.which("ffmpeg")
    configOptions = corefuncs.parseConfigFile(c.FETCHER_CONFIG_FILEPATH)
    for i in configOptions:
        if(i[0] == "YTDL_PATH"):
            ytdl = i[1]
            if(os.path.isfile(ytdl)):
                c.Config.set("YTDL_PATH", ytdl)
                c.Config.set("YTDL_FOUND", True)
            elif(os.path.isfile(ytdlPath)):
                c.Config.set("YTDL_PATH", ytdlPath)
                c.Config.set("YTDL_FOUND", True)
        if(i[0] == "FFMPEG_PATH"):
            ffmpeg = i[1]
            if(os.path.isfile(ytdl)):
                c.Config.set("FFMPEG_PATH", ffmpeg)
                c.Config.set("FFMPEG_FOUND", True)
            elif(os.path.isfile(ytdlPath)):
                c.Config.set("FFMPEG_PATH", ffmpegPath)
                c.Config.set("FFMPEG_FOUND", True)
        if(i[0] == "DEST_DIR"):
            dest = i[1]
            if(os.path.isdir(dest)):
                c.Config.set("DEST_DIR", dest)
                c.Config.set("DESTINATION_FOUND", True)

    #TODO Finish this
    if not c.Config.get("YTDL_FOUND"):
        c.Config.addError("Could not find ytdl")
    if not c.Config.get("FFMPEG_FOUND"):
        c.Config.addError("Could not find ffmpeg")
    if not c.Config.get("DESTINATION_FOUND"):
        c.Config.addError("Could not find destination dir")
    if not c.Config.hasErrors():
        c.Config.set("FILES_VALIDATED", True)
    return

def getFiles(dirName):
    listOfFile = os.listdir(dirName)
    completeFileList = list()
    for file in listOfFile:
        completePath = os.path.join(dirName, file)
        if os.path.isdir(completePath):
            completeFileList = completeFileList + getFiles(completePath)
        else:
            completeFileList.append(completePath)

    return completeFileList

def getValidatedInput(prompt, validator):
    while True:
        userInput = input(prompt)
        if re.match(validator, userInput):
            return userInput
        else:
            print("Input does not meet requirements")


## filename cleanup

def replaceUnicodeSymbols(token, text, unicodeArr):
    for i in unicodeArr:
        text = text.replace(i, token)
    return text

def removeEmojisFromText(text):
    ## uses special library to find and delete all emojis from text
    return emoji.demojize(text, version=0)

def cleanUpWhitespace(text):
    ## finds consecutive or outer whitespace and trims it down to one space
    return re.sub('\s+', ' ', text).strip()

def cleanUpAlphanum(text):
    ## not terribly robust. this finds letters in the Bold Mathematical Alphanumeric
    ## Symbols block and replaces them with their ASCII counterpart
    text = replaceUnicodeSymbols('a', text, ['\U0001D41A','\U0001D44E','\U0001D482','\U0001D4B6','\U0001D4EA','\U0001D552','\U0001D586','\U0001D5BA','\U0001D5EE','\U0001D622','\U0001D656','\U0001D68A','\U0001D6C2','\U0001D6FC','\U0001D736','\U0001D770','\U0001D7AA','\U000000E0','\U000000E1','\U000000E2','\U000000E3','\U000000E4','\U000000E5'])
    text = replaceUnicodeSymbols('b', text, ['\U0001D41B','\U0001D44F','\U0001D483','\U0001D4B7','\U0001D4EB','\U0001D553','\U0001D587','\U0001D5BB','\U0001D5EF','\U0001D623','\U0001D657','\U0001D68B'])
    text = replaceUnicodeSymbols('c', text, ['\U0001D41C','\U0001D450','\U0001D484','\U0001D4B8','\U0001D4EC','\U0001D554','\U0001D588','\U0001D5BC','\U0001D5F0','\U0001D624','\U0001D658','\U0001D68C','\U000000E7'])
    text = replaceUnicodeSymbols('d', text, ['\U0001D41D','\U0001D451','\U0001D485','\U0001D4B9','\U0001D4ED','\U0001D555','\U0001D589','\U0001D5BD','\U0001D5F1','\U0001D625','\U0001D659','\U0001D68D','\U0001D6C5','\U0001D6FF','\U0001D739','\U0001D773','\U0001D7AD','\U0001D6DB','\U0001D715','\U0001D74F','\U0001D789','\U0001D7C3','\U00002146'])
    text = replaceUnicodeSymbols('e', text, ['\U0001D41E','\U0001D452','\U0001D486','\U0001D4EE','\U0001D556','\U0001D58A','\U0001D5BE','\U0001D5F2','\U0001D626','\U0001D65A','\U0001D68E','\U0000212E','\U0000212F','\U00002147','\U000000E8','\U000000E9','\U000000EA','\U000000EB'])
    text = replaceUnicodeSymbols('f', text, ['\U0001D41F','\U0001D453','\U0001D487','\U0001D4BB','\U0001D4EF','\U0001D557','\U0001D58B','\U0001D5BF','\U0001D5F3','\U0001D627','\U0001D65B','\U0001D68F','\U0001D7CB'])
    text = replaceUnicodeSymbols('g', text, ['\U0001D420','\U0001D454','\U0001D488','\U0001D4F0','\U0001D558','\U0001D58C','\U0001D5C0','\U0001D5F4','\U0001D628','\U0001D65C','\U0001D690','\U0000210A'])
    text = replaceUnicodeSymbols('h', text, ['\U0001D421','\U0000210E','\U0001D489','\U0001D4BD','\U0001D4F1','\U0001D559','\U0001D58D','\U0001D5C1','\U0001D5F5','\U0001D629','\U0001D65D','\U0001D691','\U0000210E','\U0000210F'])
    text = replaceUnicodeSymbols('i', text, ['\U0001D422','\U0001D456','\U0001D48A','\U0001D4BE','\U0001D4F2','\U0001D55A','\U0001D58E','\U0001D5C2','\U0001D5F6','\U0001D62A','\U0001D65E','\U0001D692','\U0001D6A4','\U00002148','\U00002129','\U00002139','\U000000EC','\U000000ED','\U000000EE','\U000000EF'])
    text = replaceUnicodeSymbols('j', text, ['\U0001D423','\U0001D457','\U0001D48B','\U0001D4BF','\U0001D4F3','\U0001D55B','\U0001D58F','\U0001D5C3','\U0001D5F7','\U0001D62B','\U0001D65F','\U0001D693','\U0001D6A5','\U00002149'])
    text = replaceUnicodeSymbols('k', text, ['\U0001D424','\U0001D458','\U0001D48C','\U0001D4C0','\U0001D4F4','\U0001D55C','\U0001D590','\U0001D5C4','\U0001D5F8','\U0001D62C','\U0001D660','\U0001D694','\U0001D6CB','\U0001D705','\U0001D73F','\U0001D779','\U0001D7B3'])
    text = replaceUnicodeSymbols('l', text, ['\U0001D425','\U0001D459','\U0001D48D','\U0001D4C1','\U0001D4F5','\U0001D55D','\U0001D591','\U0001D5C5','\U0001D5F9','\U0001D62D','\U0001D661','\U0001D695','\U00002113'])
    text = replaceUnicodeSymbols('m', text, ['\U0001D426','\U0001D45A','\U0001D48E','\U0001D4C2','\U0001D4F6','\U0001D55E','\U0001D592','\U0001D5C6','\U0001D5FA','\U0001D62E','\U0001D662','\U0001D696'])
    text = replaceUnicodeSymbols('n', text, ['\U0001D427','\U0001D45B','\U0001D48F','\U0001D4C3','\U0001D4F7','\U0001D55F','\U0001D593','\U0001D5C7','\U0001D5FB','\U0001D62F','\U0001D663','\U0001D697','\U0001D6C8','\U0001D702','\U0001D73C','\U0001D776','\U0001D7B0','\U000000F1'])
    text = replaceUnicodeSymbols('o', text, ['\U0001D428','\U0001D45C','\U0001D490','\U0001D4F8','\U0001D560','\U0001D594','\U0001D5C8','\U0001D5FC','\U0001D630','\U0001D664','\U0001D698','\U0001D6D0','\U0001D70A','\U0001D744','\U0001D77E','\U0001D7B8','\U00002134','\U000000F0','\U000000F2','\U000000F3','\U000000F4','\U000000F5','\U000000F6','\U000000F8'])
    text = replaceUnicodeSymbols('p', text, ['\U0001D429','\U0001D45D','\U0001D491','\U0001D4C5','\U0001D4F9','\U0001D561','\U0001D595','\U0001D5C9','\U0001D5FD','\U0001D631','\U0001D665','\U0001D699','\U0001D6D2','\U0001D70C','\U0001D746','\U0001D780','\U0001D7BA'])
    text = replaceUnicodeSymbols('q', text, ['\U0001D42A','\U0001D45E','\U0001D492','\U0001D4C6','\U0001D4FA','\U0001D562','\U0001D596','\U0001D5CA','\U0001D5FE','\U0001D632','\U0001D666','\U0001D69A'])
    text = replaceUnicodeSymbols('r', text, ['\U0001D42B','\U0001D45F','\U0001D493','\U0001D4C7','\U0001D4FB','\U0001D563','\U0001D597','\U0001D5CB','\U0001D5FF','\U0001D633','\U0001D667','\U0001D69B'])
    text = replaceUnicodeSymbols('s', text, ['\U0001D42C','\U0001D460','\U0001D494','\U0001D4C8','\U0001D4FC','\U0001D564','\U0001D598','\U0001D5CC','\U0001D600','\U0001D634','\U0001D668','\U0001D69C'])
    text = replaceUnicodeSymbols('t', text, ['\U0001D42D','\U0001D461','\U0001D495','\U0001D4C9','\U0001D4FD','\U0001D565','\U0001D599','\U0001D5CD','\U0001D601','\U0001D635','\U0001D669','\U0001D69D'])
    text = replaceUnicodeSymbols('u', text, ['\U0001D42E','\U0001D462','\U0001D496','\U0001D4CA','\U0001D4FE','\U0001D566','\U0001D59A','\U0001D5CE','\U0001D602','\U0001D636','\U0001D66A','\U0001D69E','\U0001D6CD','\U0001D707','\U0001D741','\U0001D77B','\U0001D7B5','\U0001D6D6','\U0001D710','\U0001D74A','\U0001D784','\U0001D7BE','\U000000F9','\U000000FA','\U000000FB','\U000000FC'])
    text = replaceUnicodeSymbols('v', text, ['\U0001D42F','\U0001D463','\U0001D497','\U0001D4CB','\U0001D4FF','\U0001D567','\U0001D59B','\U0001D5CF','\U0001D603','\U0001D637','\U0001D66B','\U0001D69F','\U0001D6CE','\U0001D708','\U0001D742','\U0001D77C','\U0001D7B6'])
    text = replaceUnicodeSymbols('w', text, ['\U0001D430','\U0001D464','\U0001D498','\U0001D4CC','\U0001D500','\U0001D568','\U0001D59C','\U0001D5D0','\U0001D604','\U0001D638','\U0001D66C','\U0001D6A0','\U0001D6DA','\U0001D714','\U0001D74E','\U0001D788','\U0001D7C2','\U0001D6E1','\U0001D71B','\U0001D755','\U0001D78F','\U0001D7C9'])
    text = replaceUnicodeSymbols('x', text, ['\U0001D431','\U0001D465','\U0001D499','\U0001D4CD','\U0001D501','\U0001D569','\U0001D59D','\U0001D5D1','\U0001D605','\U0001D639','\U0001D66D','\U0001D6A1','\U0001D6DE','\U0001D718','\U0001D752','\U0001D78C','\U0001D7C6'])
    text = replaceUnicodeSymbols('y', text, ['\U0001D432','\U0001D466','\U0001D49A','\U0001D4CE','\U0001D502','\U0001D56A','\U0001D5D2','\U0001D606','\U0001D63A','\U0001D66E','\U0001D6A2','\U0000213D','\U000000FD','\U000000FF'])
    text = replaceUnicodeSymbols('z', text, ['\U0001D433','\U0001D467','\U0001D49B','\U0001D4CF','\U0001D503','\U0001D56B','\U0001D5D3','\U0001D607','\U0001D63B','\U0001D66F','\U0001D6A3'])
    text = replaceUnicodeSymbols('A', text, ['\U0001D400','\U0001D434','\U0001F150','\U0001F170','\U0001F130','\U0001D468','\U0001D49C','\U0001D4D0','\U0001D504','\U0001D538','\U0001D56C','\U0001D5A0','\U0001D5D4','\U0001D608','\U0001D63C','\U0001D670','\U0001D6A8','\U0001D6E2','\U0001D71C','\U0001D756','\U0001D790','\U0000212B','\U000000C0','\U000000C1','\U000000C2','\U000000C3','\U000000C4','\U000000C5'])
    text = replaceUnicodeSymbols('B', text, ['\U0001D401','\U0001D435','\U0001F151','\U0001F171','\U0001F131','\U0001D469','\U0001D4D1','\U0001D505','\U0001D539','\U0001D56D','\U0001D5A1','\U0001D5D5','\U0001D609','\U0001D63D','\U0001D671','\U0001D6A9','\U0001D6E3','\U0001D71D','\U0001D757','\U0001D791','\U0001D6C3','\U0001D6FD','\U0001D737','\U0001D771','\U0001D7AB','\U0000212C','\U000000DF'])
    text = replaceUnicodeSymbols('C', text, ['\U0001D402','\U0001D436','\U0001F152','\U0001F172','\U0001F132','\U0001D46A','\U0001D49E','\U0001D4D2','\U0001D56E','\U0001D5A2','\U0001D5D6','\U0001D60A','\U0001D63E','\U0001D672','\U00002102','\U00002103','\U0000212D','\U000000C7'])
    text = replaceUnicodeSymbols('D', text, ['\U0001F153','\U0001F173','\U0001F133','\U0001D403','\U0001D437','\U0001D46B','\U0001D49F','\U0001D4D3','\U0001D507','\U0001D53B','\U0001D56F','\U0001D5A3','\U0001D5D7','\U0001D60B','\U0001D63F','\U0001D673','\U00002145','\U000000D0'])
    text = replaceUnicodeSymbols('E', text, ['\U0001F154','\U0001F174','\U0001F134','\U0001D404','\U0001D438','\U0001D46C','\U0001D4D4','\U0001D508','\U0001D53C','\U0001D570','\U0001D5A4','\U0001D5D8','\U0001D60C','\U0001D640','\U0001D674','\U0001D6AC','\U0001D6E6','\U0001D720','\U0001D75A','\U0001D794','\U0001D6DC','\U0001D716','\U0001D750','\U0001D78A','\U0001D7C4','\U0001D6C6','\U0001D700','\U0001D73A','\U0001D774','\U0001D7AE','\U00002107','\U00002108','\U00002128','\U00002130','\U000000C8','\U000000C9','\U000000CA','\U000000CB'])
    text = replaceUnicodeSymbols('F', text, ['\U0001F155','\U0001F175','\U0001F135','\U0001D405','\U0001D439','\U0001D46D','\U0001D4D5','\U0001D509','\U0001D53D','\U0001D571','\U0001D5A5','\U0001D5D9','\U0001D60D','\U0001D641','\U0001D675','\U0001D7CA','\U00002131','\U00002132','\U00002109'])
    text = replaceUnicodeSymbols('G', text, ['\U0001F156','\U0001F176','\U0001F136','\U0001D406','\U0001D43A','\U0001D46E','\U0001D4A2','\U0001D4D6','\U0001D50A','\U0001D53E','\U0001D572','\U0001D5A6','\U0001D5DA','\U0001D60E','\U0001D642','\U0001D676'])
    text = replaceUnicodeSymbols('H', text, ['\U0001F157','\U0001F177','\U0001F137','\U0001D407','\U0001D43B','\U0001D46F','\U0001D4D7','\U0001D573','\U0001D5A7','\U0001D5DB','\U0001D60F','\U0001D643','\U0001D677','\U0001D6AE','\U0001D6E8','\U0001D722','\U0001D75C','\U0001D796','\U0000210B','\U0000210C','\U0000210D'])
    text = replaceUnicodeSymbols('I', text, ['\U0001F158','\U0001F178','\U0001F138','\U0001D408','\U0001D43C','\U0001D470','\U0001D4D8','\U0001D540','\U0001D574','\U0001D5A8','\U0001D5DC','\U0001D610','\U0001D644','\U0001D678','\U0001D6B0','\U0001D6EA','\U0001D724','\U0001D75E','\U0001D798','\U00002110','\U00002111','\U000000CC','\U000000CD','\U000000CE','\U000000CF'])
    text = replaceUnicodeSymbols('J', text, ['\U0001F159','\U0001F179','\U0001F139','\U0001D409','\U0001D43D','\U0001D471','\U0001D4A5','\U0001D4D9','\U0001D50D','\U0001D541','\U0001D575','\U0001D5A9','\U0001D5DD','\U0001D611','\U0001D645','\U0001D679'])
    text = replaceUnicodeSymbols('K', text, ['\U0001F15A','\U0001F17A','\U0001F13A','\U0001D40A','\U0001D43E','\U0001D472','\U0001D4A6','\U0001D4DA','\U0001D50E','\U0001D542','\U0001D576','\U0001D5AA','\U0001D5DE','\U0001D612','\U0001D646','\U0001D67A','\U0001D6B1','\U0001D6EB','\U0001D725','\U0001D75F','\U0001D799','\U0000212A'])
    text = replaceUnicodeSymbols('L', text, ['\U0001F15B','\U0001F17B','\U0001F13B','\U0001D40B','\U0001D43F','\U0001D473','\U0001D4DB','\U0001D50F','\U0001D543','\U0001D577','\U0001D5AB','\U0001D5DF','\U0001D613','\U0001D647','\U0001D67B','\U00002112'])
    text = replaceUnicodeSymbols('M', text, ['\U0001F15C','\U0001F17C','\U0001F13C','\U0001D40C','\U0001D440','\U0001D474','\U0001D4DC','\U0001D510','\U0001D544','\U0001D578','\U0001D5AC','\U0001D5E0','\U0001D614','\U0001D648','\U0001D67C','\U0001D6B3','\U0001D6ED','\U0001D727','\U0001D761','\U0001D79B','\U00002133'])
    text = replaceUnicodeSymbols('N', text, ['\U0001F15D','\U0001F17D','\U0001F13D','\U0001D40D','\U0001D441','\U0001D475','\U0001D4A9','\U0001D4DD','\U0001D511','\U0001D579','\U0001D5AD','\U0001D5E1','\U0001D615','\U0001D649','\U0001D67D','\U0001D6B4','\U0001D6B7','\U0001D6EE','\U0001D728','\U0001D762','\U0001D79C','\U00002115','\U00002135','\U000000D1'])
    text = replaceUnicodeSymbols('O', text, ['\U0001F15E','\U0001F17E','\U0001F13E','\U0001D40E','\U0001D442','\U0001D476','\U0001D4AA','\U0001D4DE','\U0001D512','\U0001D546','\U0001D57A','\U0001D5AE','\U0001D5E2','\U0001D616','\U0001D64A','\U0001D67E','\U0001D6AF','\U0001D6B6','\U0001D6B9','\U0001D6E9','\U0001D723','\U0001D75D','\U0001D797','\U0001D6F0','\U0001D72A','\U0001D764','\U0001D79E','\U0001D6F3','\U0001D72D','\U0001D767','\U0001D7A1','\U0001D6C9','\U0001D703','\U0001D73D','\U0001D777','\U0001D7B1','\U0000213A','\U000000D2','\U000000D3','\U000000D4','\U000000D5','\U000000D6','\U000000D8'])
    text = replaceUnicodeSymbols('P', text, ['\U0001F15F','\U0001F17F','\U0001F13F','\U0001D40F','\U0001D443','\U0001D477','\U0001D4AB','\U0001D4DF','\U0001D513','\U0001D57B','\U0001D5AF','\U0001D5E3','\U0001D617','\U0001D64B','\U0001D67F','\U0001D6B8','\U0001D6F2','\U0001D72C','\U0001D766','\U0001D7A0','\U00002117','\U00002118','\U00002119'])
    text = replaceUnicodeSymbols('Q', text, ['\U0001F160','\U0001F180','\U0001F140','\U0001D410','\U0001D444','\U0001D478','\U0001D4AC','\U0001D4E0','\U0001D514','\U0001D57C','\U0001D5B0','\U0001D5E4','\U0001D618','\U0001D64C','\U0001D680','\U0000211A'])
    text = replaceUnicodeSymbols('R', text, ['\U0001F161','\U0001F181','\U0001F141','\U0001D411','\U0001D445','\U0001D479','\U0001D4E1','\U0001D57D','\U0001D5B1','\U0001D5E5','\U0001D619','\U0001D64D','\U0001D681','\U0000211B','\U0000211C','\U0000211D','\U0000211E','\U0000211F'])
    text = replaceUnicodeSymbols('S', text, ['\U0001F162','\U0001F182','\U0001F142','\U0001D412','\U0001D446','\U0001D47A','\U0001D4AE','\U0001D4E2','\U0001D516','\U0001D54A','\U0001D57E','\U0001D5B2','\U0001D5E6','\U0001D61A','\U0001D64E','\U0001D682'])
    text = replaceUnicodeSymbols('T', text, ['\U0001F163','\U0001F183','\U0001F143','\U0001D413','\U0001D447','\U0001D47B','\U0001D4AF','\U0001D4E3','\U0001D517','\U0001D54B','\U0001D57F','\U0001D5B3','\U0001D5E7','\U0001D61B','\U0001D64F','\U0001D683','\U0001D6BB','\U0001D6F5','\U0001D72F','\U0001D769','\U0001D7A3','\U0001D6D5','\U0001D70F','\U0001D749','\U0001D783','\U0001D7BD'])
    text = replaceUnicodeSymbols('U', text, ['\U0001F164','\U0001F184','\U0001F144','\U0001D414','\U0001D448','\U0001D47C','\U0001D4B0','\U0001D4E4','\U0001D518','\U0001D54C','\U0001D580','\U0001D5B4','\U0001D5E8','\U0001D61C','\U0001D650','\U0001D684','\U000000D9','\U000000DA','\U000000DB','\U000000DC'])
    text = replaceUnicodeSymbols('V', text, ['\U0001F165','\U0001F185','\U0001F145','\U0001D415','\U0001D449','\U0001D47D','\U0001D4B1','\U0001D4E5','\U0001D519','\U0001D54D','\U0001D581','\U0001D5B5','\U0001D5E9','\U0001D61D','\U0001D651','\U0001D685','\U00002123'])
    text = replaceUnicodeSymbols('W', text, ['\U0001F166','\U0001F186','\U0001F146','\U0001D416','\U0001D44A','\U0001D47E','\U0001D4B2','\U0001D4E6','\U0001D51A','\U0001D54E','\U0001D582','\U0001D5B6','\U0001D5EA','\U0001D61E','\U0001D652','\U0001D686'])
    text = replaceUnicodeSymbols('X', text, ['\U0001F167','\U0001F187','\U0001F147','\U0001D417','\U0001D44B','\U0001D47F','\U0001D4B3','\U0001D4E7','\U0001D51B','\U0001D54F','\U0001D583','\U0001D5B7','\U0001D5EB','\U0001D61F','\U0001D653','\U0001D687','\U0001D6BE','\U0001D6F8','\U0001D732','\U0001D76C','\U0001D7A6','\U0001D6D8','\U0001D712','\U0001D74C','\U0001D786','\U0001D7C0','\U000000D7'])
    text = replaceUnicodeSymbols('Y', text, ['\U0001F168','\U0001F188','\U0001F148','\U0001D418','\U0001D44C','\U0001D480','\U0001D4B4','\U0001D4E8','\U0001D51C','\U0001D550','\U0001D584','\U0001D5B8','\U0001D5EC','\U0001D620','\U0001D654','\U0001D688','\U0001D6BC','\U0001D6F6','\U0001D730','\U0001D76A','\U0001D7A4','\U0001D6C4','\U0001D6FE','\U0001D738','\U0001D772','\U0001D7AC','\U000000DD'])
    text = replaceUnicodeSymbols('Z', text, ['\U0001F169','\U0001F189','\U0001F149','\U0001D419','\U0001D44D','\U0001D481','\U0001D4B5','\U0001D4E9','\U0001D585','\U0001D5B9','\U0001D5ED','\U0001D621','\U0001D655','\U0001D689','\U0001D6AD','\U0001D6E7','\U0001D721','\U0001D75B','\U0001D795','\U00002124'])
    text = replaceUnicodeSymbols('0', text, ['\U0001D7CE','\U0001D7D8','\U0001D7E2','\U0001D7EC','\U0001D7F6'])
    text = replaceUnicodeSymbols('1', text, ['\U0001D7CF','\U0001D7D9','\U0001D7E3','\U0001D7ED','\U0001D7F7'])
    text = replaceUnicodeSymbols('2', text, ['\U0001D7D0','\U0001D7DA','\U0001D7E4','\U0001D7EE','\U0001D7F8'])
    text = replaceUnicodeSymbols('3', text, ['\U0001D7D1','\U0001D7DB','\U0001D7E5','\U0001D7EF','\U0001D7F9'])
    text = replaceUnicodeSymbols('4', text, ['\U0001D7D2','\U0001D7DC','\U0001D7E6','\U0001D7F0','\U0001D7FA'])
    text = replaceUnicodeSymbols('5', text, ['\U0001D7D3','\U0001D7DD','\U0001D7E7','\U0001D7F1','\U0001D7FB'])
    text = replaceUnicodeSymbols('6', text, ['\U0001D7D4','\U0001D7DE','\U0001D7E8','\U0001D7F2','\U0001D7FC'])
    text = replaceUnicodeSymbols('7', text, ['\U0001D7D5','\U0001D7DF','\U0001D7E9','\U0001D7F3','\U0001D7FD'])
    text = replaceUnicodeSymbols('8', text, ['\U0001D7D6','\U0001D7E0','\U0001D7EA','\U0001D7F4','\U0001D7FE'])
    text = replaceUnicodeSymbols('9', text, ['\U0001D7D7','\U0001D7E1','\U0001D7EB','\U0001D7F5','\U0001D7FF'])
    text = replaceUnicodeSymbols('NO', text, ['\U00002116'])
    text = replaceUnicodeSymbols('SM', text, ['\U00002120'])
    text = replaceUnicodeSymbols('TEL', text, ['\U00002121'])
    text = replaceUnicodeSymbols('TM', text, ['\U00002122'])
    text = replaceUnicodeSymbols('FAX', text, ['\U0000213B'])
    # Fraktur y looks like an n
    text = replaceUnicodeSymbols('n', text, ['\U0001D536','\U0001D59E'])
    # Fraktur z looks like an E (kind of)
    text = replaceUnicodeSymbols('E', text, ['\U0001D537','\U0001D59F'])
    return text

def cleanUpMiscStuff(text):
    text = text.replace('🫨', '')
    text = text.replace('͛͛͛', '')
    text = text.replace('＂', '\'')
    text = text.replace('?', '？')
    text = text.replace('*', '＊')
    text = text.replace('｜', '-')
    text = re.sub(r'B[_＊\-%$#]tch', 'Bitch', text)
    text = re.sub(r'B[_＊\-%$#]{2}ch', 'Bitch', text)
    text = re.sub(r'B[_＊\-%$#]{3}h', 'Bitch', text)
    text = re.sub(r'B[_＊\-%$#]TCH', 'BITCH', text)
    text = re.sub(r'B[_＊\-%$#]{2}CH', 'BITCH', text)
    text = re.sub(r'B[_＊\-%$#]{3}H', 'BITCH', text)
    text = re.sub(r'B[_＊\-%$#]{4}', 'BITCH', text)
    text = re.sub(r'F[_＊\-%$#]ck', 'Fuck', text)
    text = re.sub(r'F[_＊\-%$#]CK', 'FUCK', text)
    text = re.sub(r'F[_＊\-%$#]{2}k', 'Fuck', text)
    text = re.sub(r'F[_＊\-%$#]{2}K', 'FUCK', text)
    text = re.sub(r'F[_＊\-%$#]{3}', 'FUCK', text)
    text = re.sub(r'FUCK[_＊\-%$#]{3}', 'FUCKING', text)
    text = re.sub(r'Fuck[_＊\-%$#]{3}', 'Fucking', text)
    text = re.sub(r'Sh[_＊\-%$#]t', 'Shit', text)
    text = re.sub(r'SH[_＊\-%$#]T', 'SHIT', text)
    text = re.sub(r'R[_＊\-%$#]pe', 'Rape', text)
    text = re.sub(r'R[_＊\-%$#]PE', 'RAPE', text)
    text = re.sub(r'N[_＊\-%$#]zi', 'Nazi', text)
    text = re.sub(r'N[_＊\-%$#]ZI', 'NAZI', text)
    text = re.sub(r'P[_＊\-%$#]do', 'Pedo', text)
    text = re.sub(r'P[_＊\-%$#]DO', 'PEDO', text)
    text = re.sub(r'F[_＊\-%$#]{1,2}ed', 'Fucked', text)
    text = re.sub(r'F[_＊\-%$#]{1,2}ED', 'FUCKED', text)
    text = re.sub(r'T[_＊\-%$#]rror', 'Terror', text)
    text = re.sub(r'9[_-]11', '9⧸11', text)
    text = re.sub(r'13[_-]50', '13⧸50', text)
    return text

def cleanUpText(text):
    text = cleanUpMiscStuff(text)
    text = removeEmojisFromText(text)
    text = cleanUpAlphanum(text)
    text = cleanUpWhitespace(text)
    return text

def cleanFilenames(videosDir):
    # TODO scan files for partial downloads and remove those file ids from the archive
    listOfFiles = getFiles(videosDir)
    for i in listOfFiles:
        location = os.path.dirname(i)
        filenameOriginal = os.path.basename(i)
        print(filenameOriginal)
        filenameNew = filenameOriginal
        ##  First pass, clean out all emojis, unicode and fix the whitespace
        filenameNew = cleanUpText(filenameNew)
        ##  Fiddly stuff because GE can't spell
        filenameNew = re.sub(r"(?i)\s+_( GE('s)?( & KC('s)?)?)?\s+Da(il)*y(\s+Bible)?\s+[Podcast]{7}\s*", r"", filenameNew)
        ##  Just removing extra letters now
        filenameNew = re.sub(r"(?i) \(Zero Punctuation\)", r"", filenameNew)
        ##  Removing Contrapoints suffix
        filenameNew = re.sub(r"\s[-_]\sContraPoints", r"", filenameNew)
        ##  Youtube-DL turns 'w\' into 'w_'
        filenameNew = re.sub(r"(?i)w_ ", r"with ", filenameNew)
        ##  Remove invalid characters
        filenameNew = re.sub(r"([\<\>:\"\/\\|?*])", r"", filenameNew)
        ##  Clean up any extra spaces, convert underscores, purge ellipses
        filenameNew = re.sub(r"\s+", r" ", filenameNew)
        filenameNew = re.sub(r" _ ", r" - ", filenameNew)
        filenameNew = re.sub(r"—", r"-", filenameNew)
        filenameNew = re.sub(r"\.\.+", r".", filenameNew)
        old = os.path.join(location, filenameOriginal)
        new = os.path.join(location, filenameNew)
        os.rename(old, new)

## file management

def moveFilesToDestination(videosDir, logFilepath, destinationDir):
    ## TODO: Move files one at a time to avoid mixing processed and unprocessed files if the program crashes
    ## OR move completed files into a new folder to wait for processing
    listOfFiles = getFiles(videosDir)
    for i in listOfFiles:
        old = os.path.join(videosDir, os.path.join(os.path.basename(os.path.dirname(i)), os.path.basename(i)))
        new = os.path.join(destinationDir, os.path.join(os.path.basename(os.path.dirname(i)), os.path.basename(i)))

        if not os.path.exists(new):
            print(f"Moving {os.path.basename(i)}")
            try:
                shutil.copy(old, new)
            except FileExistsError as err:
                appendToTextFile(err, logFilepath)
            except FileNotFoundError as err:
                appendToTextFile(err, logFilepath)
        else:
            appendToTextFile(f"WARN: File {os.path.basename(i)} already exists\n", logFilepath)

def deleteFiles(videosDir):
    location = videosDir
    folders = os.listdir(location)
    for i in folders:
        folder = os.path.join(location, i)
        print("Deleting", folder)
        shutil.rmtree(folder, ignore_errors=False, onerror=None)

## log management

def logAllFiles(videosDir, logFilepath):
    listOfFiles = getFiles(videosDir)
    if len(listOfFiles) > 0:
        appendToTextFile(f"=== NEW RUN: {str(len(listOfFiles))} new episodes ===", logFilepath, False)
        for i in listOfFiles:
            show = os.path.basename(os.path.dirname(i))
            episode = os.path.basename(i)
            log = f" - {os.path.join(show, episode)}"
            appendToTextFile(log, logFilepath)

def appendToTextFile(text, filepath, writeDate=True):
    with open(filepath, "a", encoding="utf-8") as file:
        if writeDate:
            time = datetime.now()
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {text}\n")
        else:
            file.write(f"{text}\n")
