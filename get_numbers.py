from bs4 import BeautifulSoup
import requests
from lxml import etree
from urllib.request import urlopen


xpath='//*[@id="nmm"]/body/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[4]/div/button[1]/span/text()'


link='https://www.lento.pl/praca/szukam-pracy.html?page='
numbers=list()

log=open('logs.txt','w')
client_id='Kaustav'
for i in range(867):
  print('Page: '+str(i+1))
  with open('results\\page_'+str(i+1)+'.txt','w') as ffff:
    # req = urllib.request.Request(link+str(i+1)).add_header('Client-ID', client_id)
    # r = urllib.request.urlopen(req,timeout=10).read()
    r = requests.get(link+str(i+1))
    soup = BeautifulSoup(r.text,"html.parser")
    listings = soup.find_all("div", {"class":"title-list-item"})
    print('Number of links: '+ str(len(listings)))
    j=0
    for page in listings:
      href=page.find_all('a')[0]['href']
      # req2 = urllib.request.Request(href).add_header('Client-ID', client_id)
      # rr=urllib.request.urlopen(req2,timeout=10).read()
      if('http' not in href):
        href='http://'+href
      # rr=requests.get(href)
      try:
        rr=urlopen(href)
        htmlparser = etree.HTMLParser()
        tree = etree.parse(rr, htmlparser)
        # print(tree.xpath(xpath))
        # soup_page = BeautifulSoup(rr.text,"html.parser")
        n=tree.xpath(xpath)
        if(n):
          numbers.append(n[0].strip('\n'))
          print(n[0].strip('\n'))
          print(n[0].strip('\n'),file=ffff)
          j=j+1
          # n=soup_page.find_all("button", {"class":"btn btn-call-blue phone-full"})[0].find_all('span')[0].text
        else:
          print('No number on '+href,file=log)
      except:
        print('No number on '+href,file=log)
    print(str(j)+' Numbers found in page: '+str(i+1))

with open('numbers.txt','w') as f:
  for n in numbers:
    print(n,file=f)
