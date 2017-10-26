'''Parse Facebook archive message.htm to text

Run the script with:
```
python fbmessagestotext.py username idNumber path_to_your_archive
```
e.g.:
```
python fbmessagestotext.py "My Name" 55555555 ../fb-archive
```
'''
import os
import sys
import json
import argparse
import HTMLParser
import BeautifulSoup

# <codecell>
# Custom parser because HTML parser can't handle FB's malformed HTML
class FacebookMessageParser:
    
    userHeader = ""
    userID = "@facebook.com"
    
    currentUser = ""
    lastUserFound = ""
    targetUserFoundInThread = False
    
    divClassThread = "<div class=\"thread\">"
    spanClassUser = "<span class=\"user\">"
    spanClassCloseTag = "</span>"
    paragraphTag = "<p>"
    paragraphCloseTag = "</p>"
    collatedParagraphs = []
    
    theFeed = "";
    outputFile = file(os.devnull)
        
    def __init__(self, name, id):
         self.userHeader = name
         self.userID = id + self.userID
         print(self.userHeader)
         print(self.userID)
    
    
    def parseFeed(self, string):
         nextThreadPos = 0
        
         #output file
         self.outputFile = open('.\output.txt', 'w')
    
         #print string
         self.theFeed = string        
         nextHeaderPosition = self.findNextUserHeaderMatch(0)
         while nextHeaderPosition != -1:
             if self.checkUserForMatch(self.currentUser):
                 self.targetUserFoundInThread = True
             self.checkForUserChange()
             self.lastUserFound = self.currentUser
            
             nextReadPostion = self.findNextParagraph(nextHeaderPosition)
             if nextReadPostion == -1:
                 print("next read break")
                 break    
            
             
             if nextReadPostion > nextThreadPos:                
                 #write out the IO sequence if the user was found
                 if self.targetUserFoundInThread:
                     self.writeParagraphsToFile()
                 nextThreadPos = self.findNextThread(nextReadPostion)
                 if nextThreadPos == -1: break                    
            
             nextHeaderPosition = self.findNextUserHeaderMatch(nextReadPostion)
         print("next header break")
         self.outputFile.close()
    
    def findNextThread(self, pos):
        # reset user found flag
        self.targetUserFoundInThread = False 
        self.collatedParagraphs = []
        
        # next thread position
        return self.theFeed.find(self.divClassThread, pos)         
    
    def findNextUserHeaderMatch(self, position):
        #print "Header pos: "
        startPos = self.theFeed.find(self.spanClassUser, position)
        endPos = self.theFeed.find(self.spanClassCloseTag, position)
        if (startPos != -1) and (endPos != -1):
            self.currentUser  = self.theFeed[startPos + len(self.spanClassUser):endPos]
        #print(self.currentUser)
        
        return endPos
        
    def findNextParagraph(self, position):
        startPosition = self.theFeed.find(self.paragraphTag, position)
        endPostition = self.theFeed.find(self.paragraphCloseTag, position)
        startPosition = startPosition + 3
        #print("Start position: ", startPosition)
        #print("End position: ", endPostition)
        #print(self.theFeed[startPosition:endPostition])
        self.collatedParagraphs.append((self.currentUser, self.theFeed[startPosition:endPostition] + '\n'))
         
        return endPostition
    
    def checkUserForMatch(self, userUnderTest):
        if userUnderTest == self.userHeader:
            return True
        elif userUnderTest == self.userID:
            return True
        else:
            return False
 
    def checkForUserChange(self):
        if self.currentUser != self.lastUserFound:
            #self.outputIOChange()
            return True
        else:
            return False
                
    def outputIOChange(self, user):
        if self.checkUserForMatch(user):
            #print("output:")
            #self.collatedParagraphs.append( 'Output:')
            self.outputFile.write( 'Output:')
        else:
            #print("input:")
            #self.collatedParagraphs.append('Input:')
            self.outputFile.write( 'Input:')
            
    def writeParagraphsToFile(self):         
        self.outputFile.write('---Thread---\n')
        lastUser = ""
        for line in reversed(self.collatedParagraphs):
            print(line)
            user = line[0]
            if user != lastUser:
                self.outputIOChange(line[0])
            lastUser = user
            self.outputFile.write(line[1])
        self.outputFile.write('\n')

# <codecell>        
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="fb username")
parser.add_argument("-i", "--idNumber", help="fb id number")
parser.add_argument("-a", "--archivePath", help="fb archivepath")
args = parser.parse_args()

# <codecell>        
h = HTMLParser.HTMLParser()
if args.name and args.idNumber:
    myParser = FacebookMessageParser(args.name, args.idNumber)

# <codecell>        

if args.archivePath:
    f = open(args.archivePath + "\\html\\messages.htm", 'r')

messagesHTMString = f.read()
soup = BeautifulSoup.BeautifulSoup(messagesHTMString, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
#print(soup)



myParser.parseFeed(str(soup));