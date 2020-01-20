import os
import platform
import content_extractor
import dictionary
import error_logger

def listOptions():
    while True:
        try:
            print('** Google Scraper ** ')
            print('** ============== ** ')
            print('=> Options: ')
            print(' 1. Start Scraping of Existing Search Keyword')
            print(' 2. Enter new Keywoard and Depriate Old one')
            print(' 3. Enter new Filter Key Word')
            print(' 4. Show Details of Existing Keyword')
            print(' 5. Delete Filter Key Word')
            print(' 6. Clear Screen')
            print(' 7. Exit System')
            usrInput = int(input('\n\n  => Enter Option Number : '))
            print('\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n')
            if usrInput == 1:
                content_extractor.startScraping()
            elif usrInput == 2:
                dictionary.enterNewKeyword()
            elif usrInput == 3:
                dictionary.enterNewFilter()
            elif usrInput == 4:
                dictionary.displayDictionaryDetail()
            elif usrInput == 5:
                dictionary.deleteFilter()
            elif usrInput == 6:
                clearScreen()
            elif usrInput == 7:
                break
            else:
                print(' >> Wrong Input <<')

            print('\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n')
        except Exception as e:
            error_logger.logError(format(e))

def clearScreen():
    if platform.system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == '__main__':
    listOptions()