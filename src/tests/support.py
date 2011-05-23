
import os, sys
sys.path.append(os.path.abspath('..'))

def test_findPreferences(manager):
    settings = manager.getPreferenceSettings('text.html.textile markup.heading.textile')
    for key in settings.KEYS:
        print key, getattr(settings, key, None)

def test_syntax(manager):
    from prymatex.support.syntax import PMXSyntax
    from time import time
    from prymatex.support.processor import PMXSyntaxProcessor, PMXDebugSyntaxProcessor
    syntax = manager.getSyntaxByScopeName('source.python')
    print syntax.scopeName
    file = open('../prymatex/gui/editor/codeedit.py', 'r');
    start = time()
    syntax.parse(file.read(), PMXSyntaxProcessor())
    file.close()
    print "Time:", time() - start

def test_creationAndDeleteBundle(manager):
    bundle = manager.createBundle('Diego')
    bundle.save()
    item = manager.createBundleItem('MiSnippet', 'snippet', bundle)
    item.save()
    manager.deleteBundle(bundle)

def test_bundleItemsCRUD(manager):
    items = manager.findBundleItems(name = "thon")
    for item in items:
        item = manager.updateBundleItem(item, tabTrigger = "cacho")
        print item.tabTrigger
        
if __name__ == "__main__":
    from prymatex.support.manager import PMXSupportManager
    manager = PMXSupportManager()
    manager.addNamespace('prymatex', os.path.abspath('../bundles/prymatex'))
    manager.addNamespace('user', os.path.abspath(os.path.join(os.path.expanduser('~'), '.prymatex')))
    manager.loadSupport()
    test_bundleItemsCRUD(manager)