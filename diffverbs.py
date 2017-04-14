#!/usr/bin/env python

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

with open('lod-verbs.txt') as f:
    lod = f.read().splitlines()

with open('spellchecker-verbs.txt') as f:
    spellchecker = f.read().splitlines()

print('\n'.join(diff(lod, spellchecker)))
