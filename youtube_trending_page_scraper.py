from bs4 import BeautifulSoup
from datetime import date
import requests
import csv
import re
import json

source = requests.get("https://www.youtube.com/feed/trending").text

soup = BeautifulSoup(source, 'lxml')
# here I used the lxml type
csv_filename = 'YouTube_Trand_videos_{}.csv'.format(date.today())
# I gave the csv_filename a static name and data, if file doesn't exist it will be created 

# also with json_file
json_filename = 'YouTube_Trand_videos_{}.json'.format(date.today())


# At the first we open the csv file with open context manager
with open(csv_filename,'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    # We' writing row's to the file
    csv_writer.writerow(['Title', 'URL', 'Username', 'Duration', 'Views'])

    #find all div's with class yt-lockup-content
    for content in soup.find_all('div', {'class':"yt-lockup-content"}):

        try:
            #passing to title the text included in tag <a>
            title = content.h3.a.text
            # print(title)

            # passing all required data to variables
            duration = content.find('span', {'class':"accessible-description"}).text
            username = content.find('a', {'class':"yt-uix-sessionlink spf-link"}).text
            url = "https://www.youtube.com"
            url += content.find('a', {'href':re.compile(r'[/]([a-z]|[A-Z])\w+')}).attrs['href']
            views = content.find('ul', {'class':"yt-lockup-meta-info"}).contents[1].text

            description = content.find('div', {'class':"yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2"}).text
            # print(description)

        except Exception as e:
            description = None

        print('\n')
        #writing data into csv file
        csv_writer.writerow([title, url, username, duration, views])


# Last, program converting our csv file to json
with open(csv_filename, 'r') as file:
    reader = csv.DictReader(file)

    out = json.dumps([row for row in reader])
    with open(json_filename, 'w') as jsfile:
        jsfile.write(out)

print("Done")
