#!/usr/bin/env python
from xmltodict import parse, unparse
import glob
import csv
import logging

perfectAndStemList = []

fileList = glob.glob("XML/*.xml")

def generatePerfectAndStemCSV():
    for path in fileList:
        xml = open(path, "r")
        org_xml = xml.read()
        d = parse(org_xml, force_list={'lod:MS-TYPE-VRB': True})
        try:
            if d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:MICROSTRUCTURE']['lod:MS-TYPE-VRB'][0]:
                stem = d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:ITEM-ADRESSE']['#text']
                perfect = d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:MICROSTRUCTURE']['lod:MS-TYPE-VRB'][0]['lod:PARTICIPE-PASSE']
                if not isinstance(perfect, str):
                    for onePerfect in perfect:
                        perfectAndStemList.append([onePerfect, stem])
                else:
                    perfectAndStemList.append([perfect, stem])
        except KeyError:
            pass
    if perfectAndStemList:
        with open('perfectAndStem.csv', 'w') as myfile:
            writer = csv.writer(myfile)
            writer.writerows(perfectAndStemList)

if __name__ == "__main__":
    generatePerfectAndStemCSV()
