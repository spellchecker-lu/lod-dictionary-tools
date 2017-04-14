#!/usr/bin/env python

"""
Checks data.public.lu for new version of LOD dump.

If there is a new version:
 - Download it to data/
 - Parse it and split it into files
"""

import base64
import logging
import os
import requests
import tarfile
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO)

# Where to save our data
LOD_PATHS = {
    'data': 'data/',
    'xml': 'lod-dictionary-mirror/XML',
    'audio': 'lod-audio-mirror/MP3'
}


def lod_init():
    """
    Central place for janitorial tasks
    """
    # Make sure our directories exist
    for path in LOD_PATHS.values():
        if not os.path.exists(path):
            os.makedirs(path)


def lod_get():
    """
    Downloads lod data if there is a new version.
    Calls the lod_split if a new version is downloaded.
    """
    # The API endpoint that contains the link to the most recent version of the
    # addresses in all available formats (geojson, but also shp).
    udata_lod = 'https://data.public.lu/api/1/datasets/letzebuerger-online-dictionnaire-raw-data/'

    # Eugh, magic numbers.
    # This is just the uuid for the addresses in csv format.
    udata_lod_id = 'aa81fad1-1163-443f-9ed1-1270132812ad'

    # Udata has no permalink. Parse the API to get the latest geojson.
    udata_json = requests.get(udata_lod).json()

    # Find the resource with that ID in the udata json
    # i.e. our addresses
    for resource in udata_json['resources']:
        if resource['id'] == udata_lod_id:
            lod_targz = resource['url']
            lod_title = resource['title']
            break
    else:
        # Oops, the for loop didn't find anything!
        raise IOError("Could not find resource id {} in {}".format(
            udata_lod_id, udata_lod
        ))

    try:
        with open('lod-latest', 'r+') as status:
            lateststatus = str(status.readline())
    except FileNotFoundError:
        lateststatus = ''

    logging.info('Latest status: ' + lateststatus)
    logging.info('Got file name: ' + lod_title)

    if str(lateststatus) == str(lod_title):
        logging.info('We already have the latest data. Ciao!')
        return  # exit the function
    else:
        with open('lod-latest', 'w') as status:
            status.write(lod_title)
            logging.info('Downloading latest version: ' + lod_title)

    # Downloading the addresses might take a few minutes.
    # In the meanwile, shake your wrists and correct your posture.

    with open(LOD_PATHS['data'] + lod_title, 'wb+') as handle_tar:
        r = requests.get(lod_targz, stream=True)

        if not r.ok:
            logging.error('Something went wrong, time to write debug code')

        for block in r.iter_content(chunk_size=8192):
            handle_tar.write(block)
    with open(LOD_PATHS['data'] + lod_title, 'rb+') as handle_tar:
        # Open tarfile
        tar = tarfile.open(fileobj=handle_tar, mode="r")

        for member in tar.getmembers():
            if member.name.endswith('-lod-opendata.xml'):
                # Safety check for .. or / in path
                if os.path.abspath(
                    os.path.join(
                        LOD_PATHS['data'],
                        member.name)).startswith(
                    os.path.abspath(
                        LOD_PATHS['data'])):
                    tar.extractall(path=LOD_PATHS['data'], members=[member])
                    logging.info('Yay, extracted ' + member.name)
                    lod_split(LOD_PATHS['data'] + member.name)
                else:
                    logging.error('Unsafe filename found in LOD dump!')
            else:
                logging.info('Not extracting ' + member.name)


def lod_split(path):
    """
    Parses and splits a gigantic lod xml file.
    Argument is the path to the file.
    Output is separate xml and mp3 files.
    """
    context = ET.iterparse(path, events=('end',))
    ET.register_namespace('lod', 'http://www.lod.lu/')

    for event, elem in context:
        if elem.tag == '{http://www.lod.lu/}ITEM':
            meta = elem.find('{http://www.lod.lu/}META')
            lodid = meta.attrib['{http://www.lod.lu/}ID']
            logging.info(lodid)

            # Remove the "VERSIOUN" attribute to prevent unnecessary future commits
            # None is to not raise an exception if VERSIOUN does not exist
            meta.attrib.pop('{http://www.lod.lu/}VERSIOUN', None)

            xml_filename = LOD_PATHS['xml'] + '/' + lodid + ".xml"
            audio_filename = LOD_PATHS['audio'] + '/' + lodid + ".mp3"

            # Extract the audio data
            audio_tag = elem.find('{http://www.lod.lu/}AUDIO')

            try:
                # decode it and write it to a file
                audio_data = base64.b64decode(audio_tag.text)
                with open(audio_filename, 'wb') as f_mp3:
                    f_mp3.write(audio_data)
                # Prune audio from the tree
                elem.remove(audio_tag)
            except AttributeError:
                logging.info('No audio for ' + lodid)

            with open(xml_filename, 'wb') as f_xml:
                # We need .encode() on strings because wb writes in bytes because
                # ET.tostring returns bytes.
                f_xml.write(
                    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n".encode())
                f_xml.write(
                    "<lod:LOD xmlns:lod=\"http://www.lod.lu/\">\n".encode())
                f_xml.write(ET.tostring(elem, encoding="UTF-8").strip())
                f_xml.write("\n</lod:LOD>".encode())


if __name__ == "__main__":
    lod_init()
    lod_get()