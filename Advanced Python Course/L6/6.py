import requests
from bs4 import BeautifulSoup
import difflib
import time

def getPageContent(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error while accessing page {url}: {e}")

def getSoup(url):
    page_content = getPageContent(url)
    soup = BeautifulSoup(page_content, "html.parser")

    for script in soup(["script", "style"]):
        script.extract() 
    return soup.get_text()

def printDiff(diff):
    print("Found changes: ")
    for line in diff:
        if not line.isspace() and not line.startswith('*'):
            print(line.lstrip())

def monitorPage(url):
    prev = getSoup(url)

    while True:
        soup = getSoup(url)
        if prev != soup:
            old = prev.splitlines()
            new = soup.splitlines()

            diff = difflib.context_diff(old, new)
            printDiff(diff)

            prev = soup
        else:
            print("No changes")
        time.sleep(10)

monitorPage("https://zapisy.ii.uni.wroc.pl")
