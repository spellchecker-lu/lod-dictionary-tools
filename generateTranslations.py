#!/usr/bin/env python
from os import walk
from lxml import etree
import json

f = []
for (dirpath, dirnames, filenames) in walk("XML/"):
    f.extend(filenames)
    break

translationResult = {}
for filename in filenames:
    tree = etree.parse("XML/"+filename)
    translationFile = {}
    translationDOM = {}
    i = 1
    for word in tree.xpath('//LOD:ITEM-ADRESSE', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationFile["word"] = word.text
    for deDOM in tree.xpath('//LOD:TRAD-ALL-DOMIN', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationDOM["de"] = deDOM.text
    for deDOM in tree.xpath('//LOD:TRAD-ALL-SUBORD', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationDOM["de"] = deDOM.text
    for frDOM in tree.xpath('//LOD:TRAD-FR-DOMIN', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationDOM["fr"] = frDOM.text
    for frDOM in tree.xpath('//LOD:TRAD-FR-SUBORD', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationDOM["fr"] = frDOM.text
    for enDOM in tree.xpath('//LOD:TRAD-EN-DOMIN', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationDOM["en"] = enDOM.text
    for enDOM in tree.xpath('//LOD:TRAD-EN-SUBORD', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationDOM["en"] = enDOM.text
    for ptDOM in tree.xpath('//LOD:TRAD-PO-DOMIN', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationDOM["pt"] = ptDOM.text
    for ptDOM in tree.xpath('//LOD:TRAD-PO-SUBORD', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationDOM["pt"] = ptDOM.text
    translationFile["DOM"] = translationDOM
    deTranslationRow = {}
    frTranslationRow = {}
    enTranslationRow = {}
    ptTranslationRow = {}
    translationByLanguage = {}
    for translationByMeaning in tree.xpath('//LOD:UNITE-DE-SENS', namespaces={'LOD': 'http://www.lod.lu/'}):
        deEQUIV = []
        deRS = []
        frEQUIV = []
        frRS = []
        enEQUIV = []
        enRS = []
        ptEQUIV = []
        ptRS = []
        for translation in translationByMeaning.xpath('LOD:EQUIV-TRAD-ALL', namespaces={'LOD': 'http://www.lod.lu/'}):
            for equiv in translation.xpath('LOD:ETA-EXPLICITE', namespaces={'LOD': 'http://www.lod.lu/'}):
                deEQUIV.append(equiv.text)
            for presente in translation.xpath('LOD:RS-ETA-PRESENTE', namespaces={'LOD': 'http://www.lod.lu/'}):
                deRS.append(presente.text)
            deTranslation = {}
            deTranslation["EQUIV"]=deEQUIV
            deTranslation["RS"]=deRS
            deTranslationRow[i]=deTranslation
        for translation in translationByMeaning.xpath('LOD:EQUIV-TRAD-FR', namespaces={'LOD': 'http://www.lod.lu/'}):
            for equiv in translation.xpath('LOD:ETF-EXPLICITE', namespaces={'LOD': 'http://www.lod.lu/'}):
                frEQUIV.append(equiv.text)
            for presente in translation.xpath('LOD:RS-ETF-PRESENTE', namespaces={'LOD': 'http://www.lod.lu/'}):
                frRS.append(presente.text)
            frTranslation = {}
            frTranslation["EQUIV"]=frEQUIV
            frTranslation["RS"]=frRS
            frTranslationRow[i]=frTranslation
        for translation in translationByMeaning.xpath('LOD:EQUIV-TRAD-EN', namespaces={'LOD': 'http://www.lod.lu/'}):
            for equiv in translation.xpath('LOD:ETE-EXPLICITE', namespaces={'LOD': 'http://www.lod.lu/'}):
                enEQUIV.append(equiv.text)
            for presente in translation.xpath('LOD:RS-ETE-PRESENTE', namespaces={'LOD': 'http://www.lod.lu/'}):
                enRS.append(presente.text)
            enTranslation = {}
            enTranslation["EQUIV"]=enEQUIV
            enTranslation["RS"]=enRS
            enTranslationRow[i]=enTranslation
        for translation in translationByMeaning.xpath('LOD:EQUIV-TRAD-PO', namespaces={'LOD': 'http://www.lod.lu/'}):
            for equiv in translation.xpath('LOD:ETP-EXPLICITE', namespaces={'LOD': 'http://www.lod.lu/'}):
                ptEQUIV.append(equiv.text)
            for presente in translation.xpath('LOD:RS-ETP-PRESENTE', namespaces={'LOD': 'http://www.lod.lu/'}):
                ptRS.append(presente.text)
            ptTranslation = {}
            ptTranslation["EQUIV"]=ptEQUIV
            ptTranslation["RS"]=ptRS
            ptTranslationRow[i]=ptTranslation
        translationByLanguage["de"] = deTranslationRow
        translationByLanguage["fr"] = frTranslationRow
        translationByLanguage["en"] = enTranslationRow
        translationByLanguage["pt"] = ptTranslationRow
        translationFile["OTHER"] = translationByLanguage
        i+=1
    for idOfFile in tree.xpath('//LOD:META', namespaces={'LOD': 'http://www.lod.lu/'}):
        translationResult[idOfFile.attrib["{http://www.lod.lu/}ID"]]=translationFile
print(json.dumps(translationResult, indent=1, sort_keys=True, ensure_ascii=False))
