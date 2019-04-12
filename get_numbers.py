from bs4 import BeautifulSoup
import requests
from lxml import etree
from urllib.request import urlopen
from multiprocessing import Pool
from itertools import repeat
import sys
from slugify import slugify


xpath='//*[@id="nmm"]/body/div[2]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[4]/div/button[1]/span/text()'

sys.setrecursionlimit(20000)

link='https://www.lento.pl/praca/szukam-pracy.html?page='
numbers=list()

def get_number(page):
  write_to_file=''
  write_to_log=''
  href=''
  try:
    href=page[0].find_all("div", {"class":"title-list-item"})[0].find_all('a')[0]['href']
  except :
    slug=page[0].text
    temp=slugify(slug)
    if(slug[-1]=='.' or slug[-1]==','):
      slug=temp+'-'
    else:
      slug=temp
    name=page[1].find_all("div", {"class":"atr-list-col"})[0].text
    idd=page[1].find_all("div", {"class":"favorite-adlist licon-heart-l favorite-ad"})[0]['data-id']
    href='https://'+name.lower()+'.lento.pl/'+slug+','+idd+'.html'
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
      write_to_file=n[0].strip('\n')
      return [1,write_to_file,write_to_log]
      # n=soup_page.find_all("button", {"class":"btn btn-call-blue phone-full"})[0].find_all('span')[0].text
    else:
      write_to_log='No number on '+href
      return [0,write_to_file,write_to_log]
  except:
    write_to_log='No number on '+href
    return [0,write_to_file,write_to_log]

log=open('logs_2.txt','w')
client_id='Kaustav'
for i in range(506,869):
  print('Page: '+str(i+1))
  with open('results/page_'+str(i+1)+'.txt','w') as ffff:
    # req = urllib.request.Request(link+str(i+1)).add_header('Client-ID', client_id)
    # r = urllib.request.urlopen(req,timeout=10).read()
    r = requests.get(link+str(i+1))
    soup = BeautifulSoup(r.text,"html.parser")
    # listings = soup.find_all("div", {"class":"desc-list-row"})
    # print(len(listings))
    listings = [[x,x.parent.find_all("td",{"class":"atr-list-row hidden-xs"})[0]] for x in soup.find_all("td", {"class":"desc-list-row"})]

    print('Number of links: '+ str(len(listings)))
    j=0
    pool = Pool()
    # res= [pool.apply_async(get_number, args=(listings,ffff,log))]
    response=list(pool.map(get_number,listings))
    for resp in response:
      j=j+resp[0]
      if(resp[1]):
        print(resp[1],file=ffff)
      if(resp[2]):
        print(resp[2],file=log)
    print(str(j)+' Numbers found out of : '+str(len(listings))+' links')
log.close()
with open('numbers.txt','w') as f:
  for n in numbers:
    print(n,file=f)
