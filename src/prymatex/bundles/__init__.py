import os

# for run as main
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('../..'))

from glob import glob
from prymatex.bundles import command, snippet, syntax, preference
from prymatex.bundles.base import PMXBundle
from prymatex.bundles.theme import PMXTheme, PMXStyle
from prymatex.bundles.qtadapter import buildQTextFormat
from prymatex.config import settings

#BundleItemName, BundlePattern, BundleItemClass
BUNDLE_ELEMENTS = (('Syntax', 'Syntaxes/*', syntax.PMXSyntax),
                   ('Snippet', 'Snippets/*', snippet.PMXSnippet),
                   #('Macro', 'Macros/*', macro.PMXMacro),
                   ('Command', 'Commands/*', command.PMXCommand),
                   ('Preference', 'Preferences/*', preference.PMXPreference)
                   )

def load_prymatex_bundles(after_load_callback = None):
    paths = glob(os.path.join(settings.PMX_BUNDLES_PATH, '*.tmbundle'))
    counter = 0
    total = len(paths)
    for path in paths:
        if callable(after_load_callback):
            after_load_callback(counter = counter, total = total, name = os.path.basename(path).split('.')[0])
        PMXBundle.loadBundle(path, BUNDLE_ELEMENTS, 'pryamtex')
        counter += 1
    return counter

def load_prymatex_themes(after_load_callback = None):
    paths = glob(os.path.join(settings.PMX_THEMES_PATH, '*.tmTheme'))
    counter = 0
    total = len(paths)
    for path in paths:
        if callable(after_load_callback):
            after_load_callback(counter = counter, total = total, name = os.path.basename(path).split('.')[0])
        PMXTheme.loadTheme(path)
        counter += 1
    return counter

#Adapters
#setattr(PMXStyle, 'QTextFormat', property(buildQTextFormat))