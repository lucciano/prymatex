#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Command's module    
'''
import os
from subprocess import Popen, PIPE, STDOUT

from prymatex.support.bundle import PMXBundleItem
from prymatex.support.utils import compileRegexp, prepareShellScript

class PMXCommand(PMXBundleItem):
    KEYS = [    'input', 'fallbackInput', 'standardInput', 'output', 'standardOutput',  #I/O
                'command', 'winCommand', 'linuxCommand',                                #System based Command
                'inputFormat',                                                          #Formato requerido en la entrada
                'beforeRunningCommand',                                                 #Antes de correr el command
                'capturePattern', 'fileCaptureRegister',
                'columnCaptureRegister', 'disableOutputAutoIndent',
                'lineCaptureRegister', 'dontFollowNewOutput',
                'autoScrollOutput', 'captureFormatString', 'beforeRunningScript' ]
    TYPE = 'command'
    FOLDER = 'Commands'
    EXTENSION = 'tmCommand'
    PATTERNS = ['*.tmCommand', '*.plist']
    exit_codes = {
                  200: 'discard',
                  201: 'replaceSelectedText',
                  202: 'replaceDocument',
                  203: 'insertText',
                  204: 'insertAsSnippet',
                  205: 'showAsHTML',
                  206: 'showAsTooltip',
                  207: 'createNewDocument'
                  }
    def __init__(self, uuid, namespace, hash, path = None):
        super(PMXCommand, self).__init__(uuid, namespace, hash, path)

    def load(self, hash):
        super(PMXCommand, self).load(hash)
        for key in PMXCommand.KEYS:
            value = hash.get(key, None)
            if value != None and key in [    'capturePattern' ]:
                value = compileRegexp( value )
            setattr(self, key, value)
    
    @property
    def hash(self):
        hash = super(PMXCommand, self).hash
        for key in PMXCommand.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in ['capturePattern']:
                    value = unicode(value)
                hash[key] = value
        return hash
        
    @property
    def systemCommand(self):
        if self.winCommand != None and 'Window' in os.environ['OS']:
            return self.winCommand
        elif self.linuxCommand != None:
            return self.linuxCommand
        else:
            return self.command
    
    def getInputText(self, processor):
        def getInputTypeAndValue(input):
            if input == "none": return None, None
            return input, getattr(processor, input)(self.inputFormat)
        input, value = getInputTypeAndValue(self.input)
        if value == None and self.fallbackInput != None:
            input, value = getInputTypeAndValue(self.fallbackInput)
        if value == None and self.standardInput != None:
            input, value = getInputTypeAndValue(self.standardInput)
            
        if input == 'selection' and value == None:
            value = processor.document(self.inputFormat)
            input = "document"
        elif value == None:
            input = None
        return input, value

    def getOutputHandler(self, code):
        if self.output != 'showAsHTML' and code in self.exit_codes:
            return self.exit_codes[code]
        elif code != 0:
            return "commandError"
        else:
            return self.output
    
    def execute(self, processor):
        if hasattr(self, 'beforeRunningCommand') and self.beforeRunningCommand != None:
            value = getattr(processor, self.beforeRunningCommand)()
            #Solo si es falso, intenta ejecutar para todos los otros valores
            if value == False:
                return
        processor.startCommand(self)
        input_type, input_value = self.getInputText(processor)
        command, env = prepareShellScript(self.systemCommand, processor.environment)
        
        process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, env = env)
        
        if input_type != None:
            process.stdin.write(unicode(input_value).encode("utf-8"))
        process.stdin.close()
        try:
            output_value = process.stdout.read()
        except IOError:
            pass
        process.stdout.close()
        output_type = process.wait()
        output_handler = self.getOutputHandler(output_type)
        # Remove old
        if input_type != None and output_handler in [ "insertText", "insertAsSnippet", "replaceSelectedText" ]:
            print 'delete' + input_type.title()
            deleteMethod = getattr(processor, 'delete' + input_type.title(), None)
            if deleteMethod != None:
                deleteMethod()        

        try:
            output_value = output_value.decode('utf-8')
        except:
            pass
        args = [ output_value ]
        function = getattr(processor, output_handler, None)
        
        if output_handler == "commandError":
            args.append(output_type)
            
        # Insert New
        function(*args)
        
        processor.endCommand(self)

class PMXDragCommand(PMXCommand):
    KEYS = [    'draggedFileExtensions' ]
    TYPE = 'dragcommand'
    FOLDER = 'DragCommands'
    FILES = ['*.tmCommand', '*.plist']
    def __init__(self, uuid, namespace, hash = None, path = None):
        super(PMXDragCommand, self).__init__(uuid, namespace, hash, path)

    def load(self, hash):
        super(PMXDragCommand, self).load(hash)
        for key in PMXDragCommand.KEYS:
            value = hash.get(key, None)
            if key in [ 'draggedFileExtensions' ]:
                value = map(lambda extension: extension.strip(), value.split(","))
            setattr(self, key, value)
    
    @property
    def hash(self):
        hash = super(PMXDragCommand, self).hash
        for key in PMXDragCommand.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in [ 'draggedFileExtensions' ]:
                    value = ", ".join(self.draggedFileExtensions)
                hash[key] = value
        return hash
            
    def buildEnvironment(self, directory = "", name = ""):
        env = super(PMXDragCommand, self).buildEnvironment()
        # TM_DROPPED_FILE � relative path of the file dropped (relative to the document directory, which is also set as the current directory).
        env['TM_DROPPED_FILE'] = os.path.join(directory)
        #TM_DROPPED_FILEPATH � the absolute path of the file dropped.
        env['TM_DROPPED_FILEPATH'] = os.path.join(directory)
        #TM_MODIFIER_FLAGS � the modifier keys which were held down when the file got dropped.
        #This is a bitwise OR in the form: SHIFT|CONTROL|OPTION|COMMAND (in case all modifiers were down).
        env['TM_MODIFIER_FLAGS'] = directory
        return env
