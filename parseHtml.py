from bs4 import BeautifulSoup
import urllib
r = urllib.urlopen('http://localhost:9005/newTask').read()
soup = BeautifulSoup(r, "html.parser")
print soup.find(id="taskId").get_text()

if soup.find(id="userResponse"):
    print "user task"
else:
    print "wizard task"