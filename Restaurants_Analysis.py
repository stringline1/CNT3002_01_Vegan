#2020310548 인공지능융합학과 원현선 - 비건 식당 추천 언어분석 파일


import csv
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from collections import Counter
from konlpy.tag import Hannanum
import random


#결과 출력 함수
def print_result(x):
    print('식당 이름: ', name_list[x])
    print('메뉴 종류: ', menu_list[x])
    print('주소: ', address_list[x])
    print('별점: ', rating_list[x])
    link = 'https://map.naver.com/v5/search/'+ str(name_list[x]) +'/place/1512118942?c=14123486.7248590,4516339.2959284,13,0,0,0,dh&entry=plt&isCorrectAnswer=true'
    print('링크: ', link)
    print('-'*20)


#csv 파일 데이터 불러오기
all_res = []

f = open('SeoulVegan.csv', 'r', encoding='utf-8')
content = csv.reader(f)
for i in content:
    all_res.append(i)
f.close()

name_list = []      #식당 이름
menu_list = []      #식당 메뉴 종류 (한식, 양식)
address_list = []   #주소
rating_list = []    #별점
review_list = []    #리뷰
#link = https://map.naver.com/v5/search/+ ' ' +/place/1512118942?c=14123486.7248590,4516339.2959284,13,0,0,0,dh&entry=plt&isCorrectAnswer=true


#각 리스트에 할당
for i in all_res:
    name_list.append(i[0])
    menu_list.append(i[1])
    address_list.append(i[2])
    rating_list.append(i[3])
    review_list.append(i[4])


#주소 저장 방식을 시, 구, 동 리스트로 바꾸어서 변경 ex['서울시','종로구', '명륜3가']
for i in range(0, len(address_list)):
    address_list[i] = word_tokenize(address_list[i])


#각 식당의 리뷰 데이터를 sent_reviews에 저장
sent_reviews = []
for review in review_list:
    #데이터 추출 당시에 리뷰란 크기 제한으로 인해 생긴 엔터키 제거
    remove_enter = review.replace('\n','')
    remove_enter = remove_enter.replace('\\n','')
    remove_enter = remove_enter.replace("'",'')
    remove_enter = remove_enter.replace('...','')
    remove_enter = remove_enter.replace('[','')
    remove_enter = remove_enter.replace(']','')
    remove_enter = remove_enter.replace(',','')

    review = remove_enter

    #sentence tokenizing 작업해서 하나의 리스트(sent_review)에 추가
    sent_review = sent_tokenize(review)

    #중복 리뷰 제거 (크롤링 과정에서 생긴 오류)
    no_repeat = list(set(sent_review))

    #한 문장 (하나의 string)에 모든 리뷰 데이터 저장
    sent = ''
    for i in no_repeat:
        sent += i
        sent += ' '
    
    sent_reviews.append(sent)


#KoNLPy
han = Hannanum()

stop_words = ['진짜', '너무', '매장',  '비건', '논비건','주문', '재료', '소스', '인분', '곳'
              '메뉴', '수', 'ㅎㅎ', '짱', '야채', '굿', '여기', '업체', '음식', '옵션', '장소']
nouns = []
for sent_review in sent_reviews:
    tagging = han.pos(sent_review)
    noun = []
    for i in range(0, len(tagging)):
        if tagging[i][1] == 'N' or tagging[i][1] == 'MA':
            if tagging[i][0] not in stop_words:
                noun.append(tagging[i][0])
    nouns.append(noun)


#자주 등장하는 단어 추출
keywords = []     #식당별 키워드 10 개만 추출
for noun in nouns:
    counter = Counter(noun)
    keywords.append(counter.most_common(n=10))


keywords_list = []
for keyword in keywords:
    keywords_noun = []
    for i in range(0, 10):
        try:
            temp = keyword[i][0]
            keywords_noun.append(temp)
        except:
            keywords_noun.append('NA')
    keywords_list.append(keywords_noun)


#추천할 식당의 인덱스 업데이트
keyword_recommendation = []

suggestion = input('메뉴나 선호하는 사항이 있으면 자유롭게 말해 주세요\n')


#사용자가 입력한 문장에 대한 pos tagging 후 suggestion_noun에 저장
tagging = han.pos(suggestion)
suggestion_noun = []
for i in range(0, len(tagging)):
    if tagging[i][1] == 'N' or tagging[i][1] == 'MA':
        if tagging[i][0] not in stop_words:
            suggestion_noun.append(tagging[i][0])


#모든 식당의 키워드롤 보면서 사용자의 suggestion_noun과 매치하는 것이 있는지 확인
for i in range(0, len(keywords_list)):
    for j in range(0, len(keywords_list[i])):
        for k in range(0, len(suggestion_noun)):
            if keywords_list[i][j] == suggestion_noun[k]:
                keyword_recommendation.append(i)

location = input("방문하고 싶은 서울 내 식당 위치가 어디인가요? 구 혹은 동만 정확하게 입력해 주세요\n")

#사용자가 입력한장소에 있는 음식점들을 location_recommendation에 저장
location_recommendation = []
for i in range (0, len(address_list)):
    for j in range(0, len(address_list[i])):
        if address_list[i][j] == location:
            location_recommendation.append(i)


#사용자가 원하는 키워드와 장소가 매치하는 경우 찾기
res_index = []

for i in range(0, len(keyword_recommendation)):
    for j in range(0, len(location_recommendation)):
        if keyword_recommendation[i] == location_recommendation[j]:
            res_index.append(keyword_recommendation[i])

#매치하는 곳이 없을 경우
if len(res_index)==0:
    print('검색 결과가 없습니다. 더 넓은 범위에서 다시 검색해 보세요.')

#매치할 경우 랜덤으로 출력
else:
    x = random.randint(0, len(res_index)-1)
    print_result(res_index[x])
     
    



    
