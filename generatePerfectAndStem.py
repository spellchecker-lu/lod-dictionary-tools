#!/usr/bin/env python

import xml.etree.ElementTree as etree
import glob
import csv

etree.register_namespace('lod', 'http://www.lod.lu')

perfectAndStemList = []

fileList = glob.glob("lod-dictionary-mirror/XML/*.xml")

def generatePerfectAndStemCSV():
    for file in fileList:
        tree = etree.parse(file)
        root = tree.getroot()
        for child in root:
            verbOrNot = child[1][1][0][0].tag
            if verbOrNot == "{http://www.lod.lu/}CAT-GRAM-VRB":
                stem = child[1][0].text
                perfect = child[1][1][0][2].text
                if len(perfect.strip()) > 0:
                    perfectAndStemList.append([perfect, stem])

    if perfectAndStemList :
        with open('perfectAndStem.csv', 'w') as myfile:
            writer = csv.writer(myfile)
            writer.writerows(perfectAndStemList)

if __name__ == "__main__":
    generatePerfectAndStemCSV()
