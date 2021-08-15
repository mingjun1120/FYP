from Index_Thread import main_Index_Thread
from Page_Flipping import main_PageFlipping
from ITF_Learning import main_ITF_Learning
import subprocess

if __name__ == '__main__':
    print(f"\nFORUM: SixCrazyMinutes")
    main_Index_Thread()

    print(f'CRAWL PAGE FLIPPING URLS')
    main_PageFlipping()

    print(f'ITF LEARNING')
    regexCreatedIndex, firstBackUrlIndex, regexCreatedThread, firstBackUrlThread, regexCreatedPageFlip, firstBackUrlPageFlip = main_ITF_Learning()
    print(f'INDEX: {regexCreatedIndex}, {firstBackUrlIndex}')
    print(f'THREAD: {regexCreatedThread}, {firstBackUrlThread}')
    print(f'PAGE-FLIP: {regexCreatedPageFlip}, {firstBackUrlPageFlip}')

    with open('URL_Regex.txt', 'a') as f:
        for line in [regexCreatedIndex, firstBackUrlIndex, regexCreatedThread, firstBackUrlThread, regexCreatedPageFlip, firstBackUrlPageFlip]:
            f.write(line)
            f.write('\n')
