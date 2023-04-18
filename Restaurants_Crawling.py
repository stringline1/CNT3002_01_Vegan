#2020310548 인공지능융합학과 원현선 - 비건 식당 추천 크롤링 파일

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome('chromedriver')
#네이버에 '서울 비건 식당' 검색 후 지도 클릭했을 때의 링크
driver.get('https://map.naver.com/v5/search/%EC%84%9C%EC%9A%B8%20%EB%B9%84%EA%B1%B4%20%EC%8B%9D%EB%8B%B9')

name_list = []      #식당 이름
menu_list = []      #식당 메뉴 종류 (한식, 양식)
address_list = []   #주소
rating_list = []    #별점
review_list = []    #리뷰

#식당 리스트 화면으로 프레임 전환
driver.switch_to.frame('searchIframe')
time.sleep(1)

#페이지 선택
page = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div[2]/a[6]')
page.click()

#스크롤
scroll_div = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]')
driver.execute_script("arguments[0].scrollBy(0,2000)", scroll_div)
time.sleep(2)
driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
time.sleep(2)
driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
time.sleep(2)
driver.execute_script("arguments[0].scrollBy(0,2000);", scroll_div)
time.sleep(2)


#식당 이름 크롤링
names = driver.find_elements(By.CLASS_NAME, '_3Apve')
for name in names:
    name_list.append(name.get_attribute('innerHTML'))


#식당 종류 (ex.양식, 한식) 크롤링
menus = driver.find_elements(By.CLASS_NAME, '_3B6hV')
for menu in menus:
    menu_list.append(menu.get_attribute('innerHTML'))


#식당 주소 크롤링 (구, 동까지)
addresses = driver.find_elements(By.CLASS_NAME, '_3hCbH')
for address in addresses:
    address_list.append(address.get_attribute('innerHTML'))


#식당 이름 눌러서 상세보기 링크 클릭
for name in names:
    driver.switch_to.default_content()
    time.sleep(1)
    driver.switch_to.frame('searchIframe')
    time.sleep(2)
    name.click()
    #식당 상세보기 프레임 전환
    driver.switch_to.default_content()
    time.sleep(1)
    driver.switch_to.frame('entryIframe')
    time.sleep(2)

    
    try:        #span[3]이 있는 경우 = 별점이 span[1]에 있음, 방문자 리뷰가 span[2]에 있음
        driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[2]/div[1]/div[2]/span[3]/a')
        #방문자 리뷰로 이동
        review_button = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[2]/div[1]/div[2]/span[2]/a')
        review_button.click()
        time.sleep(2)

        #별점 긁기
        rating = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[2]/div[1]/div/div/div[3]/span[1]/em')
        rating_list.append(rating.get_attribute('innerHTML'))

        more_num = 0
        while True:     #리뷰가 더 있으면 더보기 버튼이 있으면 계속 클릭하기 (모든 리뷰 로딩)
            if more_num > 20:
                break
            try:
                more_review = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[2]/div[3]/div[2]/a')
                more_review.click()
                more_num += 1
            except:
                break

            
        #리뷰 긁기
        try:
            all_reviews = []
            reviews = driver.find_elements(By.CLASS_NAME, 'WoYOw')
            for review in reviews:
                all_reviews.append(review.get_attribute('innerHTML'))
            review_list.append(all_reviews)
        except:
            review_list.append('NA')

    except: 
        try:    #span[3]이 없는 경우 = 별점이 없음, 방문자 리뷰가 span[1]에 있음
            #방문자 리뷰로 이동
            review_button = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[2]/div[1]/div[2]/span[1]/a')
            review_button.click()
            time.sleep(2)

            #별점 없음 설정
            rating_list.append('NA')
            
            while True:     #리뷰가 더 있으면 더보기 버튼이 있으면 계속 클릭하기 (모든 리뷰 로딩)
                try:
                    more_review = driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[2]/div[3]/div[2]/a')
                    more_review.click()
                except:
                    break

            #리뷰 긁기
            try:
                all_reviews = []
                reviews = driver.find_elements(By.CLASS_NAME, 'WoYOw')
                for review in reviews:
                    all_reviews.append(review.get_attribute('innerHTML'))
                review_list.append(all_reviews)
            except:
                review_list.append('NA')
        
        except:     #알 수 없는 에러가 발생하는 경우 error_list에 식당 이름 추가
            rating_list.append('NA')
            review_list.append('NA')         


#데이터 프레임으로 변환
d = {'식당 이름':name_list, '메뉴 종류':menu_list, '주소':address_list, '별점':rating_list, '리뷰':review_list }
df = pd.DataFrame(data=d)

#csv 파일로 저장
df.to_csv('SeoulVegan-page5.csv', index = False, header = False, encoding = 'utf-8-sig')

