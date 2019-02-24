# https://www.ekonyv.hu/hu/tematikak/sci-fi?id=83&str=1

import wget
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def exists(site, path):
     conn = httplib.HTTPConnection(site)
     conn.request('HEAD', path)
     response = conn.getresponse()
     conn.close()
     return response.status == 200

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
headers = {'user-agent': 'test-app/0.0.1'}
# sectionUrl = input("► Please input the base url: ")

sectionUrl = input("Please paste here the ekonyv.hu link: ")
pageCounter = 1
my_url = sectionUrl + "&str=" + str(pageCounter)
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")
totalNumOfPages = page_soup.findAll("a", {"title":"utolsó oldal"})
totalNumPagesFirstOccurence = totalNumOfPages[0]
gettingPagesString = totalNumPagesFirstOccurence["href"]
totalPages = gettingPagesString.rpartition("str=")[2]
print(totalPages)

for _ in range(int(totalPages)):

	my_url = sectionUrl + "&str=" + str(pageCounter)
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll("div", {"class":"bookListText"})

	containerCounter = 0

	for container in containers:
		container = containers[containerCounter]
		#print(container)
		bookTitleWithChars = container.a.text.replace("/", "-")
		bookTitleWithDots = bookTitleWithChars.replace("?", "")
		bookTitle = bookTitleWithDots.replace(":", "-")
		linkToBook = container.a["href"]
		bookId = linkToBook.rpartition("eid=")[2]
		authorRaw = container.find("a", {"class":"author"})
		if authorRaw == None:
			authorText = 'Ismeretlen'
		else:
			authorText = authorRaw["title"]
			
		urlForBookPreviewEpub = "https://www.ekonyv.hu/download-preview.php?id=" + bookId + "&format=epub"
		
		wget.download(urlForBookPreviewEpub, authorText + " - " + bookTitle + ".epub")
		
		
		print("Downloaded epub preview for: " + authorText + " - " + bookTitle)
		
		containerCounter = containerCounter + 1
	
	pageCounter = pageCounter + 1