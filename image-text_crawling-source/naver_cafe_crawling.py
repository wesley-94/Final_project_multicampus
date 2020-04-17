from selenium import webdriver
import pandas as pd
import time

driver = webdriver.Chrome()
driver.implicitly_wait(3)

id = 'rladhlthf123'
pw = 'kws0926!!'

# 네이버 로그인
driver.get('https://nid.naver.com/nidlogin.login')
driver.execute_script("document.getElementsByName('id')[0].value=\'"+ id +"\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'"+ pw +"\'")                     
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

# 숨겨진 URL
pageNum = 1
hiddenurl = 'https://cafe.naver.com/firenze?iframe_url=/ArticleList.nhn%3Fsearch.clubid=10209062%26search.menuid=23%26search.boardtype=L%26search.totalCount=151%26search.page={}'.format(pageNum)
driver.get(hiddenurl) # 숨겨진 URL로 들어가기

# frame 전환 [pc모드에서만 필요한 내용]
driver.switch_to.frame("cafe_main")

# 각 페이지에서 15개 글에 대해 제목, 본문 내용 추출하는
# for문 완성해보기
title_content=[]
body_content=[]
for j in range(1,1000+1):
    for i in range(1,15+1):
        k = 2*i-1

        # 각 글에 들어가기
        driver.find_element_by_xpath(f'//*[@id="main-area"]/div[6]/form/table/tbody/tr[{k}]/td[2]/span/span/a[1]').click()

        # 제목 내용 추출하기
        try:
            title = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/table/tbody/tr/td[2]/span").text
    #         print(title)
            title_content.append(title)
        except:
            title = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/table/tbody/tr/td[1]/span").text
    #         print(title)
            title_content.append(title)

        # 본문 내용 추출하기
        body = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[5]").text
        body_content.append(body)

        # 항목 확인
        if i % 10 == 0:
            print(f"{i}번째 글 크롤링 완료")

        # 페이지 목록으로 돌아가기
        driver.find_element_by_css_selector('#main-area > div.list-btn-nor2.upper-list > div.fr > div > p > a').click()
        
    # 다음 페이지로 넘어가기
    if j % 10 == 0:
        print(f"{j}+1번째 페이지 접속")
        driver.find_element_by_css_selector('#main-area > div.prev-next > table > tbody > tr > td.pgR > a > span:nth-child(1)').click()
    else:
        p = j % 10 + 1
        print(f"{p}번째 페이지 접속")
        driver.find_element_by_xpath(f'//*[@id="main-area"]/div[8]/table/tbody/tr/td[{p}]/a').click()

len(body_content) # 몇 개의 글이 긁히는지 확인 -- 거의 모든 글이 긁어와지고 있는 것을 확인했음

body_content = " ".join(body_content)

with open("review_italy_유랑.txt","w", encoding="UTF-8") as f :
    f.write(body_content)
