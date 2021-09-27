import requests
from requests_html import HTMLSession
import pandas as pd
import csv
import re
from urllib.parse import urlparse
import sys

regexCreatedIndex = sys.argv[2]
firstBackUrlIndex = sys.argv[3]
regexCreatedThread = sys.argv[4]
firstBackUrlThread = sys.argv[5]
regexCreatedPageFlip = sys.argv[6]
firstBackUrlPageFlip = sys.argv[7]

print(f'\n\n{regexCreatedIndex}')
print(f'{firstBackUrlIndex}')


def get_page(urL):
    session = HTMLSession()
    try:
        r = session.get(urL)  # entry page
        if r.status_code == 200:
            # r.html.render(sleep=1, keep_page=True, scrolldown=3, timeout=30)
            print(f"\nStatus code: {r.status_code}\nWebpage is successfully loaded!\n")
            return r.html
        else:
            print(f"Status code: {r.status_code}\nWebpage cannot be loaded!")
            return None
    except requests.exceptions.ConnectionError:
        return None


def get_href(link_table_for_href, forums):
    for forum in forums.xpath('//tr[contains(@class, "windowbg") and contains(@id, "board_")]'):
        group = {}
        for count, link in enumerate(forum.xpath('//a')):
            group[f"Group_{count + 1}"] = link.text.strip()
        link_table_for_href.append(group)


def store_csv(x, filename):
    with open(filename + '.csv', 'a', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([x])

# r_html = get_page("https://www.metacritic.com/movie/escape-room-2/user-reviews")  # https://forums.afterdawn.com/forums/other_mobile_phones/ https://forums.afterdawn.com/forums/pc-hardware-help/ https://forums.afterdawn.com/forums/windows-games/ https://www.gardenstew.com/ https://www.lfcreds.com/reds/ https://www.gardenstew.com/forums/site-rules-and-guidelines.2/

# extracted_table = r_html.xpath('//table[@class = "table_list"]', first=True)
# print(extracted_table)
# link_table_for_href = []
# get_href(link_table_for_href, extracted_table)
# print(link_table_for_href)
# df_text = pd.DataFrame(link_table_for_href)  # Save into a dataframe
# df_text = df_text.iloc[:, 0:2]
# print()
# print(df_text)

# extracted_table = r_html.find('title')
# print(extracted_table[0].text) #[0].text)
# # print(f"Discussions: {extracted_table.text.lower()}")
# # print(f"Messages: {extracted_table.text.lower()}")
# print()

# url = "https://www.lmj.com/forums/id-089/"
# # url = "https://www.lmj.com/"
# url = url[:url.index(".com/") + len(".com/")]
# print(url)
