# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 19:35:19 2020

@author: Martin
"""
#%% Imports - logger
from pynput import keyboard
import pandas as pd
import numpy as np
from pandas.core.common import flatten
import csv
import datetime as dt
import warnings

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LOGGER %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#   This class is responsible for running a listener, recognizing user inputs 
#   according to keyborad's layout and log them into file.
class logger:
    """A class to represent key-logger.

    The logger has single purpose, log the key-strokes. The logger 
    requires the knowledge of the symbol-to-button binding, in order to 
    correctly match the symbol reported from operating system, 
    to a proper keyboard button. 

    Attributes:

    Methods

    """    
    def __init__(self, symbolToButtonDict, path='loggedData.txt', doNotLogButtons=[], escapeButtons=['Esc'], debug=False):
        """Inits logger class with default parameters.
        
        This method checks, whether the logger can correctly assign a 
        unique button to a symbol and throws an exception 
        if the mapping is not unique. The "doNotLogButtons" and 
        "escapeButtons" are checked and throws warning 
        if a wrong button name is found. The default button 
        to stop the logger is 'Esc' and is used 
        when any "escapeButtons" is incorrect. The listener is 
        registered but not started.
        
        Arguments:
            symbolToButtonDict: dict(symbol1: button1, symbol2: button2, ...)
                Obtained from layout.getSymbolToButtonDict()
                
            path : <str>
                'loggedData.txt': (default) path to file 
                    to log the key strokes
            doNotLogButtons: list(<str>)
                []: (default) list of button(s) to be omitted 
                    from logging, for button names see layout.allButtons
            escapeButtons: list(<str>)
                ['Esc']: (default) list of button combinations that 
                    stop the logger.
            debug: <bool>
                True: logger prints the key-presses into the console
                False: no console output on key-press
                
        Raises:
            Exception: mapping "symbolToButtonDict" is not unique
            UserWarinig: wrong button name
                
        Returns:
        """
        # keep the path
        self._path = path
        # symbol-to-button binding
        self._symbolToButtonDict = symbolToButtonDict
        # reverse the symbol-to-button binding to obtain button-to-symbol dictionary
        self._buttonToSymbolDict = {}
        for s in self._symbolToButtonDict.keys():
            for b in [self._symbolToButtonDict[s]]:
                content = self._buttonToSymbolDict.get(b, None)
                if(content == None):
                    self._buttonToSymbolDict[b] = [s]
                else:
                    self._buttonToSymbolDict[b] = self._buttonToSymbolDict[b] + [s]              
        # check consistency
        _Kcheck = [self._buttonToSymbolDict[b] for b in self._buttonToSymbolDict]
        _Kcheck = list(flatten(_Kcheck))
        # inconsistency found
        if len(_Kcheck) > len(set(_Kcheck)):
            raise Exception("Provided "'symbolToButtonDict'" maps the same symbol to multiple buttons. The logger cannot properly log key-strokes, since it cannot determine where the symbol originates.")
        # counter for buttons
        self._buttonCounter = {}
        for b in self._buttonToSymbolDict:
            self._buttonCounter[b] = 0        
        # do not log keys
        self._doNotLogButtons = set()
        self._escapeButtons = set()
        for button in doNotLogButtons:
            if button in self._buttonToSymbolDict.keys():
                self._escapeButtons.add(button)
            else:
                warnings.warn('Button "'+button+'" in doNotLogButtons is not recognized.', UserWarning, stacklevel=1)
        # escape key
        for button in escapeButtons:
            if button in self._buttonToSymbolDict.keys():
                self._escapeButtons.add(button)
                self._doNotLogButtons.add(button)
            else:
                warnings.warn('Button "'+button+'" in escapeButtons is not recognized.', UserWarning, stacklevel=1)
        # prevent typos by assuring that at least "Esc" is there, if the list is empty
        if not self._escapeButtons:
            self._escapeButtons.add('Esc')
            warnings.warn('Default escape button "Esc" is used.', UserWarning, stacklevel=1)
        # keep the debuf option
        self._debug = debug
        # currently active keys
        self.currentlyPressed = set()
        # start non-blocking listener
        self.listener = keyboard.Listener( on_press=self.on_press, on_release=self.on_release )    
    
    #%% listener: on_release
    def on_press(self, key):
        """Callback function for listener when a key is pressed.
        
        Arguments:
            key: <pynput.keyboard.Key>
                
        Raises:
                
        Returns:
        """
        # get key-code (str)
        keyStr = self._key2str(key)
        # get button
        button = self._symbolToButtonDict.get(keyStr, 'None')
        # debug print
        if(self._debug):
            if hasattr(key, 'vk'):
                print('virtual key: ' + str(key.vk).ljust(12) + ' key name: ' + str(keyStr).ljust(12) + '   layout button: ' + button)
            else:
                print('virtual key: ' +      "None".ljust(12) + ' key name: ' + str(keyStr).ljust(12) + '   layout button: ' + button)
        # check if button is logged
        if(button=='None'):
            return
        # add the pressed key
        if(button not in self.currentlyPressed):
            self.currentlyPressed.add(button)
        # check for escape combinations
        if all(b in self.currentlyPressed for b in self._escapeButtons):
            self.stop()
        # log pressed key
        else:
            # check if the key is allowed to be logged
            if(button not in self._doNotLogButtons):
                time = (dt.datetime.now()-self.startTime).total_seconds()
                self._logKeyPress(keyStr, button, time)
        
    #%% listener: on_release
    def on_release(self, key):
        """Callback function for listener when a key is released.
        
        Arguments:
            key: <pynput.keyboard.Key>
                
        Raises:
                
        Returns:
        """
        # get key-code (str)
        keyStr = self._key2str(key)
        # get button
        button = self._symbolToButtonDict.get(keyStr, 'None')
        # check if button is logged
        if(button=='None'):
            return
        try:
            # check for escape (prevent logging to closed file)
            if not all(b in self.currentlyPressed for b in self._escapeButtons):
                # log key(s)
                if(button not in self._doNotLogButtons):
                    time = (dt.datetime.now()-self.startTime).total_seconds()
                    self._logKeyRelease(keyStr, button, time)
            self.currentlyPressed.remove(button)
        except KeyError:
            pass    
        
    #%% write to log file: key press
    def _logKeyPress(self, keyStr, button, time):
        """Format the data written to log file for key press.
        
        Arguments:
            keyStr: <str>
                Key formatted to button name.
            button
                Button name.
            time
                Time of key press.
        Raises:
                
        Returns:
        """
        # prepare values to write
        self._buttonCounter[button] += 1
        counter = self._buttonCounter[button]
        # format strings
        timeFormat = '{:.6f}'.format(time).ljust(15)
        keyStrFormat = keyStr.ljust(15)
        buttonFormat = button.ljust(15)
        eventFormat = '+'+str(counter).zfill(7)
        # write to CSV
        self.log.writerow({'Time':timeFormat, 'Button':buttonFormat, 'Key':keyStrFormat, 'Event':eventFormat})
    
    #%% write to log file: key release
    def _logKeyRelease(self, keyStr, button, time):
        """Format the data written to log file for key release.
        
        Arguments:
            keyStr: <str>
                Key formatted to button name.
            button
                Button name.
            time
                Time of key release.
        Raises:
                
        Returns:
        """
        # prepare values to write
        counter = self._buttonCounter[button]
        # format strings
        timeFormat = '{:.6f}'.format(time).ljust(15)
        keyStrFormat = keyStr.ljust(15)
        buttonFormat = button.ljust(15)
        eventFormat = '-'+str(counter).zfill(7)
        # write to CSV
        self.log.writerow({'Time':timeFormat, 'Button':buttonFormat, 'Key':keyStrFormat, 'Event':eventFormat})
        
    #%% translate key to string
    def _key2str(self, key):
        """Format the key name into a button name.
        
        Arguments:
            key: <pynput.keyboard.Key>
            
        Raises:
                
        Returns:
        """
        if hasattr(key, 'char'):
            keyStr = str(key.char)
        else:
            keyStr = str(key).replace('Key.','')
        return keyStr        

    #%% start listener
    def start(self):
        """Start the key*logger listener
        
        This method starts the listener, that listens to key presses 
        and releases. The logged data are appended to the log file, 
        assuring the timing is linear (continues from the last value).
        
        Arguments:
            
        Raises:
                
        Returns:
        """
        # check if file exists
        try:
            df = pd.read_csv(self._path, nrows=1, delimiter='\t')
            fileExists = isinstance(df['Time'][0].astype(float), float) \
                        and isinstance(df['Key'][0], str) \
                        and isinstance(df['Button'][0], str) \
                        and isinstance(df['Event'][0].astype(int), np.int32)
            del(df)
        except: # catch all exceptions
            fileExists = False
            
        # start a new file
        logFields = ('Time', 'Key', 'Button', 'Event')
        if(fileExists):
            self.logFile = open(self._path, 'a')
        else:
            self.logFile = open(self._path, 'w')
        self.log = csv.DictWriter(self.logFile, fieldnames=logFields, delimiter='\t', lineterminator = '\n', quoting = csv.QUOTE_NONE, quotechar='',escapechar='\t')
        self.log.writeheader()
        
        # get the time when the app started
        self.startTime = dt.datetime.now()
        # start listener
        self.listener.start()
        # show that the logger has started
        print('-- MagPie-ML logger has started, key stroke data are stored in file ./'+self._path+' --')
        
    #%% stop listener
    def stop(self):
        """Start the key*logger listener
        
        This method starts the listener, that listens to key presses 
        and releases. The log file if opened for writting 
        (previous content is deleted).
        
        Arguments:
            
        Raises:
                
        Returns:
        """
        # stop the listener
        self.listener.stop()
        # close the file
        self.logFile.close()
        # show that the logger has stopped
        print('-- MagPie-ML logger has stopped, key stroke data are stored in file ./'+self._path+' --')