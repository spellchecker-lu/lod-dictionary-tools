#!/usr/bin/env python

import xml.etree.ElementTree as ET
import os
import re
import base64

xmlDirectory = 'lod-dictionary-mirror/XML'
audioDirectory = 'lod-audio-mirror/MP3'

if not os.path.exists(xmlDirectory):
    os.makedirs(xmlDirectory)

if not os.path.exists(audioDirectory):
    os.makedirs(audioDirectory)

ns = {'lod': 'http://www.lod.lu/'}

ET.register_namespace('lod', 'http://www.lod.lu')

context = ET.iterparse('2017-04-13-lod-opendata.xml', events=('end',))
for event, elem in context:
    if elem.tag == '{http://www.lod.lu/}ITEM':
        print elem.find('lod:META', ns).attrib

        id = elem.find('lod:META', ns).attrib['{http://www.lod.lu/}ID']

        xmlFilename = xmlDirectory + '/' + format(id + ".xml")
        audioFilename = audioDirectory + '/' + format(id + ".mp3")

        content = ET.tostring(elem)

        # Extract the audio data, decode it and write it to a file
        audio_tag = elem.find('lod:AUDIO', ns)
        if audio_tag is not None:
            audio_content = audio_tag.text
            if audio_content:
                audio_data = base64.b64decode(audio_content)
                with open(audioFilename, 'wb') as f_mp3:
                    f_mp3.write(audio_data)

        # Replace the "ns" namespace with the original name
        # FIXME: Find a better way to do that namespaces
        content = content.replace("ns0:", "lod:")
        content = content.replace(' xmlns:ns0="http://www.lod.lu/"', "")

        # Remove the "VERSIOUN" attribute to prevent unnecessary commits with future updates
        content = re.sub(r' lod:VERSIOUN="[^"]+"', '', content)

        # Remove the audio data
        content = re.sub(r'<lod:AUDIO.+</lod:AUDIO>\n', '', content, 0, re.DOTALL)

        with open(xmlFilename, 'wb') as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write("<lod:LOD xmlns:lod=\"http://www.lod.lu/\">\n")
            f.write(content.strip())
            f.write("\n</lod:LOD>")
