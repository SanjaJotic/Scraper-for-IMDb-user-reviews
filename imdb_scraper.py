# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:20:10 2018

@author: Lenovo
"""

from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
"""
comment - for number of comments
nc - for number of negative comments
pc - for number of positive comments
"""
comment = 0
nc = 0
pc = 0

headers = {"Accept-Language": "en-US, en;q=0.5"}
"""
pages - links for comments of movies
original link: https://www.imdb.com/title/tt0451279/reviews?ref_=tt_ql_3
on the original link delete string to question mark and add /_ajax?paginationKey= to catch Load More button (it's ajax key)
"""
pages = ['https://www.imdb.com/title/tt0974015/reviews/_ajax?paginationKey=','https://www.imdb.com/title/tt1825683/reviews/_ajax?paginationKey=',
         'https://www.imdb.com/title/tt1386697/reviews/_ajax?paginationKey=', 'https://www.imdb.com/title/tt0451279/reviews/_ajax?paginationKey=', 
         'https://www.imdb.com/title/tt1431045/reviews/_ajax?paginationKey=','https://www.imdb.com/title/tt3501632/reviews/_ajax?paginationKey=',
         'https://www.imdb.com/title/tt2395427/reviews/_ajax?paginationKey=', 'https://www.imdb.com/title/tt3498820/reviews/_ajax?paginationKey=',
         'https://www.imdb.com/title/tt4500922/reviews/_ajax?paginationKey=','https://www.imdb.com/title/tt2557478/reviews/_ajax?paginationKey=' 
         ]

for url in pages: 
    response = get(url, headers = headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # button Load More is cass load-more-data, to click all that buttons and get all reviews
    # we are checking if can find that html tag (if is not None)
    while html_soup.find('div', attrs={'class':'load-more-data'}) is not None:
        reviews_container = html_soup.find_all('div', class_ = 'review-container')
        for review_c in reviews_container:
            # save rating
            if review_c.find('span', class_ = 'rating-other-user-rating') is not None:
                rating = review_c.find('span', class_ = 'rating-other-user-rating')
                rating = int(rating.find('span').text)

                # save date of review
                review_date = review_c.find('span', class_ = 'review-date').text
                date = datetime.strptime(review_date, '%d %B %Y')
                date = date.strftime('%d-%m-%Y')

                # if rating is <=4 save review as negative
                # file name contain tag of neg/pos review, date and number of scraped comment
                if rating <= 4: 
                    p = "neg"
                    comment += 1
                    nc += 1
                    review = review_c.find('div', class_ = 'text show-more__control').text
                    file_name = p + "_IMDB-user-reviews_" + date + "_" + str(comment)
                    with open("corpus/" + file_name + ".txt", "w") as f:
                        f.write(review.encode('utf8'))
                        
                if rating >= 5: 
                    p = "pos"
                    comment += 1
                    pc += 1
                    print comment
                    review = review_c.find('div', class_ = 'text show-more__control').text
                    file_name = p + "_IMDB-user-reviews_" + date + "_" + str(comment)
                    with open("corpus/" + file_name + ".txt", "w") as f:
                        f.write(review.encode('utf8'))  

        # if we find Load More button, click them to open more reviews              
        if html_soup.find('div', attrs={'class':'load-more-data'}) is not None:
            key = html_soup.find('div', attrs={'class':'load-more-data'})['data-key']
            response = get(url + key, headers = headers)
            html_soup = BeautifulSoup(response.text, 'html.parser')

print 'No positive comments:', pc
print 'No negative comments:', nc    

        




