from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

options=webdriver.ChromeOptions()
options.add_argument('--incognito')
driver=webdriver.Chrome(options=options)
driver.get('https://www.linkedin.com/uas/login')
driver.maximize_window()

username = driver.find_element_by_id('username')
username.send_keys('your_username')
password = driver.find_element_by_id('password')
password.send_keys('your_password')
log_in_button = driver.find_element_by_class_name('from__button--floating')
log_in_button.click()


urls=['https://www.linkedin.com/company/alicorp-saa/posts/?feedView=all',
       'https://www.linkedin.com/company/backus/posts/?feedView=all',
       'https://www.linkedin.com/showcase/linkedin-noticias-america-latina/posts/?feedView=all']

data={
    "name": [],
    "date": [],
    "post": [],
    "likes": [],
    "count_posts":[]
}

for url in urls:
    driver.get(url)
    for i in range(max(0,10)): # here you will need to tune to see exactly how many scrolls you need
        driver.execute_script('window.scrollBy(0, 500)')
        sleep(1)
    
    src=driver.page_source
    soup=BeautifulSoup(src, 'html.parser')
    posts = driver.find_elements_by_xpath('//div[@class="occludable-update ember-view"]')
    
    count_posts = len(posts) -1
    for names, dates, likes, posts in zip(soup.find_all('div',{'class':'display-flex feed-shared-actor display-flex feed-shared-actor--with-control-menu ember-view'}),
                                        soup.find_all('div',{"class":"display-flex feed-shared-actor display-flex feed-shared-actor--with-control-menu ember-view"}),
                                        soup.find_all('div',{'class':'social-details-social-activity update-v2-social-activity'}),
                                        soup.find_all('div',{'class':"occludable-update ember-view"})):


        name = names.find('span',{'class':'feed-shared-actor__title'}).get_text().strip()
        date = dates.find('span',{'class':'visually-hidden'}).get_text().strip()

        if name and date:
            print('name: ' +name.strip())
            print('date: ' +date.strip())
            data["name"].append(name)                
            data["date"].append(date)              

        try:
            post = posts.find('div',{'class':"feed-shared-update-v2__description-wrapper ember-view"}).span.get_text().strip()   

            if post:
                print('post: ' +post.strip())                       
                data["post"].append(post)

        except Exception as e:
                print('post: ' +'')
                data["post"].append('')
        try:
            likes = likes.find('span',{'class':'v-align-middle social-details-social-counts__reactions-count'}).get_text().strip()

            if likes:
                print('likes: ' +likes)        
                data["likes"].append(likes)                            

        except Exception as e:
                print('likes: ' +'0')        
                data["likes"].append('')     
        print('count_posts: ' +str(count_posts))
        data["count_posts"].append(count_posts)
        print('*'*40)
    print('='*120)
    print('\n')
driver.close()

df=pd.DataFrame(data)
df