#!/usr/bin/env python
from xmltodict import parse, unparse
import glob
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
fileList = glob.glob("lod-dictionary-mirror/XML/*.xml")


for path in fileList:
    xml = open(path, "r")
    org_xml = xml.read()
    d = parse(org_xml)
    try:
        if d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:MICROSTRUCTURE']['lod:MS-TYPE-VRB']:
            print(d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:ITEM-ADRESSE']['#text'])
    except KeyError:
        log.debug('not a verb')
