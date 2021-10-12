import re
import pandas as pd

'''
Resource:
https://stackoverflow.com/questions/57494666/split-string-on-punctuation-or-number-in-python
https://www.journaldev.com/37091/get-unique-values-from-a-list-in-python
https://stackoverflow.com/questions/28860440/check-when-string-contains-only-special-characters-in-python
https://stackoverflow.com/questions/42376201/list-comprehension-for-multiple-return-function
https://wiki.simplemachines.org/smf/Large_forums
https://xenforo.com/community/threads/the-large-xenforo-forums-list.87974/
https://www.geeksforgeeks.org/python-check-if-all-elements-in-a-list-are-same/
https://towardsdatascience.com/finding-and-removing-duplicate-rows-in-pandas-dataframe-c6117668631f
'''


def get_thread_index_urls():
    with open('index_url.txt') as f:
        index_urls = f.readlines()
    with open('thread_url.txt') as f:
        thread_urls = f.readlines()
    with open('page_flipping_url.txt') as f:
        page_flipping_urls = f.readlines()

    index_urls = [text.replace('\n', '') for text in index_urls]
    thread_urls = [text.replace('\n', '') for text in thread_urls]
    page_flipping_urls = [text.replace('\n', '') for text in page_flipping_urls]

    return list(set(thread_urls)), list(set(index_urls)), list(set(page_flipping_urls))


def separate_urls(url):

    if '.com/' in url:
        main_url = url[:url.index(".com/") + len(".com/")]
        back_url = url[url.index(".com/") + len(".com/"):]
    else:
        main_url = url[:url.index(".uk/") + len(".uk/")]
        back_url = url[url.index(".uk/") + len(".uk/"):]

    first_back_split_url = back_url.split('/')[0]
    second_back_split_url = back_url.split('/')[1]
    try:
        third_back_split_url = back_url.split('/')[2]
    except IndexError:
        third_back_split_url = ''

    return url, main_url, back_url, first_back_split_url, second_back_split_url, third_back_split_url


def check_existence_qty(combined, url):
    counter = 0
    for link in url:
        if combined in link:
            counter += 1
    return counter


def ispunctuation(s):
    if re.match(r'^[_\W]+$', s):
        return True
    else:
        return False


def addValue(dictionary, key, key2):
    if key not in dictionary:
        dictionary.append(key)
    if key2 not in dictionary:
        dictionary.append(key2)


def chkListSame(lst):
    return len(set(lst)) == 1


def chgListElementsToType(comparedValList):
    for count, x in enumerate(comparedValList):
        if x.isalnum():
            if x.isalpha():
                comparedValList[count] = 'str'
            elif x.isdigit():
                comparedValList[count] = 'int'
            else:
                comparedValList[count] = 'str'


def convertRegex(text):
    if 'int' in text:
        text = '\d+'
    elif text == 'str':
        text = '[a-zA-Z0-9]+'
    elif '.' in text:
        text = '\.'
    return text


def countUniqueValOccurrences(third_back_split_url):
    each_unique_value_count = {}
    for val in set(third_back_split_url):
        counter = 0
        for x in third_back_split_url:
            if x == val:
                counter += 1
        each_unique_value_count[val] = counter
    return each_unique_value_count


def learn_ITF(pageType, urlsType, regexForPageFlip=None):
    print(f'\n{pageType} URL INFORMATION:')
    print(f'------------------------')
    url, main_url, back_url, first_back_split_url, second_back_split_url, third_back_split_url = zip(
        *[separate_urls(value) for value in urlsType])
    print(f'Main URL: {list(set(main_url))}')
    print(f'1st back URLS: {list(set(first_back_split_url))}')
    print(f'2nd back URLS: {list(set(second_back_split_url))}')
    print(f'3rd back URLS: {list(set(third_back_split_url))}')

    # combine the main_url (E.g. https://www.gardenstew.com/) and first_back_split_url (E.g. forums/). Result: https://www.gardenstew.com/forums/
    combined = None
    first_back_Url = None
    if len(list(set(first_back_split_url))) == 1:
        combined = list(set(main_url))[0] + list(set(first_back_split_url))[0] + '/'
        first_back_Url = list(set(first_back_split_url))[0]

    elif len(list(set(first_back_split_url))) > 1:

        # Find the each unique values (Key) and its number of occurrences (Value)
        each_unique_value_count_first_back_split_url = countUniqueValOccurrences(first_back_split_url)

        # Unique value that has the highest number of occurrences
        max_key = max(each_unique_value_count_first_back_split_url,
                      key=each_unique_value_count_first_back_split_url.get)
        max_value = max(each_unique_value_count_first_back_split_url.values())

        # Unique value that has the minimum number of occurrences
        min_key = min(each_unique_value_count_first_back_split_url,
                      key=each_unique_value_count_first_back_split_url.get)
        min_value = min(each_unique_value_count_first_back_split_url.values())

        if max_value >= 10 and min_value >= 10:
            combined = list(set(main_url))[0] + f'({max_key}|{min_key})' + '/'
            first_back_Url = f'({max_key}|{min_key})'
        else:
            combined = list(set(main_url))[0] + max_key + '/'
            first_back_Url = max_key
        # qty = 0
        # for count, val in enumerate(list(set(first_back_split_url))):
        #     check_qty = check_existence_qty(list(set(main_url))[0] + list(set(first_back_split_url))[count] + '/', url)
        #     if check_qty > qty:
        #         qty = check_qty
        #         combined = list(set(main_url))[0] + list(set(first_back_split_url))[count] + '/'
        #         first_back_Url = list(set(first_back_split_url))[count]

    # Used for page-flipping only. Count each unique value occurrences and retrieve the values that has the highest number of occurrences
    each_unique_value_count_third_back_split_url = countUniqueValOccurrences(third_back_split_url)
    max_key = max(each_unique_value_count_third_back_split_url, key=each_unique_value_count_third_back_split_url.get)
    if max_key != '':
        combined = combined + regexForPageFlip.replace('$', '') + '\/'

    # Create a dictionary that stores each second_back_split_url in punctuation-tokenized format
    # E.g. {'Link_1': ['general', '-', 'chat', '-', 'forum', '.', '6'], 'Link_2': ['other', '-', 'sports', '.', '5']}
    group = {}
    counter = 0
    if pageType == 'PAGE-FLIPPING':
        for string in list(set(third_back_split_url)):
            string_list = re.split(r"([\-`,.?:;~!@#$%^&*()+=[\]])", string)
            group[f'Link_{counter + 1}'] = string_list
            counter += 1
    else:
        for string in list(set(second_back_split_url)):
            if re.match(r"^[a-zA-Z0-9]+-[a-zA-Z0-9]+-[a-zA-Z0-9]+$", string[:string.index(".") + len(".") - 1]):
                string_list = re.split(r"([\-`,.?:;~!@#$%^&*()+=[\]])", string)
                group[f'Link_{counter + 1}'] = string_list
                counter += 1

    # Create a dictionary that stores the LENGTH of each second_back_split_url in punctuation-tokenized format above
    # E.g. {'Link_1': 7, 'Link_2': 5}
    group_count = group.copy()
    for count, list_val in enumerate(list(group_count.values())):
        group_count[f'Link_{count + 1}'] = len(list_val)

    # Create a dictionary that groups each list with lists that have the same length with it:
    # Keys -> LENGTH OF LIST
    # Values -> LIST OF KEYS in group_count dictionary that have the length of lists respected to Keys
    # E.g. {7: ['Link_1', 'Link_3', 'Link_4', 'Link_5'], 5: ['Link_2', 'Link_6']}
    new_dict = {}
    for key, val in group_count.items():
        for key2, val2 in group_count.items():
            if key != key2:
                if val == val2:
                    if new_dict.get(val) is not None:
                        addValue(new_dict[val], key, key2)
                    else:
                        new_dict[val] = [key, key2]

    # Retrieve the keys (E.g. ['Link_1', 'Link_3', 'Link_4', 'Link_5']) which have the same length
    # Choose the one has more samples -> ['Link_1', 'Link_3', 'Link_4', 'Link_5'] instead of ['Link_2', 'Link_6']
    comparable_string = []
    for y in new_dict.values():
        if len(y) == 4:
            comparable_string = y
            break
        elif len(y) >= 5:
            if len(y) >= 10:
                comparable_string = y[10]
            else:
                comparable_string = y
            break
        elif len(y) == 3:
            comparable_string = y
            break
        elif len(y) == 2:
            comparable_string = y
            break
        else:
            pass

    # Loop through the group dictionary that created very early and retrieve the values that the key exists in comparable_string
    # Then, convert into dataframe. At here, we just select the first 10 values so that we can save time when executing. In case, there are more than 10000 values will take time
    all_comparable_string = [val for key, val in group.items() if key in comparable_string[:10]]
    comparable_string_DF = pd.DataFrame(all_comparable_string)
    print(f'\n{comparable_string_DF}')

    # Then, convert each value in the dataframe to its data type EXCEPT "punctuations" and "values that repeated similarly in other rows"
    # E.g. liverpool-fc-news.32 => str-str-str.int
    for (columnName, columnData) in comparable_string_DF.iteritems():
        comparedValList = list(columnData.values)
        if chkListSame(comparedValList) is False:
            chgListElementsToType(comparedValList)
            comparable_string_DF[columnName] = comparedValList
    print(f'\n{comparable_string_DF}')

    # Combine the each tokenized values (row-wise) in the dataframe into a string again and append it to a list
    # E.g. str-str-str.int
    row_str_lst = []
    for index, row in comparable_string_DF.iterrows():
        row_str_lst.append(''.join([str(x) for x in row.tolist()]))

    # Find the occurrences of each unique string
    occurrences = {}
    if chkListSame(row_str_lst) is False:
        for x in list(set(row_str_lst)):
            counter = 0
            for y in row_str_lst:
                if x == y:
                    counter += 1
            occurrences[x] = counter

    # Retrieve those strings that have higher occurrences
    maxKey = None
    if occurrences:
        for key, val in occurrences.items():
            maxNum = val
            maxKey = key
            for key2, val2 in occurrences.items():
                if key != key2:
                    if val2 > maxNum:
                        maxKey = key2
    else:
        maxKey = row_str_lst[0]

    maxKey_split = re.split(r"([\-`,.?:;~!@#$%^&*()+=[\]])", maxKey)
    maxKey_split = pd.Series(maxKey_split)

    # Drop the row of data which the row of data (strings) were not the one that appeared the most
    for index, row in comparable_string_DF.iterrows():
        if row.tolist() != maxKey_split.tolist():
            comparable_string_DF.drop(index=index, inplace=True)

    # Reset Index
    comparable_string_DF.reset_index(drop=True, inplace=True)

    # Drop duplicated rows
    comparable_string_DF = comparable_string_DF.T.drop_duplicates(keep='first', ignore_index=True)
    comparable_string_DF = comparable_string_DF.T
    print(f'\n{comparable_string_DF}')

    # Convert to regex
    comparable_string_DF = comparable_string_DF.applymap(convertRegex)
    print(f'\n{comparable_string_DF}')

    # Select a regex from the dataframe (Select any row also can since all rows are same. In my case, I choose 1st row)
    row_1 = comparable_string_DF.iloc[0]
    if pageType != 'PAGE-FLIPPING':
        regexCreated = f"^({row_1[0]}{row_1[1]}{row_1[0]})+{row_1[2]}{row_1[3]}$"
    else:
        regexCreated = f"^{row_1[0]}{row_1[1]}{row_1[2]}$"

    print(f'\nURL REGEX of sixcrazyminutes forum ({pageType} PAGE):')
    print(f'--------------------------------------------')
    if pageType != 'PAGE-FLIPPING':
        print(f'{combined + regexCreated}')
    else:
        print(f'{combined + regexCreated.replace("^", "")}')

    print(f'\nURL REGEX ({pageType} PAGE):')
    print(f'--------------------------------------------')
    if pageType != 'PAGE-FLIPPING':
        print(f'^(http[s]?:\/\/)([A-Za-z0-9-]+\.[A-Za-z0-9]+){1, 2}\/{first_back_Url}\/{regexCreated.replace("^", "")}')
    else:
        print(
            f'^(http[s]?:\/\/)([A-Za-z0-9-]+\.[A-Za-z0-9]+){1, 2}\/{first_back_Url}\/{regexForPageFlip.replace("$", "")}\/{regexCreated.replace("^", "")}')

    return regexCreated, first_back_Url


def main_ITF_Learning():
    # Get all index and thread urls in a list respectively
    thread_urls, index_urls, page_flipping_urls = get_thread_index_urls()

    regexCreatedIndex = None
    regexCreatedThread = None
    firstBackUrlIndex = None
    firstBackUrlThread = None

    # Handles index and thread urls
    for pageType in ['INDEX', 'THREAD']:
        if pageType == 'INDEX':
            regexCreated, first_back_Url = learn_ITF(pageType, index_urls)
            regexCreatedIndex = regexCreated
            firstBackUrlIndex = first_back_Url
        else:
            regexCreated, first_back_Url = learn_ITF(pageType, thread_urls)
            regexCreatedThread = regexCreated
            firstBackUrlThread = first_back_Url

    # Handles page-flipping urls
    regexCreatedPageFlip, firstBackUrlPageFlip = learn_ITF("PAGE-FLIPPING", page_flipping_urls,
                                                           regexCreated.replace("^", ""))

    return regexCreatedIndex, firstBackUrlIndex, regexCreatedThread, firstBackUrlThread, regexCreatedPageFlip, firstBackUrlPageFlip


if __name__ == '__main__':
    main_ITF_Learning()  # regexCreatedIndex, regexCreatedThread, regexCreatedPageFlip
