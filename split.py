#!/usr/bin/env python

import xml.etree.ElementTree as ET
import os
import base64
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LOD_PATHS['xml'] = 'lod-dictionary-mirror/XML'
LOD_PATHS['audio'] = 'lod-audio-mirror/MP3'

if not os.path.exists(LOD_PATHS['xml']):
    os.makedirs(LOD_PATHS['xml'])

if not os.path.exists(LOD_PATHS['audio']):
    os.makedirs(LOD_PATHS['audio'])

context = ET.iterparse('2017-04-13-lod-opendata.xml', events=('end',))

ET.register_namespace('lod', 'http://www.lod.lu/')

for event, elem in context:
    if elem.tag == '{http://www.lod.lu/}ITEM':
        meta = elem.find('{http://www.lod.lu/}META')
        lodid = meta.attrib['{http://www.lod.lu/}ID']
        logger.info(lodid)

        # Remove the "VERSIOUN" attribute to prevent unnecessary future commits
        # None is to not raise an exception if VERSIOUN does not exist
        meta.attrib.pop('{http://www.lod.lu/}VERSIOUN', None)

        xmlFilename = LOD_PATHS['xml'] + '/' + lodid + ".xml"
        audioFilename = LOD_PATHS['audio'] + '/' + lodid + ".mp3"

        # Extract the audio data
        audio_tag = elem.find('{http://www.lod.lu/}AUDIO')

        try:
            # decode it and write it to a file
            audio_data = base64.b64decode(audio_tag.text)
            with open(audioFilename, 'wb') as f_mp3:
                f_mp3.write(audio_data)
            # Prune audio from the tree
            elem.remove(audio_tag)
        except AttributeError:
            logger.info('No audio for '+lodid)

        with open(xmlFilename, 'wb') as f:
            f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            f.write("<lod:LOD xmlns:lod=\"http://www.lod.lu/\">\n")
            f.write(ET.tostring(elem).strip())
            f.write("\n</lod:LOD>")
