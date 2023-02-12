from datetime import datetime, timedelta, timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import time, random, sys, os
from multiprocessing import Process, Queue
from urllib.request import urlretrieve


# face_of_celebrities 폴더안에
# 다양한 연예인 폴더들이 있고
# 해당 연예인 폴더안에는 사진들이 존재하게됩니다

# 수정하세요
img_folder = "../../faces_of_celebrities" # 파일 경로
img_folder=str(os.path.abspath(img_folder))
# print(f'리플레이스전 {img_folder}')
img_folder=img_folder.replace('\\','/')
# print(f'리플레이스후 {img_folder}')

if not os.path.isdir(img_folder) : # faces_of_celebrities폴더안에 새로운 폴더 생성
    os.mkdir(img_folder)



chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) # 용도에 맞는 크롬드라이버 버전 다운로드
def crawling_celebrity_pics(name: str): # 이름이 name인 연예인
    global num
    img_link_list=[] # 이름이 name인 연예인의 사진들의 링크가 저장되는 리스트입니다

    path=img_folder+f'/face_{num}'
    # print(path)
    if not os.path.isdir(path) : # faces_of_celebrities폴더안에 새로운 폴더 생성
        os.mkdir(path)
    
    
    # 뽐뿌이동
    URL='https://www.ppomppu.co.kr/zboard/zboard.php?id=star&page_num=20&category=3&search_type=sub_memo&keyword='
    driver.get(URL)
    driver.implicitly_wait(1)
    
    # 1. 연예인 검색
    driver.find_element(By.XPATH,'//*[@id="keyword"]').send_keys(name) 

    # 2. 검색 버튼 클릭
    driver.find_element(By.XPATH,'/html/body/div/div[2]/div[6]/div[1]/table[6]/tbody/tr[2]/td/table/tbody/tr/td[2]/span/input[2]').click() 
    driver.implicitly_wait(1)
    
    # https://www.ppomppu.co.kr/zboard/zboard.php?id=star&page=1&category=3&search_type=subject&keyword=%B0%F8%C0%AF&divpage=40
    # https://www.ppomppu.co.kr/zboard/zboard.php?id=star&page=2&category=3&search_type=subject&keyword=%B0%F8%C0%AF&divpage=40
    # https://www.ppomppu.co.kr/zboard/zboard.php?id=star&page_num=20&category=3&search_type=sub_memo&keyword=%BE%C6%C0%CC%C0%AF
    
    while True:
        for i in range(2,7):
            for j in range(1,5):                
                try:
                    # 3. 들어가려는 이미지 제목이 내가 검색한 연예인과 같은지 확인 ('공유' 로 검색했을때 '공유림'이 나오는것을 방지)
                    사진제목=driver.find_element(By.XPATH,f'/html/body/div/div[2]/div[6]/div[1]/table[2]/tbody/tr[{i}]/td[{j}]/div/ul/li[2]/span/a/font').get_attribute("textContent")
                    if 사진제목!=name:
                        continue
                    
                    # 4. 이미지 클릭
                    driver.find_element(By.XPATH,f'/html/body/div/div[2]/div[6]/div[1]/table[2]/tbody/tr[{i}]/td[{j}]/div/ul/li[1]/a/img').click() 
                    driver.implicitly_wait(1)
                except:
                    continue # 에러발생시 스킵

                try:
                    # 5. 이미지 url 가져오기
                    img_URL=driver.find_element(By.XPATH,'/html/body/div/div[2]/div[6]/div/table[5]/tbody/tr[1]/td/table/tbody/tr/td/p[2]/img').get_attribute("src")
                except: 
                    driver.back() # 에러발생시 뒤로가기      
                    driver.implicitly_wait(1)               
                    continue
                
                # 6. 이미지 리스트에 저장하기
                img_link_list.append(img_URL)
                
                # 7. 다시 뒤로가기 (메인으로)
                driver.back()
                driver.implicitly_wait(1)
                
        
        # 8. 링크(사진) 다운로드
        for index, link in enumerate(img_link_list):
            urlretrieve(link, path+f'/{index+1}.jpg')    
            driver.implicitly_wait(1)
        
        # 9. 다음페이지로 이동 클릭!
        try:
            page_text=driver.find_element(By.XPATH,'/html/body/div/div[2]/div[6]/div[1]/table[4]/tbody/tr[2]/td/nobr/a[2]/font').get_attribute("textContent")
            if page_text=='-이전페이지': # 버튼이름이 이전페이지면 종료(다음페이지가 존재하지않는다=마지막페이지)
                break
            
            driver.find_element(By.XPATH,'/html/body/div/div[2]/div[6]/div[1]/table[4]/tbody/tr[2]/td/nobr/a[2]/font').click() 
            driver.implicitly_wait(1)  
        except:
            break

        print(f'{name} pic crawling done {num}')
    
    num+=1
    
# /html/body/div/div[2]/div[6]/div[1]/table[2]/tbody/tr[2]/td[1]/div/ul/li[2]/span/a/font/b
# /html/body/div/div[2]/div[6]/div[1]/table[2]/tbody/tr[2]/td[2]/div/ul/li[2]/span/a/font/b
# /html/body/div/div[2]/div[6]/div[1]/table[2]/tbody/tr[3]/td[2]/div/ul/li[2]/span/a/font/b

num=1 # 폴더 이름짓는 변수
# 연예인 이름들어간 리스트 만들기(연예인 이상형 월드컵 참고)
name_list=['서강준', '차은우', '현빈', '공유', '박서준', '남주혁', '이동욱', '정해인', '박보검', '최우식', '박형석', '송중기', '윤시윤', '조정석', '유연석', '육성재', '김우빈', '조인성', '유지태', '원빈', '고수','장동윤', '이정재', '이준기', '이민호', '이현우', '유아인', '안우연', '최웅', '박솔로몬', '송승헌', '홍빈', '박시후'
           , '이태선', '강은탁', '강지환', '조한선', '장동건', # 남자 배우 40
           '배수지', '한소희', '김유정', '신세경', '고윤정', '임윤아', '박은빈', '한지민','전지현', '이주빈', '김지은', '김지수', '권나라', '이혜리', '설인아', '연우', '박규영', '손예진', '이유비', '박보영', '김지원', '이민정', '김다미', '한효주', '이은재', '김태리', '조보아', '배윤경', '홍수주', '신예은', '정은지', '박민영', 
           '이영애', '조이현', '이다희', '장희령', '김태희', '신혜선',# 여자 배우 40
           '박효신', '나얼', '하현우', '임창정', '권정열', '정승환', '김동률', '윤도현', '성시경', '폴킴', '이승기', '이승윤', '김범수', '김경호', '양다일', # 15
           '윤하', '아이유', '거미', '이선희', '에일리', '소향', '펀치', '권진아', '스텔라장', '벤', '케이시', '이수현', '안예은', '장혜진', '강민경','백지영',
           '윈터', '유아', '카리나', '안유진', '제니', '슬기', '설윤', '아이린', '지수', '장원영', '조이', '나연', '지효', '레이', '로제', '권은비', '사나', '웬디',
           '종현', '슈가', '제이크', '김석진', '뷔', '호시', '성훈', '마크', '창섭', '엠제이', '윤정한', '수호', '전정국', '박지훈', '카이', '정우', '윤재혁']
# name_list=['서강준', '차은우', '현빈', '공유']
for name in name_list:
    crawling_celebrity_pics(name)




print('all crawling done')









# def work(ID,PW,year,month,row,col):
    
#     op=Options()
#     path=f'\ID_{ID}'
#     op.add_experimental_option('prefs', {'download.default_directory':r'D:\_flexsys_31\Desktop\새 폴더\crawled_exelfiles'+path}) # 로그인한 ID를 이름으로 갖는 파일명을 생성합니다
#     browser = webdriver.Chrome(r"D:\_flexsys_31\Desktop\chromedriver.exe", options=op)

#     # 1. 한전파워플래너 이동
#     browser.get('https://pp.kepco.co.kr/intro.do')

#     # 2. id, pw 입력
#     browser.find_element(By.XPATH,'//*[@id="RSA_USER_ID"]').send_keys(ID) 
#     browser.find_element(By.XPATH,'//*[@id="RSA_USER_PWD"]').send_keys(PW) 

#     # 3. 로그인 버튼 클릭
#     browser.find_element(By.XPATH,'//*[@id="intro_form"]/form/fieldset/input[1]').click() 

#     # 4. 시간대별 실시간 사용량 이동
#     browser.get('https://pp.kepco.co.kr/rs/rs0101N.do?menu_id=O010201')

#     # 5. 년,월 드롭다운에서 고르기
#     browser.find_element(By.XPATH,'//*[@id="SELECT_DT"]').send_keys('1234') # 달력버튼 누르기
    
#     month=str(int(month)-1)        
#     dropdown=Select(browser.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[2]'))
#     dropdown.select_by_value(month)
#     month=str(int(month)+1) 
    
#     dropdown=Select(browser.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[1]'))
#     dropdown.select_by_value(year)
    
    
#     # 6. 달력에서 알맞는 일 고르기
#     browser.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[{row+1}]/td[{col+1}]/a').send_keys(Keys.ENTER) 
    
#     # 7. 조회버튼 클릭
#     button=browser.find_element(By.XPATH,'//*[@id="txt"]/div[2]/div/p[2]/span[1]/a') 
#     browser.execute_script("arguments[0].click();", button)

#     # 8. 엑셀다운로드 버튼 클릭
#     button=browser.find_element(By.XPATH,'//*[@id="txt"]/div[2]/div/p[2]/span[2]/a')
#     browser.execute_script("arguments[0].click();", button)

#     time.sleep(random.uniform(1,4))

#     # print(f'{year}-{month}-{day} ID:{ID} done')

# # 구하고자 하는 날짜 범위를 입력해주세요
# def date_range(start, end):
#     start = datetime.strptime(start, "%Y-%m-%d")
#     end = datetime.strptime(end, "%Y-%m-%d")
#     # dates = [(start + timedelta(days=i)) for i in range((end-start).days+1)]
#     dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
#     return dates

# dates = date_range("2022-11-24", "2022-12-12") 
# # for datess in tqdm(range(len(dates))):

# # print(dates)
# for datess in range(len(dates)):
#     date=dates[datess]
#     # date=kst-timedelta(days=1) # 하루전 날짜를 구합니다
#     # 어제 날짜 년, 월, 일 추출(문자열 형식)
#     year=date[0:4]
#     month=date[5:7]
#     day=date[8:10]

#     # 해당월의 1일은 어떤요일인지 파악합니다(달력을 그리기 위함)
#     start_of_month=year+'-'+month+'-'+'01'
#     start_of_month_weekday = datetime.strptime(start_of_month, '%Y-%m-%d').weekday() 

#     # 달력을 그립니다(파워플래너 달력과 일치하는 달력을 출력합니다)
#     import numpy as np
#     calendar=[0]*(start_of_month_weekday+1)+[i for i in range(1,32)] 
#     new_calendar=calendar+[0]*(7-len(calendar)%7) # 2차원 배열로 전환하기위해 0을 추가해줍니다
#     new_calendar=np.array(new_calendar).reshape(-1,7).tolist() # 넘파이 reshape 함수를 이용합니다
#     # 달력에서 어제 날짜의 좌표를 찾습니다
#     found=0
#     row=0
#     while True:
#         for col in range(7):
#             if new_calendar[row][col]==int(day):
#                 found+=1
#                 break
#         if found==1:
#             break
#         row+=1

#     #########
#     # id, pw 리스트(셀레니움을 이용하여 로그인)
#     account=[("1116129303", "se430226**"),("1116129349", "power6900**"),("1116129394", "sa0803####"),
#             ("1120946271", "p1318144728!@"),("1116094475", "msj4475**"),("1128312207", "s12345678#"),("0539622531","onfs123456")] # id, password 순서
#     if __name__ == "__main__":
#         th1 = Process(target=work, args=(account[0][0], account[0][1],year,month,row,col))
#         th2 = Process(target=work, args=(account[1][0], account[1][1],year,month,row,col))
#         th3 = Process(target=work, args=(account[2][0], account[2][1],year,month,row,col))
#         th4 = Process(target=work, args=(account[3][0], account[3][1],year,month,row,col))
#         th5 = Process(target=work, args=(account[4][0], account[4][1],year,month,row,col))
#         th6 = Process(target=work, args=(account[5][0], account[5][1],year,month,row,col))
#         th7 = Process(target=work, args=(account[6][0], account[6][1],year,month,row,col))

#         th1.start()
#         th2.start()
#         th3.start()
#         th4.start()
#         th5.start()
#         th6.start()
#         th7.start()

#         th1.join()
#         th2.join()
#         th3.join()
#         th4.join()
#         th5.join()
#         th6.join()
#         th7.join()

# # def close_new_tabs(driver):
# #     tabs = driver.window_handles
# #     while len(tabs) != 1:
# #         driver.switch_to.window(tabs[1])
# #         driver.close()
# #         tabs = driver.window_handles
# #     driver.switch_to.window(tabs[0])

# # close_new_tabs(browser)
# # print('done closing tabs')