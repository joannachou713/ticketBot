from django.shortcuts import render, render_to_response
from selenium import webdriver
from pyquery import PyQuery as pq
from time import sleep
import requests
res = requests.get(url='https://tixcraft.com/activity')
doc = pq(res.text)
doc.make_links_absolute(base_url=res.url)

try:
    concertDateList = []
    for each in doc('#selling > div > div > div > a').items():
        doc2 = pq(each.attr("href"))
        doc2.make_links_absolute(base_url=res.url)
        link = doc2('#content > div > div > ul > li:nth-child(1) > a')
        doc3 = pq(link.attr("href"))
        dateList = []
        for date in doc3("#gameList > table > tbody > tr > td:nth-child(1)").items():
            dateList.append(date.text())
        concertDateList.append(dateList)
    print(concertDateList)
except:
    print(concertDateList)

# Create your views here.
def concertOption(request):

    concertList = []
    doc = pq(url='https://tixcraft.com/activity')
    for each in doc('#selling > div > div > div > h5 > a').items():
        concert = each.text()
        concertList.append(concert)

    localVars = {}
    localVars['concertDateList'] = concertDateList
    localVars['concertList'] = concertList
    
    return render_to_response('index.html',localVars)

def getTicket(request):
    ticketName = request.POST['ticketName']
    ticketNum = int(request.POST['ticketNum'])
    ticketDate = request.POST['ticketDate']
    res = requests.get(url='https://tixcraft.com/activity')
    doc = pq(res.text)
    doc.make_links_absolute(base_url=res.url)

    # 選演唱會
    link = doc('#selling > div > div:nth-child(' + ticketName + ') > div > a')
    buyPage = link.attr("href").replace("detail", "game")
    driver = webdriver.Chrome(r'C:\Users\simuccn\simuccn\Desktop\chromedriver.exe')
    driver.get(buyPage)
    # 選擇日期
    for each in driver.find_elements_by_css_selector("#gameList > table > tbody > tr > td:nth-child(1)"):
        if each.text == ticketDate:
            each.find_element_by_xpath("//../td[4]/input").click()

    # 選擇區域(默認最貴)
    sleep(2)
    js = 'document.querySelector("#group_0 > li:nth-child(1) > a").click();'
    driver.execute_script(js)
    # 我同意
    sleep(2)
    driver.find_element_by_css_selector('#TicketForm_agree').click()
    # 選擇張數
    driver.find_element_by_css_selector('#board > img.closeNotice').click()
    driver.find_element_by_css_selector('#TicketForm_ticketPrice_01 > option:nth-child(' + str(ticketNum + 1) + ')').click()
    c={'name':ticketName}
    c['num'] = ticketNum
    c['date'] = ticketDate
    return render(request, 'result_page.html', c)
