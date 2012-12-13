#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, plistlib
import shelve

RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                 u'|' + \
                 u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                  (unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff),
                   unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff),
                   unichr(0xd800), unichr(0xdbff), unichr(0xdc00), unichr(0xdfff))

RE_XML_ILLEGAL = re.compile(RE_XML_ILLEGAL)

REPLACES = {
    '': " ", #Este caracter es usado en el autocompletado pongo un espacio
    '': "*", #Conitnue bullet del bundle text
    '': "-"     #El backspace en una macro de latex
}

_cache = shelve.open('/tmp/cache.shelve')

def cached(f):
    def wrapped(path):
        if not path in _cache:
            _cache[path] = f(path)
        return _cache[path]
    return wrapped

@cached
def readPlist(filePath):
    print "Called with", filePath
    try:
        data = plistlib.readPlist(filePath)
    except Exception, e:
        data = open(filePath).read()
        for match in RE_XML_ILLEGAL.finditer(data):
            char = data[match.start():match.end()]
            if char in REPLACES:
                char = REPLACES[char]
            data = data[:match.start()] + char + data[match.end():]
        data = plistlib.readPlistFromString(data)
    return data

def writePlist(dictionary, filePath):
    plistlib.writePlist(dictionary, filePath)
