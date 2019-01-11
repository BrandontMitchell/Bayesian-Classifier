#
# Final.py
#
# TextModel project!
#
# Name(s): Danny Porras, Nico Manucci, Brandon Mitchell
#
from porter import create_stem
from prettytable import PrettyTable
import math


class TextModel():
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        #
        # Create another of your own
        #
        self.punctuation = {}     # For counting punctuation
    
    def __repr__(self):
        """Display the contents of a TextModel."""
        s = 'Words:\n' + str(self.words) + '\n\n'
        s += 'Word lengths:\n' + str(self.wordlengths) + '\n\n'
        s += 'Stems:\n' + str(self.stems) + '\n\n'
        s += 'Sentence lengths:\n' + str(self.sentencelengths) + '\n\n'
        s += 'Punctuation:\n' + str(self.punctuation)
        return s

    # Include other functions here.
    # In particular, you'll need functions that add to the model.

    def readTextFromFile(self, filename):
        """ Accepts a filename (a string) and set self.text to all the text in that file, represented as a single large string
        """
        f = open(filename, encoding = 'utf-8')
        text = f.read()
        f.close()
        return text



    def makeSentenceLengths(self, text):
        """ Use the text in self.text to create the self.sentencelengths dictionary
        """
        self.sentencelengths = {}
        text = text.split()
        slength = 0

        for word in text:
            slength += 1
            if word[-1] == '.' or word[-1] == '?' or word[-1] == '!':
                if slength not in self.sentencelengths:
                    self.sentencelengths[slength] = 0

                self.sentencelengths[slength] += 1
                slength = 0
            

    def cleanString(self, s):
        """ Should accept a string s and return a string with no punctuation
            and no upper-case letters
        """
        s = s.lower()
        new = ''

        for i in range(len(s)):
            if s[i] == '.' or s[i] == '?' or s[i] == '!':
                i + 1
            else: 
                new += s[i]

        return new

    def makeWordLengths(self, s):
        """ Similar to makesetencelengths, except that it makes a dictionary of the 
            word length features
        """
        s = self.cleanString(s)
        self.wordengths = {}
        length = 0

        for word in s:
            length += 1

            if word == ' ':
                if length not in self.wordlengths:
                    self.wordlengths[length] = 0
                self.wordlengths[length] += 1
                length = 0


    def makeWords(self, s):
        """ similar to makesentencelengths, except that it makes a dictionary of words themselves (cleaned)
            so we should use the cleaned string for this one
        """
        s = self.cleanString(s)
        s = s.split()
        self.words = {}

        for word in s:
            if word not in self.words:
                self.words[word] = 0
            self.words[word] += 1

        

    def makeStems(self, s):
        """ similar to makewords, except that it makes a dictionary of the stems of the 
            words themselves (cleaned), so we should used cleaned string for this one
        """
        s = self.cleanString(s)
        s = s.split()
        self.stems = {}

        for word in s:
            word = create_stem(word)
        
        for word in s:
            if word not in self.stems:
                self.stems[word] = 0
            self.stems[word] += 1
        

    def makePunctuation(self, s):
        """ similar to makewords, but we chose the feature
        """
        s = s.lower()
        self.punctuation = {}

        for word in s:
            if word in '?.,!-_':
                if word not in self.punctuation:
                    self.punctuation[word] = 0
                self.punctuation[word] += 1
    

#--------------------------TESTS-----------------------------#

# put the text between these triple-quotes into a file named text.txt
# test_text = """This is a small sentence. This isn't a small sentence,
# because this sentence contains more than 10 words and a number! This
# isn't a question, is it?"""

# TM = TextModel()
# text = TM.readTextFromFile("test.txt")

# TM.makeSentenceLengths(text)
# TM.makeWordLengths(text)
# TM.makeWords(text)
# TM.makeStems(text)
# TM.makePunctuation(text)

# Let's see all the dictionaries!
# print("The text model has these dictionaries: ")
# print(TM)


#-------------------------------------------------------------#


    def normalizeDictionary(self, d):
        """ accept any single one of the model dictionaries d and return a 
            normalized version in which values add to 1.0
        """
        keys = {}

        for k in d:
            keys[k] = d[k] / sum(d.values())
        return keys
    
    def smallestValue(self, nd1, nd2):
        """ This method should accept any two model dictionaries nd1 and nd2 and should return the
            smallest positive (non-zero) value across both
        """
        value1 = min(nd1.values())
        value2 = min(nd2.values())

        if value1 < value2:
            return value1
        else:
            return value2


    def compareDictionaries(self, d, nd1, nd2):
        """ Should compute the log-probability that the dictionary d arose from the distribution of data
            in the normalized dictionary nd1 and the log-probability that dictionary d arose from the 
            distribution of data in normalized dictionary nd2
        """
        e = 0.5 * self.smallestValue(nd1, nd2)
        logProb1 = 0.0
        logProb2 = 0.0

        for k in d:
            if k in nd1:
                logProb1 += math.log(nd1[k]) * d[k]
            elif k not in nd1:
                logProb1 += math.log(e)

            
        for k in d:
            if k in nd2:
                logProb2 += math.log(nd2[k]) * d[k]
            elif k not in nd2:
                logProb2 += math.log(e)

        return [logProb1, logProb2]

            
    def createAllDictionaries(self, s):
        """ helps create all dictionaries with the raw input string self.text
        """

        cleanS = self.cleanString(s)
        self.makeSentenceLengths(s)
        self.makeWords(cleanS)
        self.makeStems(cleanS)
        self.makePunctuation(s)
        self.makeWordLengths(cleanS)

    def compareTextWithTwoModels(self, model1, model2):
        """ run the compareDictionaries and for each feature dictionaries in 
            newmodel against the correspond (normalized) dictionaries in model1
            and model2
        """

        model1Win = 0
        model2Win = 0

        words1 = self.normalizeDictionary(model1.words)
        words2 = self.normalizeDictionary(model2.words)
        c1 = self.compareDictionaries(self.words, words1, words2)

        sentence1 = self.normalizeDictionary(model1.sentencelengths)
        sentence2 = self.normalizeDictionary(model2.sentencelengths)
        c2 = self.compareDictionaries(self.sentencelengths, sentence1, sentence2)

        wordL1 = self.normalizeDictionary(model1.wordlengths)
        wordL2 = self.normalizeDictionary(model2.wordlengths)
        c3 = self.compareDictionaries(self.wordlengths, wordL1, wordL2)

        punc1 = self.normalizeDictionary(model1.punctuation)
        punc2 = self.normalizeDictionary(model2.punctuation)
        c4 = self.compareDictionaries(self.punctuation, punc1, punc2)

        stem1 = self.normalizeDictionary(model1.stems)
        stem2 = self.normalizeDictionary(model2.stems)
        c5 = self.compareDictionaries(self.stems, stem1, stem2)

        if c1[0] > c1[1]:
            model1Win += 1
        else:
            model2Win += 1
        
        if c2[0] > c2[1]:
            model1Win += 1
        else:
            model2Win += 1
        
        if c3[0] > c3[1]:
            model1Win += 1
        else:
            model2Win += 1
        
        if c4[0] > c4[1]:
            model1Win += 1
        else:
            model2Win += 1
        
        if c5[0] > c5[1]:
            model1Win += 1
        else:
            model2Win += 1

# -------- FORMATTING ------- #  

        x = PrettyTable()

        x.field_names = ["Name", "vs TM1", "vs TM2"]
        x.add_row(["----", "----", "----"])
        x.add_row(["Words", c1[0], c1[1]])
        x.add_row(["Word Length", c3[0], c3[1]])
        x.add_row(["Sentence Length", c2[0], c2[1]])
        x.add_row(["Stems", c4[0], c4[1]])
        x.add_row(["Punctuation", c5[0], c5[1]])
        print(x)

# -------- FORMATTING ------- #

        print("Model 1 wins on ", model1Win, " features!")
        print("Model 2 wins on ", model2Win, " features!")

        if model1Win > model2Win:
            print("+++++++ Model 1 is the better match +++++++")

        else: 
            print("+++++++ Model 2 is the better match +++++++")


print('\n', " +++++++++++ Model1 +++++++++++ ")
TM1 = TextModel()
text1 = TM1.readTextFromFile("kanye.txt")
TM1.createAllDictionaries(text1)  # provided in hw description
print(TM1)

print('\n', " +++++++++++ Model1 +++++++++++ ")
TM2 = TextModel()
text2 = TM2.readTextFromFile("frost.txt")
TM2.createAllDictionaries(text2)  # provided in hw description
print(TM2)


print('\n', " +++++++++++ #1 Unknown text +++++++++++ ")
TM_Unk = TextModel()
textUK = TM_Unk.readTextFromFile("unknown.txt")
TM_Unk.createAllDictionaries(textUK)  # provided in hw description
print(TM_Unk)


# print('\n', " +++++++++++ #2 Unknown text +++++++++++ ")
# TM_Unk = TextModel()
# textUK = TM_Unk.readTextFromFile("unknown2.txt")
# TM_Unk.createAllDictionaries(textUK)  # provided in hw description
# print(TM_Unk)

TM_Unk.compareTextWithTwoModels(TM1, TM2)


##### OUR RESULTS ###

""" We decided to test two different artists: one a lyricist and rapper, Kanye West, and one poet, Robert Frost, compared with two random unknown text files.
    Our first unknown text file contains a made-up paragraph with no specific reference to either artist. From this, we got a near even result, however this 
    text file seemed more similar to how kanye west writes. We see a significant difference here mostly in the stems per source, where kanye was more related here in that sense
    partially due to the fact that we used some abbreviated words. Our second text file consisted of text from each author, with more of text from Robert Frost than from Kanye West
    and this proved our program to be accurate. It came to a 4-1 decision with Frost being the more related text. We decided the winner based on which artist the text more 
    corresponded with by comparing each individual factor (dictionary) with our artists'. We expected the second text to give us these results, however the first text could have
    gone either way and would've been accepted by us. A very fun project, and helped us better understand how to use and manipulate dictionaries, as well as a good practice in 
    object oriented programming with classes and methods. 

"""