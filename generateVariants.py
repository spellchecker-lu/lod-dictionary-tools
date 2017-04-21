#!/usr/bin/env python
from xmltodict import parse, unparse
import glob
import csv
import logging

variantList = []

xmlpath = 'lod-dictionary-mirror/XML/'

fileList = glob.glob(xmlpath+"*.xml")

def generateVariantsCSV():
    for path in fileList:
        d = parse(open(path, "r").read(), force_list={
            'lod:MS-TYPE-ADJ': True,
            'lod:MS-TYPE-ADV': True,
            'lod:MS-TYPE-CONJ': True,
            'lod:MS-TYPE-PART': True,
            'lod:MS-TYPE-PREP': True,
            'lod:MS-TYPE-PREP-plus-ART': True,
            'lod:MS-TYPE-PRON': True,
            'lod:MS-TYPE-SUBST': True,
            'lod:MS-TYPE-VRB': True
            })
        nodetype = list(d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:MICROSTRUCTURE'].items())[0][0]
        for node_list in d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:MICROSTRUCTURE'][nodetype]:
            for idx, node in enumerate(node_list):
                try:
                    if (node.startswith('lod:RENVOI-')
                    and 'lod:VARIANTE-ORTHOGRAPHIQUE'
                    in d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:MICROSTRUCTURE'][nodetype][0][node].keys()
                    ):
                        stem = d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:ITEM-ADRESSE']['#text']
                        target = d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:MICROSTRUCTURE'][nodetype][0][node]['@lod:REF-ID-ITEM-ADRESSE'][:-3]
                        td = parse(open(xmlpath+target+".xml", "r").read())
                        tstem = td['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:ITEM-ADRESSE']['#text']
                        variantList.append([stem, tstem])
                except NameError:
                    print(nodetype)
                    print(d['lod:LOD']['lod:ITEM']['lod:ARTICLE']['lod:ITEM-ADRESSE']['#text'])

    if variantList:
        with open('variants.csv', 'w') as myfile:
            writer = csv.writer(myfile)
            writer.writerows(variantList)
    else:
        print("No variants, you done goofed up")

if __name__ == "__main__":
    generateVariantsCSV()
