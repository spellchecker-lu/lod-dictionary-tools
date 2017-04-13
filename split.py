#!/usr/bin/env python

import xml.etree.ElementTree as ET
import os
import re

xmlDirectory = 'lod-dictionary-mirror/XML'
csvDirectory = 'lod-dictionary-mirror/CSV'

if not os.path.exists(xmlDirectory):
    os.makedirs(xmlDirectory)

if not os.path.exists(csvDirectory):
    os.makedirs(csvDirectory)

ns = {'lod': 'http://www.lod.lu/'}

ET.register_namespace('lod', 'http://www.lod.lu')

context = ET.iterparse('2017-04-13-lod-opendata.xml', events=('end', ))
for event, elem in context:
    if elem.tag == '{http://www.lod.lu/}ITEM':
        print elem.find('lod:META', ns).attrib
        title = elem.find('lod:META', ns).attrib['{http://www.lod.lu/}ID']
        filename = xmlDirectory + '/' + format(title + ".xml")

        content = ET.tostring(elem)

        content = content.replace("ns0:", "lod:") #FIXME: Find a better way to keep namespaces
        content = content.replace(' xmlns:ns0="http://www.lod.lu/"', "")

        # Remove the "VERSIOUN" attribute to prevent unnecessary commits with future updates
        content = re.sub(r' lod:VERSIOUN="[^"]+"', '', content)

        # Remove the audio data
        content = re.sub(r'<lod:AUDIO.+</lod:AUDIO>\n', '', content, 0, re.DOTALL)

        with open(filename, 'wb') as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write("<lod:LOD xmlns:lod=\"http://www.lod.lu/\">\n")
            f.write(content.strip())
            f.write("\n</lod:LOD>")
