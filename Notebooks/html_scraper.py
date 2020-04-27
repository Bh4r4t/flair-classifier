# In this script i tried to scrape reddit data using beautiful soup. Some complexities were there in scraping
# as the pages of reddit are dynamic so the complete page does not load at once, so i have to get the id of the last post on a page and use that to 
# open next page, So this process was very time consuming and after certain number of pages no data is available so the data scraped is also less.

# This scrapper is not useful anymore, check the scrapper used in the project in 'Data Scraping.ipynb'

from bs4 import BeautifulSoup as bsp
import csv
import requests
import re

#url = 'https://www.reddit.com/r/india/'

class Scrapper:
    """
    holds all the methods to scrape data(posts) from reddit webpage(url)
    """
    def __init__(self, url):
        # link to reddit webpage(base url)
        self.url = url
        # list to store all the data dictionaries
        self.data = []
        
    def requestHTML(self, nextUrl=None):
        """
        fetch html from source url
        Args:
            nextUrl: url of the next page
        Return:
            content: parsed html structure
        """
        if nextUrl :
            link = nextUrl
        else:
            link = self.url
        response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
        content = bsp(response.text, 'html.parser')
        return content

    def getAllPosts(self, content):
        """
        seperate out every post's html structure
        Args:
            content : html content as parsed by beautifulsoup
        Return:
            posts: list of all posts' html structure
            ID: html id of the last post on the webpage,
        """
        block = re.compile("[\d\w]{23} [-\d\w]{23} scrollerItem [-\d\w]{23} [-\d\w]{23} Post [\d\w]{9}")
        posts = content.find_all('div', class_=block)
        return posts, posts[-1]['id']
    
    def getComments(self, url):
        
        # TODO: comments are not properly extracted
        """
        returns best 10 (or less) comments on the input post(url)
        Args:
            url (str): url of the post
        Return:
            best 10 comments as single text structure.
        """
        response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
        soup = bsp(response.text, 'html.parser')
        allcomments = soup.find_all('div', {'class':'_292iotee39Lmt0MkQZ2hPV RichTextJSON-root'})
        return allcomments
        comments =""
        for i in range(min(10, len(allcomments))):
            para_comments = allcomments[i].find_all('p', class_='_1qeIAgB0cPwnLhDF9XSiJM')
            for all_para in para_comments:
                comments+=(" "+ all_para.text)
        return comments[1:]
    
    #def scrapeComments(string):
    #    return string
    
    def singlePostData(self, content):
        """
        extracts all the below field data from a single post
        and returns a dictionary of all those elements
        Args:
            content: (single post)element from which data-subelement to be seperated
            
        Returns:
            dictionary object containing all the extracted data.
            headline        (str): post headline
            rating          (int): total of likes and dislikes on post
            flair           (str): flair (tag) of the post
            body            (str): text segment or description part 
                                   of the post(in case of images body is null)
            author          (str): author of the post
            link            (str): link of the reddit post
            num_of_comments (int): number of comments on the post
            comments        (str): 'best' 10 comments on the post
        """
        #link of post
        link = content.find('a', class_='_3jOxDPIQ0KaOWpzvSQo-1s')['href']
        
        # Rating of the post
        rating = content.find('div', class_='_1rZYMD_4xY3gRcSS3p8ODO _25IkBM0rRUqWX5ZojEMAFQ').text
        try:
            if rating[-1]=='k' :
                rating =float(rating[0:-1])*1e3
            int(rating)
        except:
            rating = 0
            
        # number of comments on the post
        num_comments = content.find('span', class_='FHCV02u6Cp2zYL0fhQPsO').text.split()[0]
        try:
            if num_comments[-1]=='k':
                num_comments = float(num_comments[0:-1])*1e3
            int(num_comments)
        except:
            num_comments=0
        
        #author = content.find('a', class_='_2tbHP6ZydRpjI44J3syuqC _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE').text
        #author = author.replace('\n', '')
        
        # flair of post
        try:
            flair = content.find('div', class_='_2X6EB3ZhEeXCh1eIVA64XM _2hSecp_zkPm_s5ddV2htoj _2VqfzH0dZ9dIl3XWNxs42y aJrgrewN9C8x1Fusdx4hh').text
        except:
            flair = ""
            
            
        # headline of post
        try:
            headline = content.find('h3').text
        except:
            headline = ""
        
        
        # body of post (text)
        feedAll = content.find_all('p', class_='_1qeIAgB0cPwnLhDF9XSiJM')
        feed=""
        for f in feedAll:
            feed+=(" " + f.text)
        feed = feed[1:]
        
        #top 10 comments
        comments = self.getComments(link)
        
        return ({'headline': headline,
                 'rating': rating,
                 'flair': flair,
                 'body': feed,
                 #'author': author,
                 'link': link,
                 'num_of_comments': num_comments,
                 'comments': comments})        
    
    
    def getNextPage(self, content):
        """
        Args:
            content: current webpage 
        Return:
            next: url of next web page
        """
        nextPage = content.find('link', {'rel':'next'})['href']
        return nextPage
    
    
    def scrape(self, n, thread):
        """
        main function to scrape contents from webpage
        Args:
            url: base url
            n: number of pages to be scraped
            thread (optional)(str): sorting posts as filter(thread)
                    can be-> Hot, Best, New, Top, Rising`
        Return:
            data:
                list of extracted data as dictionary
        """
        if(thread):
            self.url += (thread+'/')
        print("======= scraping stared at '{}' =======".format(self.url))
        next_base = self.url+'?after='
        next_page = ""
        total=0
        for i in range(n):
            # updates next page url
            next_page = next_base + next_page
            #print(next_page)
            # fetch next page
            content = self.requestHTML(next_page)
            posts, next_page = self.getAllPosts(content)
            for post in posts:
                self.data.append(self.singlePostData(post))
                total=total+1
            print("-> Total {} posts scraped".format(len(posts)))
            print("------ page-{} Done ------".format(i+1))
        print("------posts scraped: {} ------".format(total))
            
        return self.data
    
    
def saveAsCSV(path, dictionary):
    """
    saves list of dictionaries to a csv file
    Args:
        path (str): path where to store csv file along with file name
        dictionary: list of dictionaries
    """
    keys = dictionary[0].keys()
    with open(path, 'w', newline="", encoding='utf-8') as file:
        dict_writer = csv.DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dictionary)
