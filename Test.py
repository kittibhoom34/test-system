#ยากมาก
#no
#easy
from bs4 import BeautifulSoup4
import requests
from datetime import datetime , timedelta

global limit
limit = 2

def check_time(time) :
    now = datetime.now()
    timelimit = now - timedelta(days=limit)
    check = 1
    if datetime.strptime(time, '%Y-%m-%d %H:%M:%S') > timelimit :
        check = 0
    return check

def AddZero(val) :
    if int(val) < 10 :
        res = "0"+val 
    else :
        res = val
    return res

def ConvertMonth(month) :
    switcher = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }
    return switcher.get(month)

def ConvertDatetime(dt) :
    # By: workplace  on 31 May 2021 - 10:30
    dt = dt.split(' ')
    day = AddZero(dt[4])
    month = ConvertMonth(dt[5])
    year = dt[6]
    time = dt[8] + ":00"
    timepost = f"{year}-{month}-{day} {time}"
    return timepost

def get_content(url) :
    res = requests.get(url)
    soup = BeautifulSoup(res.content , "html.parser")
    dt = ConvertDatetime(soup.find("span" , attrs={"class":"submitted"}).text)
    content = soup.find("div" , attrs={"class":"node-content"}).text
    return " ".join(content.split()) , dt

def blognone() :
    website = "https://www.blognone.com"
    page = 0
    while True :
        url = f"{website}/node?page={page}"
        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.content , "html.parser")
        content_ = soup.find("div" , attrs={"id": "content"})
        news = content_.find_all("h2" , attrs={"itemprop":"name"})
        for i in range(len(news)):
            title = news[i].text
            link = f'{website}{news[i].find("a").get("href")}' #https://www.blognone.com/none/2555
            content , time = get_content(link)
            
            if check_time(time) == 0 :
                print(f"title : {title}\ncontent : {content}\ntime : {time}")
                print("="*30)
            else :
                continue

        if page == 3 :
            break
                
        page += 1

if __name__ == '__main__' :
    blognone()


# เวลาปัจจุบัน now = datetime.now()
# เวลาที่ได้จากเนื้อหา time = datetime.strptime(time, '%Y-%m-%d')
# abs(now - time).days   -> ผลลัพธ์ : ตัวเลข ถ้าเวลาปัจจุบันลบเวลาเนื้อหาแล้วเกิน 1 วัน ค่าจะเป็น 1 แต่ถ้าไม่เกินจะเป็น 0 
# แล้วจึงเอาค่า ไปเทียบกับเวลาที่ limit อีกที ถ้า limit คือ 2 หากเวลาเกิน 2 ค่อยข้ามการทำงาน
