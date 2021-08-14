import requests
from requests_html import HTMLSession

'Reference: https://stackoverflow.com/questions/40985060/scrapy-css-selector-get-text-of-all-inner-tags'


def get_thread_index_urls():
    with open('index_url.txt') as f:
        index_urls = f.readlines()
    with open('thread_url.txt') as f:
        thread_urls = f.readlines()
    thread_urls = [text.replace('\n', '') for text in thread_urls]
    index_urls = [text.replace('\n', '') for text in index_urls]

    # bb = [x for x in thread_urls + index_urls if ("redandwhitekop" not in x.lower()) and ("lfcreds" not in x.lower())]

    return list(set(thread_urls)) + list(set(index_urls))


def get_page(urL):
    session = HTMLSession()
    try:
        r = session.get(urL)  # entry page
        if r.status_code == 200:
            print(f"\nStatus code: {r.status_code}\n{urL} is successfully loaded!")
            return r.html
        else:
            print(f"\nStatus code: {r.status_code}\n{urL} cannot be loaded!")
            return None
    except requests.exceptions.ConnectionError:
        return None


def get_PageNum_PageLink(html, r_html):
    possiblePages = r_html.find(html, first=True)

    # Find the anchor text which is digit (e.g. 1, 2, 3, 55)
    possiblePagesNum = [int(link_text.text) for link_text in possiblePages.find('a') if link_text.text.isdigit()]
    possiblePageLink = [link.xpath('//@href', first=True) for link in possiblePages.find('a') if link.text.isdigit()]

    return possiblePagesNum, possiblePageLink


def get_PageNum_PageLink2(html, r_html, url):
    possiblePages = r_html.find(html, first=True)

    # Find the anchor text which is digit (e.g. 1, 2, 3, 55)
    possiblePagesNum = [int(link_text.text) for link_text in possiblePages.find('a') if link_text.text.isdigit()]
    url = url[:url.index(".com/") + len(".com/")]
    possiblePageLink = [url + link.xpath('//@href', first=True) for link in possiblePages.find('a') if link.text.isdigit()]

    return possiblePagesNum, possiblePageLink


def crawlAllPageFlipLinks(index, lastPossiblePageLink, url):
    lst = []
    if "lfcreds.com" in url:
        possible_number = lastPossiblePageLink[-1][index + 1:]
        number = int(possible_number[:possible_number.index(".html")])
        while number >= 0:
            lst.append(f'{lastPossiblePageLink[-1][:index + 1] + str(number)}')
            number -= 25
    else:
        number = int(lastPossiblePageLink[-1][index + 1:])
        while number >= 0:
            lst.append(f'{lastPossiblePageLink[-1][:index + 1] + str(number)}')
            number -= 40
    return lst


def crawlAllPageFlipLinks2(index, lastPossiblePageLink):
    # url = url[:url.index(".com/") + len(".com/")]
    lst = []
    try:
        number = int(lastPossiblePageLink[-1][index + 1:])
        while number > 0:
            lst.append(f'{lastPossiblePageLink[-1][:index + 1] + str(number)}')
            number -= 1
    except:
        pass
    return lst


# Returns 2nd last index of x if it is present. Else, returns -1.
def find2ndLastIndex(text, x):
    count = 0
    # Traverse from right
    for i in range(len(text) - 1, -1, -1):
        if text[i] == x:
            count += 1
            if count == 2:
                return i
    return -1


# Returns last index of x if it is present. Else, returns -1.
def findLastIndex(text, x):
    # Traverse from right
    for i in range(len(text) - 1, -1, -1):
        if text[i] == x:
            return i
    return -1


def findPageFlippingUrls(all_thread_index_urls):
    page_flipping_urls = []
    page_flipping_urls2 = []

    for url in all_thread_index_urls:

        r_html = get_page(url)  # https://www.redandwhitekop.com/forum/index.php?board=17.0

        if r_html is not None:
            if r_html.find('div.pagelinks.floatleft', first=True) is not None:

                # Get the 1st page's possible page-flipping urls
                possiblePagesNum, possiblePageLink = get_PageNum_PageLink('div.pagelinks.floatleft', r_html)

                if len(possiblePageLink) != 0:
                    # From the possiblePageLink, get the 2nd page page-flipping urls
                    r_html = get_page(possiblePageLink[0])

                    # Get the 2nd page's possible page-flipping urls
                    lastPossiblePagesNum, lastPossiblePageLink = get_PageNum_PageLink('div.pagelinks.floatleft', r_html)

                    # Compare the last page number of  1st page's possible page-flipping urls and 2nd page's possible page-flipping urls
                    print(f'The LAST PAGE NUMBER and LINK of 1st page-flipping url: {possiblePagesNum[-1]}, {possiblePageLink[-1]}')
                    print(f'The LAST PAGE NUMBER and LINK of 2nd page-flipping url: {lastPossiblePagesNum[-1]}, {lastPossiblePageLink[-1]}')
                    print(f'Are they same? : {possiblePagesNum[-1] == lastPossiblePagesNum[-1]}, {possiblePageLink[-1] == lastPossiblePageLink[-1]} (If same means that they are valid page-flipping urls)')

                    if (possiblePagesNum[-1] == lastPossiblePagesNum[-1]) and (possiblePageLink[-1] == lastPossiblePageLink[-1]):
                        if "lfcreds.com" in url:
                            index = find2ndLastIndex(lastPossiblePageLink[-1], '.')
                        else:
                            index = findLastIndex(lastPossiblePageLink[-1], '.')
                        # print(index)
                        # print(f'{lastPossiblePageLink[-1][:index + 1]}')
                        # print(f'{lastPossiblePageLink[-1][index + 1:]}')
                        page_flipping_urls += crawlAllPageFlipLinks(index, lastPossiblePageLink, url)
                else:
                    print("No page flipping url was found!\n")
            elif r_html.find('div.PageNav', first=True) is not None:

                # Get the 1st page's possible page-flipping urls
                possiblePagesNum, possiblePageLink = get_PageNum_PageLink2('div.PageNav', r_html, url)

                # From the possiblePageLink, get the 2nd page page-flipping urls
                print(possiblePageLink[0])
                r_html = get_page(possiblePageLink[0])

                if len(possiblePageLink) != 0:
                    # Get the 2nd page's possible page-flipping urls
                    lastPossiblePagesNum, lastPossiblePageLink = get_PageNum_PageLink2('div.PageNav', r_html, url)

                    # Compare the last page number of  1st page's possible page-flipping urls and 2nd page's possible page-flipping urls
                    print(f'The LAST PAGE NUMBER and LINK of 1st page-flipping url: {possiblePagesNum[-1]}, {possiblePageLink[-1]}')
                    print(f'The LAST PAGE NUMBER and LINK of 2nd page-flipping url: {lastPossiblePagesNum[-1]}, {lastPossiblePageLink[-1]}')
                    print(f'Are they same? : {possiblePagesNum[-1] == lastPossiblePagesNum[-1]}, {possiblePageLink[-1] == lastPossiblePageLink[-1]} (If same means that they are valid page-flipping urls)')

                    if (possiblePagesNum[-1] == lastPossiblePagesNum[-1]) and (possiblePageLink[-1] == lastPossiblePageLink[-1]):
                        index = findLastIndex(lastPossiblePageLink[-1], '-')
                        page_flipping_urls2 += crawlAllPageFlipLinks2(index, lastPossiblePageLink)
                else:
                    print("No page flipping url was found!\n")
            else:
                print("No page flipping url was found!\n")

    return page_flipping_urls + page_flipping_urls2


def main_PageFlipping():
    all_thread_index_urls = get_thread_index_urls()
    # all_thread_index_urls = ['https://www.redandwhitekop.com/forum/index.php?board=17.0'] #https://www.gardenstew.com/threads/new-to-gardening%E2%80%8D.42723/

    results = findPageFlippingUrls(all_thread_index_urls)
    with open('page_flipping_url.txt', 'a') as f:
        for line in results:
            f.write(line)
            f.write('\n')


if __name__ == '__main__':
    main_PageFlipping()
