#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Preferences's module
    http://manual.macromates.com/en/preferences_items.html
    
    completions, an array of additional candidates when cycling through completion candidates from the current document.
    completionCommand, a shell command (string) which should return a list of candidates to complete the current word (obtained via the TM_CURRENT_WORD variable).
    disableDefaultCompletion, set to 1 if you want to exclude matches from the current document when asking for completion candidates (useful when you provide your own completion command).

    decreaseIndentPattern, regular expression.
    increaseIndentPattern, regular expression.
    indentNextLinePattern, regular expression.
    unIndentedLinePattern, regular expression.

    showInSymbolList, set to 1 to include in the symbol list.
    symbolTransformation, 

    highlightPairs, an array of arrays, each containing a pair of characters where, when the caret moves over the second, the first one will be highlighted for a short moment, if found.
    smartTypingPairs, an array of arrays, each containing a pair of characters where when the first is typed, the second will be inserted. An example is shown below. For more information see auto-paired characters.

    shellVariables, an array of key/value pairs. See context dependent variables.
    spellChecking, set to 0/1 to disable/enable spell checking.
'''
from copy import copy
import uuid as uuidmodule

from prymatex.support.bundle import PMXBundleItem
from prymatex.support.utils import compileRegexp
from prymatex.support.snippet import PMXSnippet
from prymatex.support.processor import PMXDebugSnippetProcessor

DEFAULT_SETTINGS = { 
    'showInSymbolList': False,
    'spellChecking': True,
    'completions': [],
    'shellVariables': {}
}
                      
class PMXPreferenceSettings(object):
    KEYS = [    'completions', 'completionCommand', 'disableDefaultCompletion', 'showInSymbolList', 'symbolTransformation', 
                'highlightPairs', 'smartTypingPairs', 'shellVariables', 'spellChecking',
                'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]
    INDENT_KEYS = [ 'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]
    COPY_KEYS = ['shellVariables', 'highlightPairs', 'smartTypingPairs', 'completions']
    INDENT_INCREASE = 0
    INDENT_DECREASE = 1
    INDENT_NEXTLINE = 2
    UNINDENT = 3
    def __init__(self, dataHash = {}):
        for key in self.KEYS:
            value = dataHash.get(key, None)
            if value != None:
                if key in [ 'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]:
                    value = compileRegexp( value )
                elif key in [ 'shellVariables' ]:
                    value = dict(map(lambda d: (d['name'], d['value']), value))
                elif key in [ 'symbolTransformation' ]:
                    value = map(lambda value: value.strip(), value.split(";"))
                elif key in [ 'showInSymbolList' ]:
                    value = bool(int(value))
                elif key in [ 'spellChecking' ]:
                    value = bool(int(value))
            setattr(self, key, value)
    
    @property
    def hash(self):
        dataHash = {}
        for key in PMXPreferenceSettings.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in [ 'decreaseIndentPattern', 'increaseIndentPattern', 'indentNextLinePattern', 'unIndentedLinePattern' ]:
                    value = value.pattern
                elif key in [ 'shellVariables' ]:
                    value = [ {'name': t[0], 'value': t[1] } for t in  value.iteritems() ]
                elif key in [ 'symbolTransformation' ]:
                    value = ";".join(value) + ";"
                elif key in [ 'showInSymbolList' ]:
                    value = value and "1" or "0"
                elif key in [ 'spellChecking' ]:
                    value = value and "1" or "0"
                dataHash[key] = value
        return dataHash
    
    def update(self, other):
        self._indentPatternsReady = any(map(lambda indent: getattr(self, indent) is not None, PMXPreferenceSettings.INDENT_KEYS))
        for key in PMXPreferenceSettings.KEYS:
            value = getattr(other, key, None)
            if value != None:
                if key in PMXPreferenceSettings.COPY_KEYS:
                    value = copy(value)

                isIndent = key in PMXPreferenceSettings.INDENT_KEYS
                currentValue = getattr(self, key)
                if (isIndent and not self._indentPatternsReady) or (not isIndent and currentValue is None):
                    setattr(self, key, value)
                elif key == "shellVariables" and isinstance(currentValue, dict) and isinstance(value, dict):
                    #Solo voy a hacer updates si no rompen lo que ya esta bien ganado por el score
                    if all(map(lambda newValue: newValue not in currentValue, value)):
                        currentValue.update(value)

    def combine(self, other):
        for key in PMXPreferenceSettings.KEYS:
            if key in [ 'decreaseIndentPattern', 'increaseIndentPattern', 
                        'indentNextLinePattern', 'unIndentedLinePattern' ]:
                continue
            value = getattr(other, key, None)
            if value is not None and getattr(self, key) is None:
                setattr(self, key, value)

    def indent(self, line):
        #IncreasePattern on return indent nextline
        #DecreasePattern evaluate line to decrease, no requiere del return
        #IncreaseOnlyNextLine on return indent nextline only
        #IgnoringLines evaluate line to unindent, no require el return
        indent = []
        if self.decreaseIndentPattern != None and self.decreaseIndentPattern.search(line):
            indent.append(self.INDENT_DECREASE)
        if self.increaseIndentPattern != None and self.increaseIndentPattern.search(line):
            indent.append(self.INDENT_INCREASE)
        if self.indentNextLinePattern != None and self.indentNextLinePattern.search(line):
            indent.append(self.INDENT_NEXTLINE)
        if self.unIndentedLinePattern != None and self.unIndentedLinePattern.search(line):
            indent.append(self.UNINDENT)
        return indent
    
    def compileSymbolTransformation(self):
        self.snippetsTransformation = []
        for symbol in self.symbolTransformation:
            symbol = "${SYMBOL" + symbol[1:] + "}"
            dataHash = {    'content': symbol, 
                            'name': symbol }
            snippet = PMXSnippet(uuidmodule.uuid1(), "internal", dataHash = dataHash)
            self.snippetsTransformation.append(snippet)
    
    def transformSymbol(self, text):
        #TODO: Hacer la transformacion de los simbolos
        return text
        if not hasattr(self, 'snippetsTransformation'):
            self.compileSymbolTransformation()
        pro = PMXDebugSnippetProcessor()
        for snippet in self.snippetsTransformation:
            snippet.execute(pro)
            text = pro.text
            if text:
                return text
        return text

DEFAULTS = PMXPreferenceSettings(DEFAULT_SETTINGS)
    
class PMXPreference(PMXBundleItem):
    KEYS = [ 'settings' ]
    TYPE = 'preference'
    FOLDER = 'Preferences'
    EXTENSION = 'tmPreferences'
    PATTERNS = ['*.tmPreferences', '*.plist']

    def load(self, dataHash):
        super(PMXPreference, self).load(dataHash)
        for key in PMXPreference.KEYS:
            if key == 'settings':
                setattr(self, key, PMXPreferenceSettings(dataHash.get(key, {})))
            else:
                setattr(self, key, dataHash.get(key, None))
    
    @property
    def hash(self):
        dataHash = super(PMXPreference, self).hash
        for key in PMXPreference.KEYS:
            value = self.settings.hash
            if value != None:
                dataHash[key] = value
        return dataHash

    @staticmethod
    def buildSettings(preferences):
        settings = PMXPreferenceSettings()
        if preferences:
            for p in preferences:
                settings.update(p.settings)
        settings.update(DEFAULTS)
        return settings