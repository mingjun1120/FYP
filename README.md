
# Web Forum Crawler
This is a web crawler that can help to crawl all the index, thread and page-flipping urls of a forum that built by Xenforo software package. [XenForo](https://xenforo.com/)
## Authors

- Lim Ming Jun [@mingjun1120](https://www.github.com/mingjun1120)

  
## Python Version

Python 3.7+ will do

  
## Documentation

- [Documentation for Scrapy](https://docs.scrapy.org/en/latest/)
- [Documentation for request-html](https://docs.python-requests.org/projects/requests-html/en/latest/)

  
## How to run

Firstly, open up the **terminal** and **activate** your project's Python virtual environment then type the below command:

**View only:**
```
scrapy runspider ForumCrawler.py
```

**View & Store in csv file:**
```
scrapy runspider ForumCrawler.py -O FinalOutput.csv
```

**View & Store in JSON file:**
```
scrapy runspider ForumCrawler.py -O FinalOutput.json
```

**Note:** 
- **`FinalOutput`** is the the filename, you can put your own filename that you like.
- This command just run the **`ForumCrawler.py`** (a Scrapy Crawl Spider) only.

## How this program works:
Basically, I fed this program a web forum entry/home page and then it will crawl all all the index urls, threads urls and page-flipping urls. 

The output of these 3 different urls will be stored in each different text file namely, **`index_url.txt`**, **`thread_url.txt`** and **`page_flipping_url.txt`**
respectively. After that, the program will find out the pattern of the 3 different types of urls and **`convert each of them to regular expression`**.

So now, we have the regular expression for **`index_url`**, **`thread_url`** and **`page_flipping_url`**. Then, **`ForumCrawler.py`** just need to get 
these 3 regular expression and perform crawling.
(Refer to **How to run** section)

## Website used to learn links' patterns and create regular expression:
Either one of the websites below will do since both produce the same link structure pattern:
- http://www.sixcrazyminutes.com/forums/ **(I use this)**
- https://www.gardenstew.com/

### How to run the learning links' patterns and create regular expression:###
Before start running, DELETE the **`index_url.txt`**, **`thread_url.txt`**, **`page_flipping_url.txt`** and **`URL_Regex.txt`**. 
Then, go to **`main.py`** and run it! (Will take some time)

## Web forum that can be crawled
Most of the web forums that was built by using [XenForo](https://xenforo.com/) can be crawled. Here are some of the lists you can try:

- https://www.namepros.com/
- https://www.gardenstew.com/
- http://www.sixcrazyminutes.com/forums/
- http://www.sportsjournalists.com/forum/
- https://www.bladeforums.com/
- https://forums.sufficientvelocity.com/
- https://www.physicsforums.com/
- https://www.bigfooty.com/forum/
- https://www.cigarpass.com/community/

**Note:** 
You can find tons of XenForo forums here and have a try:
- https://xenforo.com/community/threads/the-large-xenforo-forums-list.87974/
