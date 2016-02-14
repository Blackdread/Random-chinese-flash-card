#!/usr/bin/python
# -*- coding: utf-8 -*-

# Written by Yoann CAPLAIN
# 2016-01-01

import re
import os
import sys, traceback
import csv, codecs, cStringIO
import random
import pickle

# http://stackoverflow.com/questions/2688020/how-to-print-chinese-word-in-my-code-using-python

documentToSave = "/Users/yoann/Documents/Script Geektool/random.pickle"
documentToSaveFairRandom = "/Users/yoann/Documents/Script Geektool/randomDict.pickle"

useFairRandom = True

# Choose from level 1 to 6
hskFile = '/Users/yoann/Documents/UTBM/Semestre 5/A1_Data_Science/chineseCSV/HSK_Level_4.csv'


pinyinToneMarks = {
    u'a': u'āáǎà', u'e': u'ēéěè', u'i': u'īíǐì',
    u'o': u'ōóǒò', u'u': u'ūúǔù', u'ü': u'ǖǘǚǜ',
    u'A': u'ĀÁǍÀ', u'E': u'ĒÉĚÈ', u'I': u'ĪÍǏÌ',
    u'O': u'ŌÓǑÒ', u'U': u'ŪÚǓÙ', u'Ü': u'ǕǗǙǛ'
}

def convertPinyinCallback(m):
    tone=int(m.group(3))%5
    r=m.group(1).replace(u'v', u'ü').replace(u'V', u'Ü')
    # for multple vowels, use first one if it is a/e/o, otherwise use second one
    pos=0
    if len(r)>1 and not r[0] in 'aeoAEO':
        pos=1
    if tone != 0:
        r=r[0:pos]+pinyinToneMarks[r[pos]][tone-1]+r[pos+1:]
    return r+m.group(2)

def convertPinyin(s):
    return re.sub(ur'([aeiouüvÜ]{1,3})(n?g?r?)([012345])', convertPinyinCallback, s, flags=re.IGNORECASE)

def makeRandom():
	TOO_MUCH_ENTRIES = 1
	global randLine
	with open(hskFile, 'rb') as csvfile:
	
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

		numberOfLine = sum(1 for row in spamreader)

		# print numberOfLine

		if not useFairRandom:
			randLine = random.randint(1, numberOfLine - 1 - TOO_MUCH_ENTRIES) # For no reason, i get more entries than real
		else:
			dictFairRand = getRandomDict()
			if len(dictFairRand) >= numberOfLine - 1 - TOO_MUCH_ENTRIES:
			# ===================== Version 1 ===========================
			# I do not really like, not really random
			# 	minValue = 999999999
			# 	minKey = 0
			# 	for row in dictFairRand:
			# 		if dictFairRand[row] < minValue:
			# 			minKey = row
			# 			minValue = dictFairRand[row]
			# 	randLine = minKey
			# ===========================================================

			# ===================== Version 2 ===========================
				resetRandomUsed()
				randLine = random.randint(1, numberOfLine - 1 - TOO_MUCH_ENTRIES)
			# ===========================================================
			else:
				while(True):
					randLine = random.randint(1, numberOfLine - 1 - TOO_MUCH_ENTRIES)

					# Possible also to allow some multiple occurences by doing:
					if len(dictFairRand) > 10 and random.randint(0, 100) < 40:
						while (True):
							randLine = random.randint(1, numberOfLine - 1 - TOO_MUCH_ENTRIES)
							if randLine in dictFairRand:
								break
						break

					# Should maybe do like the other one because every time, randLine is in dictFairRand we loop again and we give one more chance for
					# an old occurence to appear again
					if randLine not in dictFairRand:
						# print "found",randLine," et ",len(dictFairRand)
						break

		fileDbPickle = open(documentToSave, "w+")
		pickle.dump(randLine, fileDbPickle)
		fileDbPickle.close()

def resetRandomUsed():
	dictFairRand = {}
	fileDbPickle = open(documentToSaveFairRandom, "w+")
	pickle.dump(dictFairRand, fileDbPickle)
	fileDbPickle.close()


def saveRandomUsed(numberUsed):
	# key is numberUsed, value is number of time used
	# Get old data
	dictFairRand = getRandomDict()

	if numberUsed not in dictFairRand:
		dictFairRand[numberUsed] = 1
	else:
		dictFairRand[numberUsed] += 1

	fileDbPickle = open(documentToSaveFairRandom, "w+")
	pickle.dump(dictFairRand, fileDbPickle)
	fileDbPickle.close()

def getRandomDict():
	try:
		fileDbPickle = open(documentToSaveFairRandom, "r")
		dictFairRand = pickle.load(fileDbPickle)
	except:
		dictFairRand = {}
		fileDbPickle = open(documentToSaveFairRandom, "w+")
		pickle.dump(dictFairRand, fileDbPickle)
		fileDbPickle.close()

	return dictFairRand

def loadRand():
	global randLine
	try:
		fileDbPickle = open(documentToSave, "r")
		randLine = pickle.load(fileDbPickle)
		fileDbPickle.close()
	except IOError, Argument:
		print "Error loading pickle"

random.seed()

UTF8Writer = codecs.getwriter('utf-8')
sys.stdout = UTF8Writer(sys.stdout)

randLine = 0
showOnlyChinese = False
ShowProAndDef = False

# I did that because I use Geektool to show the data, I decided to create two "geeklet", one that refresh and only show Chinese (so I have a different font size -> bigger) 
# another one the pinyin and the translation (smaller font size)
# It's also possible instead of saving the random number, to save chinese, pinyin and translation
if len(sys.argv) == 2:
	if "rand" in sys.argv[1]:
		makeRandom()
		saveRandomUsed(randLine)
		sys.exit()
	else:
		loadRand()
	if "chinese" in sys.argv[1]:
		showOnlyChinese = True
	if "proDef" in sys.argv[1]:
		ShowProAndDef = True
else:
	# Default behavior without any parameters
	# new word is selected and eveything is displayed
	makeRandom()

saveRandomUsed(randLine)

with open(hskFile, 'rb') as csvfile:
	spamreader2 = csv.DictReader(csvfile)
	for row in spamreader2:
		if spamreader2.line_num == randLine:
			chinese = row['Word'].decode('utf-8')
			# pro = row['Pronunciation'].decode('utf-8') # normal with numbers

			accents = "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜĀÁǍÀĒÉĚÈĪÍǏÌŌÓǑÒŪÚǓÙǕǗǙǛ"
			if any((c in accents) for c in row['Pronunciation']):
				# Means the pinyin is already written with accents
				pro = row['Pronunciation'].decode('utf-8') # normal with numbers
			else:
				pro = convertPinyin(row['Pronunciation'])
			# defi = row['Definition'].decode('utf-8')
			defi = convertPinyin(row['Definition'].decode('utf-8'))
			if showOnlyChinese:
				print chinese
			elif ShowProAndDef:
				print pro
				print defi
			else:
				print chinese
				print pro
				print defi
			break
