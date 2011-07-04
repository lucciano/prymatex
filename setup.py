#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  https://launchpad.net/encuentro

"""Build tar.gz for prymatex.

Needed packages to run (using Debian/Ubuntu package names):
"""

import os

from distutils.command.install import install
from distutils.command.build import build
from distutils.command.install_data import install_data
from distutils.core import setup

class QtBuild(build):
    """Build PyQt (.ui) files and resources."""
 
    description = "build PyQt GUIs (.ui)."
 
    def compile_ui(self, ui_file, py_file=None):
        """Compile the .ui files to python modules."""
        # Search for pyuic4 in python bin dir, then in the $Path.
        if py_file is None:
            py_file = os.path.split(ui_file)[1]
            py_file = os.path.splitext(py_file)[0] + '.py'
            py_file = os.path.join('prymatex', 'ui', py_file)
        # we indeed want to catch Exception, is ugle but w need it
        # pylint: disable=W0703
        try:
            from PyQt4 import uic
            fp = open(py_file, 'w')
            uic.compileUi(ui_file, fp)
            fp.close()
        except Exception, e:
            self.warn('Unable to compile user interface %s: %s', py_file, e)
            if not os.path.exists(py_file) or not file(py_file).read():
                raise SystemExit(1)
            return
        # pylint: enable=W0703
    def compile_rc(self, rc_file, py_file = None):
        if py_file is None:
            py_file = os.path.basename(rc_file)
            py_file = os.path.splitext(py_file)[0] + '_rc.py'
            py_file = os.path.join('prymatex', py_file)
        try:
            command = 'pyrcc4 %s -o %s'
            os.system(command % (rc_file, py_file))
        except Exception, e:
            self.warn('Unable to compile resources %s: %s', py_file, e)
            if not os.path.exists(py_file) or not file(py_file).read():
                raise SystemExit(1)
            return

    def run(self):
        """Execute the command."""
        self._wrapuic()
        basepath = os.path.join('resources', 'ui')
        for dirpath, _, filenames in os.walk(basepath):
            for filename in filenames:
                if filename.endswith('.ui'):
                    self.compile_ui(os.path.join(dirpath, filename))
        self.compile_rc(os.path.join('resources', 'resources.qrc'))
 
    # pylint: disable=E1002
    _wrappeduic = False
    @classmethod
    def _wrapuic(cls):
        """Wrap uic to use gettext's _() in place of tr()"""
        if cls._wrappeduic:
            return
 
        from PyQt4.uic.Compiler import compiler, qtproxies, indenter
 
        # pylint: disable=C0103
        class _UICompiler(compiler.UICompiler):
            """Speciallized compiler for qt .ui files."""
            def createToplevelWidget(self, classname, widgetname):
                output = indenter.getIndenter()
                output.level = 0
                output.write('from prymatex.utils.translation import ugettext as _')
                return super(_UICompiler, self).createToplevelWidget(classname, widgetname)
                
            def compileUi(self, input_stream, output_stream, from_imports):
                indenter.createCodeIndenter(output_stream)
                w = self.parse(input_stream)

                output = indenter.getIndenter()
                output.write("")

                self.factory._cpolicy._writeOutImports()
                
                for res in self._resources:
                    output.write("from prymatex import %s" % res)
                    #write_import(res, from_imports)

                return {"widgetname": str(w),
                        "uiclass" : w.uiclass,
                        "baseclass" : w.baseclass}
        compiler.UICompiler = _UICompiler
 
        class _i18n_string(qtproxies.i18n_string):
            """Provide a translated text."""
            def __str__(self):
                return "_('%s')" % self.string.encode('string-escape')
        qtproxies.i18n_string = _i18n_string
 
        cls._wrappeduic = True
        # pylint: enable=C0103
    # pylint: enable=E1002

class CustomInstall(install):
    """Custom installation class on package files.

    It copies all the files into the "PREFIX/PROJECTNAME" dir.
    """
    def run(self):
        """Run parent install, and then save the install dir in the script."""
        install.run(self)

        for script in self.distribution.scripts:
            script_path = os.path.join(self.install_scripts, os.path.basename(script))
            with open(script_path, 'rb') as fh:
                content = fh.read()
            content = content.replace('@ INSTALLED_BASE_DIR @', self._custom_data_dir)
            with open(script_path, 'wb') as fh:
                fh.write(content)

    def finalize_options(self):
        """Alter the installation path."""
        install.finalize_options(self)

        # the data path is under 'prefix'
        data_dir = os.path.join(self.prefix, self.distribution.get_name())

        # if we have 'root', put the building path also under it (used normally
        # by pbuilder)
        if self.root is None:
            build_dir = data_dir
        else:
            build_dir = os.path.join(self.root, data_dir[1:])

        # change the lib install directory so all package files go inside here
        self.install_lib = build_dir

        # save this custom data dir to later change the scripts
        self._custom_data_dir = data_dir

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, package_data = [], {}
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
prymatex_dir = 'prymatex'

for dirpath, dirnames, filenames in os.walk(prymatex_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        package = '.'.join(fullsplit(dirpath))
        packages.append(package)
        package_data.setdefault(package, [])
    elif filenames:
        #Find package
        parts = fullsplit(dirpath)
        while '.'.join(parts) not in packages:
            parts = parts[:-1]
        #Build patterns
        patterns = []
        for file in filenames:
            name, ext = os.path.splitext(file)
            pattern = '*%s' % ext
            if not ext:
                patterns.append(name)
            elif pattern not in patterns:
                patterns.append(pattern)
        #Build basename
        basename = os.path.join(*fullsplit(dirpath)[1:])
        package_data['.'.join(parts)].extend([os.path.join(basename, p) for p in patterns])

# Dynamically calculate the version based on prymatex.VERSION.
vmodule = __import__('prymatex.version', fromlist=['prymatex'])
version = vmodule.get_version()
if u'GIT' in version:
    version = ' '.join(version.split(' ')[:-1])

setup(
    name = 'prymatex',
    version = version,
    license = 'GPL-3',
    author = vmodule.AUTHOR,
    author_email = vmodule.AUTHOR_EMAIL,
    description = vmodule.DESCRIPTION,
    long_description = vmodule.LONG_DESCRIPTION,
    url = vmodule.URL,

    packages = packages,
    package_data = package_data,
    scripts = ["prymatex/bin/pmx.py"],

    cmdclass = {
        'install': CustomInstall,
        'build_ui': QtBuild 
    }
)
