#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from prymatex.qt import QtGui, QtCore

from prymatex.utils.decorators.memoize import memoized

RESOURCES = {}
RESOURCES_READY = False

THEME_ICON_TEST = "document-open"

STATICMAPPING = (
    # Process
    (os.path.normcase("/groups/red.png"), "porcess-not-running"),
    (os.path.normcase("/groups/yellow.png"), "porcess-starting"),
    (os.path.normcase("/groups/green.png"), "porcess-running"),
    
    # Symbols
    (os.path.normcase("/groups/blue.png"), "symbol-class"),
    (os.path.normcase("/groups/green.png"), "symbol-block"),
    (os.path.normcase("/groups/yellow.png"), "symbol-context"),
    (os.path.normcase("/groups/ligthblue.png"), "symbol-function"),
    (os.path.normcase("/groups/brown.png"), "symbol-typedef"),
    (os.path.normcase("/groups/red.png"), "symbol-variable"),
    
    # Scope Root Groups
    (os.path.normcase("/groups/blue.png"), "scope-root-comment"),
    (os.path.normcase("/groups/yellow.png"), "scope-root-constant"),
    (os.path.normcase("/groups/ligthblue.png"), "scope-root-entity"),
    (os.path.normcase("/groups/red.png"), "scope-root-invalid"),
    (os.path.normcase("/groups/green.png"), "scope-root-keyword"),
    (os.path.normcase("/groups/violet.png"), "scope-root-markup"),
    (os.path.normcase("/groups/darkviolet.png"), "scope-root-meta"),
    (os.path.normcase("/groups/gray.png"), "scope-root-storage"),
    (os.path.normcase("/groups/darkgreen.png"), "scope-root-string"),
    (os.path.normcase("/groups/brown.png"), "scope-root-support"),
    (os.path.normcase("/groups/orange.png"), "scope-root-variable"),
    
    #Editor Sidebar
    (os.path.normcase("/sidebar/folding-top.png"), "foldingtop"),
    (os.path.normcase("/sidebar/folding-bottom.png"), "foldingbottom"),
    (os.path.normcase("/sidebar/folding-collapsed.png"), "foldingcollapsed"),
    (os.path.normcase("/sidebar/folding-ellipsis.png"), "foldingellipsis"),
    (os.path.normcase("/sidebar/bookmark-flag.png"), "bookmarkflag"),
    
    #Bundles
    (os.path.normcase("/bundles/bundle.png"), "bundle-item-bundle"),
    (os.path.normcase("/bundles/templates.png"), "bundle-item-template"),
    (os.path.normcase("/bundles/commands.png"), "bundle-item-command"),
    (os.path.normcase("/bundles/languages.png"), "bundle-item-syntax"),
    (os.path.normcase("/bundles/project.png"), "bundle-item-project"),
    (os.path.normcase("/bundles/preferences.png"), "bundle-item-preference"),
    (os.path.normcase("/bundles/drag-commands.png"), "bundle-item-dragcommand"),
    (os.path.normcase("/bundles/snippets.png"), "bundle-item-snippet"),
    (os.path.normcase("/bundles/macros.png"), "bundle-item-macro"),
    (os.path.normcase("/bundles/template-files.png"), "bundle-item-templatefile"),
    
    #Editor Sidebar
    (os.path.normcase("/modes/cursors.png"), "modes-cursors"),
    (os.path.normcase("/modes/snippet.png"), "modes-snippet"),
    (os.path.normcase("/modes/insert.png"), "modes-insert"),
)

#===============================================================
# LOAD
#===============================================================
def buildResourceKey(filename, namePrefixes, installedKeys):
    resourceKey, _ = os.path.splitext(filename)
    index = -1
    while resourceKey in installedKeys and index:
        newKey = "-".join(namePrefixes[index:] + [resourceKey])
        if newKey == resourceKey:
            raise Exception("Esto no puede ocurrir")
        index -= 1
        resourceKey = newKey
    return resourceKey

def loadResources(resourcesPath, staticMapping = []):
    from prymatex.utils import osextra
    def loadSourcePath(sourcePath):
        sources ={}
        for dirpath, dirnames, filenames in os.walk(sourcePath):
            for filename in filenames:
                iconPath = os.path.join(dirpath, filename)
                staticNames = filter(lambda (path, names): iconPath.endswith(path), staticMapping)
                if staticNames:
                    for name in staticNames:
                        sources[name[1]] = iconPath
                else:
                    name = buildResourceKey(filename, osextra.path.fullsplit(dirpath), sources)
                    sources[name] = iconPath
        return sources
    resources = {}
    for source in [ "Icons", "Images" ]:
        resources[source] = loadSourcePath(os.path.join(resourcesPath, source))
    return resources

def loadPrymatexResources(resourcesPath, preferedThemeName = "oxygen"):
    global RESOURCES, RESOURCES_READY
    if not RESOURCES_READY:
        #Test default theme:
        if not QtGui.QIcon.hasThemeIcon(THEME_ICON_TEST):
            themePaths = QtGui.QIcon.themeSearchPaths()
            if os.path.exists("/usr/share/icons") and "/usr/share/icons" not in themePaths:
                themePaths.append("/usr/share/icons")
            themePaths.append(os.path.join(resourcesPath, "IconThemes"))
            themeNames = [ preferedThemeName ]
            for themePath in themePaths:
	    	if os.path.exists(themePath):
                    themeNames.extend(os.listdir(themePath))
            # Set and test
            QtGui.QIcon.setThemeSearchPaths( themePaths )
            for themeName in themeNames:
                QtGui.QIcon.setThemeName(themeName)
                if QtGui.QIcon.hasThemeIcon(THEME_ICON_TEST):
                    break
        RESOURCES = loadResources(resourcesPath, STATICMAPPING)
        installCustomFromThemeMethod()
        RESOURCES_READY = True
        
def installCustomFromThemeMethod():
    #Install fromTheme custom function
    from prymatex.resources.icons import get_icon
    QtGui.QIcon._fromTheme = QtGui.QIcon.fromTheme
    QtGui.QIcon.fromTheme = staticmethod(get_icon)
            
def registerImagePath(name, path):
    global RESOURCES
    external = RESOURCES.setdefault("External", {})
    external[name] = path

def getResourcePath(name, sources = None):
    global RESOURCES
    if sources is not None:
        sources = sources if isinstance(sources, (list, tuple)) else (sources, )
    else:
        sources = RESOURCES.keys()
    for source in sources:
        if source in RESOURCES and name in RESOURCES[source]:
            return RESOURCES[source].get(name)

#===============================================================
# FUNCTIONS
#===============================================================
def getFileType(fileInfo):
    return FileIconProvider.type(fileInfo)
