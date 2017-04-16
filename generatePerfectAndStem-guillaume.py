#!/usr/bin/env python
from xmltodict import parse
import glob
import csv
import logging

perfectAndStemList = []

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

fileList = glob.glob("lod-dictionary-mirror/XML/ARENNEN1.xml")


def generatePerfectAndStemCSV():
    for path in fileList:
        xml = open(path, "r")
        org_xml = xml.read()
        d = parse(org_xml, force_list={'lod:MICROSTRUCTURE': True})
        try:
            if d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:MICROSTRUCTURE'][0]['lod:MS-TYPE-VRB']:
                stem = d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:ITEM-ADRESSE']['#text']
                perfect = d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:MICROSTRUCTURE'][0]['lod:MS-TYPE-VRB']['lod:PARTICIPE-PASSE']
                print(stem)
                perfectAndStemList.append([perfect, stem])
        except KeyError:
            pass
    if perfectAndStemList:
        with open('perfectAndStem.csv', 'w') as myfile:
            writer = csv.writer(myfile)
            writer.writerows(perfectAndStemList)

if __name__ == "__main__":
    generatePerfectAndStemCSV()
