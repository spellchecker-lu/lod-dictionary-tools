#!/usr/bin/env python
from lxml import etree
import glob
import csv

fileList = sorted(glob.glob("lod-dictionary-mirror/XML/*"))
csvFile = open('lod-dictionary-mirror/index.csv', 'w')
csvWriter = csv.writer(csvFile)

def generateLemmaList():
    for filename in fileList:
        tree = etree.parse(filename)
        id = tree.xpath('//LOD:META', namespaces={'LOD': 'http://www.lod.lu/'})[0].get('{http://www.lod.lu/}ID')
        word = tree.xpath('//LOD:ITEM-ADRESSE', namespaces={'LOD': 'http://www.lod.lu/'})[0]
        print (id, word.text)
        csvWriter.writerow([id, word.text])

if __name__ == "__main__":
    generateLemmaList()
