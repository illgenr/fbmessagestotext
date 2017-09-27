'''Parse Facebook archive message.htm to text

Run the script with:
```
python fbmessagestotext.py path_to_your_archive.jpg 
```
e.g.:
```
python fbmessagestotext.py ../fb-archive
```
'''
import HTMLParser
import BeautifulSoup

# <codecell>
# Custom parser because HTML parser can't handle FB's malformed HTML
class FacebookMessageParser():
	
	userHeader = "<span class=\"user\">Raleigh Sea Illgen"
	paragraphTag = "<p>"
	paragraphCloseTag = "</p>"
	theFeed = "";
	outputFile = file('.\\output.txt')
	
	def parseMessages(self):
		print("Parsing!")

	def feed(self, string):
		
		#output file
		self.outputFile = open('.\output.txt', 'w')
	
		#print string
		self.theFeed = string		
		nextHeaderPosition = self.findNextUserHeaderMatch(0)
		while nextHeaderPosition != -1:
			nextReadPostion = self.findNextParagraph(nextHeaderPosition)
			if nextReadPostion == -1:
				print("next read break")
				break
			nextHeaderPosition = self.findNextUserHeaderMatch(nextReadPostion)
		
		print("next header break")
		
		self.outputFile.close()
		
	def findNextUserHeaderMatch(self, position):
		#print "Header pos: "
		return self.theFeed.find(self.userHeader, position)
		
	def findNextParagraph(self, position):
         startPosition = self.theFeed.find(self.paragraphTag, position)
         endPostition = self.theFeed.find(self.paragraphCloseTag, position)
         startPosition = startPosition + 3
         print("Start position: ", startPosition)
         print("End position: ", endPostition)
         print(self.theFeed[startPosition:endPostition])
         self.outputFile.write(self.theFeed[startPosition:endPostition])
         self.outputFile.write("\n")
         return endPostition
# <codecell>		

h = HTMLParser.HTMLParser()

myParser = FacebookMessageParser();

f = open('..\\facebook-raleighc-data\\html\\messages.htm', 'r')
messagesHTMString = f.read()
soup = BeautifulSoup.BeautifulSoup(messagesHTMString, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
#print(soup)

myParser.feed(str(soup));