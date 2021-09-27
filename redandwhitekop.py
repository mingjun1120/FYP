from requests_html import HTMLSession
import pandas as pd

''' 
    Text File Resources: 
    https://www.pythontutorial.net/python-basics/python-write-text-file/, 
    https://www.pythontutorial.net/python-basics/python-read-text-file/
'''


def get_page(urL):
    session = HTMLSession()
    r = session.get(urL)  # entry page
    if r.status_code == 200:
        # r.html.render(sleep=1, keep_page=True, scrolldown=3, timeout=60, wait=5)
        print(f"\nStatus code: {r.status_code}\n{urL} is successfully loaded!\n")
        return r.html
    else:
        print(f"\nStatus code: {r.status_code}\n{urL} cannot be loaded!")
        return None


def countCharLength(column_data):
    counter = 0
    for text in column_data:
        counter += len(text)
    return counter


def get_href(link_table_for_href, forums, html2):
    for forum in forums.xpath(html2):
        group = {}
        for count, link in enumerate(forum.xpath('//a/@href')):
            group[f"Group_{count + 1}"] = link
        link_table_for_href.append(group)


def getLinkTxt(link_table_for_text, forums, html2):
    for forum in forums.xpath(html2):
        group = {}
        for count, link in enumerate(forum.xpath('//a')):
            group[f"Group_{count + 1}"] = link.text.strip()
        link_table_for_text.append(group)


def get_href_text_df(r_html, html, html2):
    df_href_1st3_col = None
    df_text_1st3_col = None

    # Find the table like-structure
    forums = r_html.xpath(html, first=True)

    if forums is not None:
        # Loop through each forum at entry page
        link_table_for_href = []
        get_href(link_table_for_href, forums, html2)
        df_href = pd.DataFrame(link_table_for_href)  # Save into a dataframe

        # Select the first 2 columns only because all forums' title or topics located at first, 2nd or 3rd column only
        df_href_1st3_col = df_href.iloc[:, 0:2]

        # Loop through each forum at entry page
        link_table_for_text = []
        getLinkTxt(link_table_for_text, forums, html2)
        df_text = pd.DataFrame(link_table_for_text)  # Save into a dataframe

        # Select the first 2 columns only because all forums' title or topics located at first, 2nd or 3rd column only
        df_text_1st3_col = df_text.iloc[:, 0:2]

    return df_href_1st3_col, df_text_1st3_col


def get_it_group(df_href_1st3_col, df_text_1st3_col):
    # Calculate the total text length of each column
    totalTxtLen1 = None
    totalTxtLen2 = None

    for (columnName, columnData) in df_text_1st3_col.iteritems():
        num = countCharLength(columnData.values)
        if columnName == 'Group_1':
            totalTxtLen1 = num
        else:
            totalTxtLen2 = num

    # Compare the totalTxtLen1 and totalTxtLen2, the higher value is the candidate of index/threads url
    max_val = totalTxtLen1

    it_group = df_href_1st3_col['Group_1'].tolist()
    for counter, txtLen in enumerate([totalTxtLen2]):
        if txtLen > max_val:
            max_val = txtLen
            it_group = df_href_1st3_col[f'Group_{counter + 2}'].tolist()

    return it_group


def get_href_and_text_df(url, html, html2):
    # Load the page
    r_html = get_page(url)

    if r_html is not None:
        # Retrieve each anchor text and its corresponding link into dataframes
        df_href_1st3_col, df_text_1st3_col = get_href_text_df(r_html, html, html2)
        return df_href_1st3_col, df_text_1st3_col
    else:
        return None, None


def classify_Index_Thread_Url(it_group):
    index_BoardList_url = []
    index_board_thread_url = []
    for link in it_group:

        r_html = get_page(link)
        print(f'CHECKING URL: {link}')
        if r_html is not None:
            try:
                extracted_table = r_html.find('table', first=True)
                try:
                    if extracted_table.text.lower().count("posts") >= 1 and extracted_table.text.lower().count("topics") >= 1:
                        index_BoardList_url.append(link)
                        print('INDEX_BOARD_LIST URL')
                    elif (extracted_table.text.lower().count("replies") >= 1 and extracted_table.text.lower().count("views") >= 1) and (extracted_table.find('thead', first=True).text.lower().count("replies") and extracted_table.find('thead', first=True).text.lower().count("views")):
                        index_board_thread_url.append(link)
                        print('INDEX_BOARD_THREAD URL')
                    else:
                        print('UNRELATED URL')
                except:
                    print('UNRELATED URL')
            except:
                print('UNRELATED URL')
        else:
            print("WEBPAGE DOESN'T EXIST")

    return index_BoardList_url, index_board_thread_url


def main_redandwhitekop():
    urls = ["https://www.redandwhitekop.com/forum/", "https://www.lfcreds.com/reds/"]

    index_BoardList_urls = []
    index_board_thread_urls = []

    for url in urls:

        total_index_BoardList_urls = []
        total_index_board_thread_urls = []
        counter = 0

        while True:
            # Retrieve the link of the anchor text as well as the text of the anchor text into 2 different df respectively1
            df_href_1st3_col, df_text_1st3_col = get_href_and_text_df(url, '//table[@class = "table_list"]',
                                                                      '//tr[contains(@class, "windowbg") and contains(@id, "board_")]')

            if df_href_1st3_col is not None and df_text_1st3_col is not None:
                # Get the index and thread urls in a list
                it_group = get_it_group(df_href_1st3_col, df_text_1st3_col)
                print(f"Index/Thread URLs:\n{it_group}")

                # Classify index and thread urls
                index_BoardList_url, index_board_thread_url = classify_Index_Thread_Url(it_group)

                if len(index_BoardList_url) != 0:
                    for x in index_BoardList_url:
                        total_index_BoardList_urls.append(x)

                if len(index_board_thread_url) != 0:
                    for x in index_board_thread_url:
                        total_index_board_thread_urls.append(x)
            try:
                url = total_index_BoardList_urls[counter]
            except:
                print("ONE FORUM HAS FINISHED CRAWLED!!!")

                index_BoardList_urls += total_index_BoardList_urls
                index_board_thread_urls += total_index_board_thread_urls

                with open('index_url.txt', 'a') as f:
                    for line in index_BoardList_urls + index_board_thread_urls:
                        f.write(line)
                        f.write('\n')
                break
            counter += 1

    # Scrape Thread urls
    for x in [index_board_thread_urls, index_BoardList_urls]:
        for thread_url in x:
            df_href_1st3_col, df_text_1st3_col = get_href_and_text_df(thread_url, '//table[@class = "table_grid"]', '//tbody/tr[not(contains(@class, "windowbg2")) and not(contains(@class, "titlebg6"))]')  # tbody > tr:not(.windowbg2):not(.titlebg6)

            if df_href_1st3_col is not None and df_text_1st3_col is not None:
                # Get the index and thread urls in a list
                it_group = get_it_group(df_href_1st3_col, df_text_1st3_col)
                print(f"Thread URLs:\n{it_group}")

                with open('thread_url.txt', 'a') as f:
                    for line in it_group:
                        f.write(line)
                        f.write('\n')

    # # Pattern of text that contains only alphanumeric characters
    # pattern = re.compile('^[a-zA-Z0-9 ]+$')
    #
    # for count, link in enumerate(r_html.find('a')):
    #     if re.search(pattern, link.text.strip()):
    #         print(f"{count + 1}: {link.text.strip()}")
