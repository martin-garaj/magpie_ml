# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 19:35:19 2020

@author: Martin
"""
#%% Imports - layout
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from pandas.core.common import flatten
import warnings
import numpy as np


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LAYOUT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%% Class
#   The layout class represents the keyboard's layout. This includes 2 major parts:
#       graphics - related to representing used data in 2D/3D plots, including a detailed layout of the keyboard
#       mapping - maping symbols (e.g. A,b,c,1,2,3,@,!,.,/,) to the actual buttons (physical keys) on the keyboard
class layout:
    """A class to represent keyboard layout.

    Layout class has 2 major functions. At first is holds an information
    about the keyboard layout (position of buttons on keyboard). 
    Secondly, it provides mapping from symbols (e.g. ['z', 'Z'] maps 
    to button 'Z', ['~','`'] maps to button 'Tilde'). This mapping needs
    to be unique in order to be reversible. The one-to-many 
    (further refered as button-to-symbol mapping is stored in 
    dictionary _K[<button>]['symbol']). The one-to-one mapping 
    (further refered to as symbol-to-button is obtained by reversing 
    the mapping _K and is stored in dictionary _M[symbol]).

    Attributes:
        self.allButtons
        self.alphabetButtons
        self.numericButtons
        self.punctuationButtons
        self.functionalButtons 
        self.extendedButtons
        self.finger1Buttons
        self.finger2Buttons
        self.finger3Buttons
        self.finger4Buttons
        self.finger7Buttons
        self.finger8Buttons
        self.finger9Buttons
        self.finger10Buttons
        self.leftHandButtons
        self.rightHandButtons     
            Predefined lists of buttons list(<str>) to provide 
                simple way to partition the keyboard layout.

    Methods:
        layout(keyboardType='external', qwerty=True, shift_l_long=True, enter_tall=True, language='englishUS', alpha=0.1, facecolor='blue', edgecolor='black')
        bindSymbolToButton(symbol, button)
        unbindSymbolFromButton(symbol, button)
        createButton(button, x, y, symbols, dx, dy, z = 0.0, dz=1.0, edgecolor='black',facecolor='blue', alpha=0.1)
        deleteButton(button)
        symbol2button(symbol)
        getButtonList()
        getSymbolList()
        getButtonToSymbolDict()
        getSymbolToButtonDict()
        setButtonValue(button, labels, value)
        getButtonValue(button, labels)
        plotKeyboard3D(axis, defaultLook=True, nameShow=True, bindShow=False, dzShow=True, textOffset=[0.0, 0.0, 0.0], aspectRatioModifier=[1.0, 1.0, 1.0], fontSize=10)
        plotKeyboard2D(axis, defaultLook=True, nameShow=True, bindShow=False, dzShow=True, textOffset=[0.0, 0.0, 0.0], fontSize=10)        
    """
    #%% init
    def __init__(self, keyboardType='external', qwerty=True, shift_l_long=True, enter_tall=True, language='englishUS', alpha=0.1, facecolor='blue', edgecolor='black'):
        """Inits layout class with default parameters.
        
        Arguments:
            keyboardType: <str>
                'external': (default) large format keyboard (e.g. desktop)
                'builtin': small form-factor keyboard (e.g. laptop)
            qwerty : <bool>
                True: (default) QWERTY
                False: QWERTZ
            shift_l_long: <bool>
                True: (default) left SHIFT is followed by the letter 'Z' 
                    (qwerty: True) or 'Y' (qwerty: False)
                False: left sHIFT is followed by 's10' (symbol button 10)
            enter_tall: <bool>
                True: (default) Enter button streches across row 2 and 3
                False: Enter button occupies row 3, s6 is moved above Enter
            language: <str>
                'englishUS': (default) US English keyboard (e.g. SHIFT+3=#)
                'englishUK': UK English keyboard (e.g. SHIFT+3=£)
            alpha: <float>
                0.1: (default) initial value of alpha channel
            facecolor: <str> or <list(<int>)>
                'blue': (default) inital value of button color
            edgecolor: <str> or <list(<int>)>
                'black': (default) inital value of buttonedge color
                
        Raises:
            UserInput: an error occured due to changes in mapping 
                of symbol to button (changes to internal variable _K)
                
        Returns:
        """
        ### input check
        # keyboardType
        if(keyboardType=='external' or  keyboardType=='builtin'):
            self._keyboardType = keyboardType
        else:
            raise Exception("layout.__init__(..., keyboardType=<'external', 'builtin'>, ...): incorrect parameter keyboardType=<"+keyboardType+">")
        # language
        if(language=='englishUS' or  language=='englishUK'):
            self._language = language
        else:
            raise Exception("layout.__init__(..., language=<'englishUS','englishUK'>, ...): incorrect parameter language=<"+language+">")
        self._qwerty = qwerty
        self._shift_l_long = shift_l_long
        self._enter_tall   = enter_tall
        
        #%% keyboard layout dict
        self._K = {}
        
        ## abbreviated language variable for terniary operator
        if(self._language == 'englishUS'):
            _L = True
        else:
            _L = False
        
        ### external keyboard
        if(self._keyboardType=='external'):
            # row 1
            _rowX = 0
            self._K['Esc']   = {'symbol':['esc'],                               'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F1']    = {'symbol':['f1'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+1    , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F2']    = {'symbol':['f2'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F3']    = {'symbol':['f3'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F4']    = {'symbol':['f4'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F5']    = {'symbol':['f5'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+0.25 , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F6']    = {'symbol':['f6'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F7']    = {'symbol':['f7'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F8']    = {'symbol':['f8'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F9']    = {'symbol':['f9'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+0.25 , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F10']   = {'symbol':['f10'],                               'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F11']   = {'symbol':['f11'],                               'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F12']   = {'symbol':['f12'],                               'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            
            self._K['PrtSc']   = {'symbol':['print_screen'],                    'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+0.25 , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['ScrLk']   = {'symbol':['scroll_lock'],                     'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['PauBrk']  = {'symbol':['pause'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            # row 2
            _rowX = 1
            self._K['Tilde']   = {'symbol':['`','~'] if _L else ['`','¬','¦','§','±'],  'graphics': {'x':_rowX, 'y':0                                                                                             ,  'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['1']       = {'symbol':['1','!'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['2']       = {'symbol':['2','@'] if _L else ['2','"'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['3']       = {'symbol':['3','#'] if _L else ['3','£'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['4']       = {'symbol':['4','$'] if _L else ['4','$','€'],  'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['5']       = {'symbol':['5','%'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['6']       = {'symbol':['6','^'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['7']       = {'symbol':['7','&'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['8']       = {'symbol':['8','*'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['9']       = {'symbol':['9','('],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['0']       = {'symbol':['0',')'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s0']      = {'symbol':['-','_'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s1']      = {'symbol':['=','+'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['BckSpc']  = {'symbol':['backspace'],                       'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}

            self._K['Ins']     = {'symbol':['insert'],                          'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+0.25 , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Home']    = {'symbol':['home'],                            'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['PgUp']    = {'symbol':['page_up'],                         'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            ## row 3
            _rowX = 2
            self._K['Tab']     = {'symbol':['tab'],                             'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Q']       = {'symbol':['q','Q'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['W']       = {'symbol':['w','W'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['E']       = {'symbol':['e','E'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['R']       = {'symbol':['r','R'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['T']       = {'symbol':['t','T'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            if(self._qwerty):
                self._K['Y']      = {'symbol':['y','Y'],                        'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:
                self._K['Z']      = {'symbol':['z','Z'],                        'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['U']       = {'symbol':['u','U'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['I']       = {'symbol':['i','I'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['O']       = {'symbol':['o','O'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['P']       = {'symbol':['p','P'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s2']      = {'symbol':['[','{'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s3']      = {'symbol':[']','}'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            if(self._enter_tall):        
                self._K['Enter']   = {'symbol':['enter'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+0.5  , 'z':0, 'dx':2, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:
                self._K['s6']      = {'symbol':['\\','|'] if _L else ['#','~','\\'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
                
            self._K['Del']     = {'symbol':['delete'],                          'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+0.25 , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['End']     = {'symbol':['end'],                             'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['PgDn']    = {'symbol':['page_down'],                       'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            # row 4
            _rowX = 3
            self._K['CapsLck'] = {'symbol':['caps_lock'],                       'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':1.5,'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['A']       = {'symbol':['a','A'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['S']       = {'symbol':['s','S'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['D']       = {'symbol':['d','D'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F']       = {'symbol':['f','F'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['G']       = {'symbol':['g','G'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['H']       = {'symbol':['h','H'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['J']       = {'symbol':['j','J'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['K']       = {'symbol':['k','K'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['L']       = {'symbol':['l','L'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s4']      = {'symbol':[';',':'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s5']      = {'symbol':["'",'"'] if _L else ["'",'@'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            if(self._enter_tall):
                self._K['s6']      = {'symbol':['\\','|'] if _L else ['#','~','\\'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:
                self._K['Enter']   = {'symbol':['enter'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']  , 'z':0, 'dx':1, 'dy':2, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}

            # row 5
            _rowX = 4
            if(self._shift_l_long):
                self._K['Shift_l'] = {'symbol':['shift','shift_l'],                     'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':2.0,'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:
                 self._K['Shift_l'] = {'symbol':['shift','shift_l'],                    'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':1.0,'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
                 # add new button
                 self._K['s10'] = {'symbol':['\\','|'],                                 'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1.0,'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
                 # change symbol assignmnet at 's6'
                 self._K['s6']['symbol'] = []               
                
            if(qwerty):
                self._K['Z']       = {'symbol':['z','Z'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:    
                self._K['Y']       = {'symbol':['y','Y'],                       'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['X']       = {'symbol':['x','X'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['C']       = {'symbol':['c','C'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['V']       = {'symbol':['v','V'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['B']       = {'symbol':['b','B'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['N']       = {'symbol':['n','N'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['M']       = {'symbol':['m','M'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s7']      = {'symbol':[',','<'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s8']      = {'symbol':['.','>'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s9']      = {'symbol':['/','?'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Shift_r'] = {'symbol':['shift_r'],                         'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':2.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}

            self._K['aUp']    = {'symbol':['up'],                                   'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+1.25      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            ## row 6
            _rowX = 5
            self._K['Ctrl_l']  = {'symbol':['ctrl','ctrl_l'],                   'graphics': {'x':_rowX, 'y':0        , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Alt_l']   = {'symbol':['alt', 'alt_l'],                    'graphics': {'x':_rowX, 'y':3        , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Space']   = {'symbol':['space', ' '],                      'graphics': {'x':_rowX, 'y':4.5      , 'z':0, 'dx':1, 'dy':5.0, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Alt_r']   = {'symbol':['alt_r','alt_gr'],                  'graphics': {'x':_rowX, 'y':9.5      , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Ctrl_r']  = {'symbol':['ctrl_r'],                          'graphics': {'x':_rowX, 'y':13.0     , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}

            self._K['aLeft']  = {'symbol':['left'],                             'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+0.25 , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['aDown']  = {'symbol':['down'],                             'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['aRight'] = {'symbol':['right'],                            'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}

        ### builtin keyboard (different geometry of arrow keys and functional keys)
        if(keyboardType=='builtin'):
            # row 1
            _rowX = 0
            self._K['Esc']   = {'symbol':['esc'],                               'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F1']    = {'symbol':['f1'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F2']    = {'symbol':['f2'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F3']    = {'symbol':['f3'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F4']    = {'symbol':['f4'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F5']    = {'symbol':['f5'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F6']    = {'symbol':['f6'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F7']    = {'symbol':['f7'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F8']    = {'symbol':['f8'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F9']    = {'symbol':['f9'],                                'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F10']   = {'symbol':['f10'],                               'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F11']   = {'symbol':['f11'],                               'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F12']   = {'symbol':['f12'],                               'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['PrtSc'] = {'symbol':['print_screen'],                    'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']        , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Ins']   = {'symbol':['insert'],                     'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']             , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Del']   = {'symbol':['delete'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']       , 'z':0, 'dx':1, 'dy':0.9, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            # row 2
            _rowX = 1
            self._K['Tilde']   = {'symbol':['`','~'] if _L else ['`','¬','¦','§','±'],  'graphics': {'x':_rowX, 'y':0                                                                                             ,  'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['1']       = {'symbol':['1','!'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['2']       = {'symbol':['2','@'] if _L else ['2','"'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['3']       = {'symbol':['3','#'] if _L else ['3','£'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['4']       = {'symbol':['4','$'] if _L else ['4','$','€'],  'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['5']       = {'symbol':['5','%'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['6']       = {'symbol':['6','^'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['7']       = {'symbol':['7','&'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['8']       = {'symbol':['8','*'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['9']       = {'symbol':['9','('],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['0']       = {'symbol':['0',')'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s0']      = {'symbol':['-','_'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s1']      = {'symbol':['=','+'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['BckSpc']  = {'symbol':['backspace'],                       'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            ## row 3
            _rowX = 2
            self._K['Tab']     = {'symbol':['tab'],                             'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Q']       = {'symbol':['q','Q'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['W']       = {'symbol':['w','W'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['E']       = {'symbol':['e','E'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['R']       = {'symbol':['r','R'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['T']       = {'symbol':['t','T'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            if(qwerty):
                self._K['Y']      = {'symbol':['y','Y'],                        'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:
                self._K['Z']      = {'symbol':['z','Z'],                        'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['U']       = {'symbol':['u','U'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['I']       = {'symbol':['i','I'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['O']       = {'symbol':['o','O'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['P']       = {'symbol':['p','P'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s2']      = {'symbol':['[','{'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s3']      = {'symbol':[']','}'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            if(self._enter_tall):        
                self._K['Enter']   = {'symbol':['enter'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']+0.5  , 'z':0, 'dx':2, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:
                self._K['s6']      = {'symbol':['\\','|'] if _L else ['#','~','\\'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            # row 4
            _rowX = 3
            self._K['CapsLck'] = {'symbol':['caps_lock'],                       'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':1.5,'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['A']       = {'symbol':['a','A'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['S']       = {'symbol':['s','S'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['D']       = {'symbol':['d','D'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['F']       = {'symbol':['f','F'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['G']       = {'symbol':['g','G'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['H']       = {'symbol':['h','H'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['J']       = {'symbol':['j','J'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['K']       = {'symbol':['k','K'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['L']       = {'symbol':['l','L'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s4']      = {'symbol':[';',':'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s5']      = {'symbol':["'",'"'] if _L else ["'",'@'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            if(self._enter_tall):
                self._K['s6']      = {'symbol':['\\','|'] if _L else ['#','~','\\'],      'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:
                self._K['Enter']   = {'symbol':['enter'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']  , 'z':0, 'dx':1, 'dy':2, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            # row 5
            _rowX = 4
            if(self._shift_l_long):
                self._K['Shift_l'] = {'symbol':['shift','shift_l'],                     'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':2.0,'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:
                 self._K['Shift_l'] = {'symbol':['shift','shift_l'],                    'graphics': {'x':_rowX, 'y':0                                                                                             , 'z':0, 'dx':1, 'dy':1.0,'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
                 # add new button
                 self._K['s10'] = {'symbol':['\\','|'],                                 'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1.0,'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
                 # change symbol assignmnet at 's6'
                 self._K['s6']['symbol'] = []               
            if(qwerty):
                self._K['Z']       = {'symbol':['z','Z'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            else:    
                self._K['Y']       = {'symbol':['y','Y'],                       'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['X']       = {'symbol':['x','X'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['C']       = {'symbol':['c','C'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['V']       = {'symbol':['v','V'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['B']       = {'symbol':['b','B'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['N']       = {'symbol':['n','N'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['M']       = {'symbol':['m','M'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s7']      = {'symbol':[',','<'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s8']      = {'symbol':['.','>'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['s9']      = {'symbol':['/','?'],                           'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Shift_r'] = {'symbol':['shift_r'],                         'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':2.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            ## row 6
            _rowX = 5
            self._K['Ctrl_l']  = {'symbol':['ctrl','ctrl_l'],                   'graphics': {'x':_rowX, 'y':0        , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Alt_l']   = {'symbol':['alt', 'alt_l'],                    'graphics': {'x':_rowX, 'y':3        , 'z':0, 'dx':1, 'dy':1.5, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Space']   = {'symbol':['space', ' '],                      'graphics': {'x':_rowX, 'y':4.5      , 'z':0, 'dx':1, 'dy':5.0, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Alt_r']   = {'symbol':['alt_r','alt_gr'],                  'graphics': {'x':_rowX, 'y':9.5      , 'z':0, 'dx':1, 'dy':1.0, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['Ctrl_r']  = {'symbol':['ctrl_r'],                          'graphics': {'x':_rowX, 'y':10.5      , 'z':0, 'dx':1, 'dy':1.0, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}

            self._K['aLeft']  = {'symbol':['left'],                             'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['aUp']    = {'symbol':['up'],                               'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':0.5, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['aDown']  = {'symbol':['down'],                             'graphics': {'x':_rowX+0.5, 'y':self._K[list(self._K)[-1]]['graphics']['y']                                               , 'z':0, 'dx':0.5, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            self._K['aRight'] = {'symbol':['right'],                            'graphics': {'x':_rowX, 'y':self._K[list(self._K)[-1]]['graphics']['y']+self._K[list(self._K)[-1]]['graphics']['dy']      , 'z':0, 'dx':1, 'dy':1, 'dz':1, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}

        #%% keyboard layout definition
        # predefined button sets
        self.allButtons         = self._K.keys()
        self.alphabetButtons    = ['Q', 'W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
        self.numericButtons     = ['1','2','3','4','5','6','7','8','9','0']
        if(shift_l_long):
            self.punctuationButtons = ['s0','s1','s2','s3','s4','s5','s6','s7','s8','s9']
        else:
            self.punctuationButtons = ['s0','s1','s2','s3','s4','s5','s6','s7','s8','s9', 's10']     
        if(keyboardType=='external'):
            self.functionalButtons  = ['Esc','Tab','CapsLck','Shift_l','Ctrl_l','Alt_l','Space','BckSpc','Enter','Shift_r','Alt_r','Ctrl_r']   
            self.extendedButtons    = ['PrtSc','ScrLk','PauBrk','Ins','Home','PgUp','Del','End','PgDn','aUp','aLeft','aDown','aRight']  
        elif(keyboardType=='builtin'):
            self.functionalButtons  = ['Esc','Tab','CapsLck','Shift_l','Ctrl_l','Alt_l','Space','BckSpc','Enter','Shift_r','Alt_r','Ctrl_r']   
            self.extendedButtons    = ['PrtSc','Ins','Del','aUp','aLeft','aDown','aRight']  
        # according to https://thekeyboardreviews.com/typing-speed-how-can-i-improve-myself/
        if(shift_l_long):
            self.finger1Buttons    = ['1','Tab','Q','CapsLck', 'A', 'Shift_l', 'Z']
        else:
            self.finger1Buttons    = ['1','Tab','Q','CapsLck', 'A', 'Shift_l', 'Z','s10']
        self.finger2Buttons    = ['2','W','S','X']
        self.finger3Buttons    = ['3','E','D','C']
        self.finger4Buttons    = ['4','5','R','T','F','G','V','B']
        self.finger7Buttons    = ['6','7','Y','U','H','J','N','M']
        self.finger8Buttons    = ['8','I','K','s7']
        self.finger9Buttons    = ['9','O','L','s8']
        self.finger10Buttons    = ['0','s0','s1','P','s2','s3','s4','s5','s6','s9']    
        
        self.leftHandButtons   = self.finger1Buttons + self.finger2Buttons + self.finger3Buttons + self.finger4Buttons
        self.rightHandButtons  = self.finger7Buttons + self.finger8Buttons + self.finger9Buttons + self.finger10Buttons

        #%% keyboard mapping dict
        self._M = {} 
        # symbol to button mapping
        _doubleBind = self._updateSymbolToButtonMap()
        if(len(_doubleBind)>0):
            warnings.warn('Changes to _K[button][''symbol''] within the \
                          class constructor __init__ raised a warning \
                          that the symbol-to-button map is not unique. \
                          The dictionary of {symbol:[button1, button2, \
                          ...]} is printed to console.', \
                            UserWarning, stacklevel=1)
            print(_doubleBind)
    
    #%% _updateSymbolToButtonMap
    def _updateSymbolToButtonMap(self):
        """Updates map _M providing unique symbol-to-button map. 
        
        This method updates the internal _M symbol-to-button map and 
        checks whether the mapping is unique. The method returns a list 
        of symbol(s) bound to multiple buttons.
        
        Returns:
            dict={symbol: [button1, button2, ...]}
                A dictionary with a symbol bound to multiple buttons. 
                This requires correction, such that every symbol is 
                mapped to unique button (the opposite doesn't hold, 
                since one button can produce multiple symbols)
        """
        _ERRORdoubleBind = {}
        for k in self._K:
            for v in self._K[k]['symbol']:
                if(v in self._M.keys()): # the "v" is already mapped to a key
                    # keep the double-bound keys in _ERRORdoubleBind
                    if(k in _ERRORdoubleBind):
                        _ERRORdoubleBind[v] = _ERRORdoubleBind[k] + [k] + [self._M[v]]
                    else:
                        _ERRORdoubleBind[v] = [k] + [self._M[v]]
                self._M[v] = k
        return _ERRORdoubleBind

    #%% Bind symbol to button
    def bindSymbolToButton(self, symbol, button):
        """Create new binding of a symbol to a button.
        
        Arguments:
            symbol: <str>
                A symbol on a keyboard (e.g. 'k', '!', ':', '\\', 'P').
            button: <str>
                Predefined button name from self.allButtons list or
                    user-defined button.
                    
        Returns:
            <int>
            -1: error, raises warining
            0: a symbol is already bound to a button (no change)
            1: successfult binding of a symbol to a button
            
        Raises:
            UserWarning: Wrong button name.
            UserWarning: Non-unique symbol-to-button binding.
        """
        if(button not in self._K.keys()):
            warnings.warn('Button "'+button+'" is not recognized as valid button name, see layout.allButtons for a list of valid button names.', \
                            UserWarning, stacklevel=1)
            # return that binding was not performed due to error
            return -1
        else:
            # binding already exists
            if(symbol in self._K[button]['symbol']):
                # return no change
                return 0
            # perform binding
            else:
                # add new bind
                self._K[button]['symbol'].append(symbol)                
                # redo mapping
                self._M = {} 
                # perform symbol-to-button mapping
                _doubleBind = self._updateSymbolToButtonMap()
                # check for inconsistency
                if(len(_doubleBind)>0):
                    warnings.warn('Symbol-to-button map is not unique. The dictionary of {symbol:[button1, button2, ...]} is printed to console.', UserWarning, stacklevel=1)
                    print(_doubleBind)
                # return the new binding is performed
                return 1

    #%% Unbind symbol from button
    def unbindSymbolFromButton(self, symbol, button):
        """Remove a binding of a symbol to a button.
        
        Arguments:
            symbol: <str>
                A symbol on a keyboard (e.g. 'k', '!', ':', '\\', 'P').
            button: <str>
                Predefined button name from self.allButtons list or
                    user-defined button.
                    
        Returns:
            <int>
            -1: error, raises warining
            0: a symbol is not bound to a button (no change)
            1: successfult unbinding of a symbol from a button
            
        Raises:
            UserWarning: Wrong button name.
            UserWarning: Non-unique symbol-to-button binding.
        """
        if(button not in self._K.keys()):
            warnings.warn('Button "'+button+'" is not recognized as valid button name, see layout.allButtons for a list of valid button names.', \
                            UserWarning, stacklevel=1)
            return -1
        else:
            # binding already exists
            if(symbol in self._K[button]['symbol']):
                self._K[button]['symbol'].remove(symbol)
                # redo mapping
                self._M = {} 
                # symbol to button mapping
                self._updateSymbolToButtonMap()
                return 1
            # perform binding
            else:    
                warnings.warn('Symbol "'+symbol+'" is not bound to Button "'+button+'".', UserWarning, stacklevel=1)
                return -1
            
    #%% Create new button
    def createButton(self, button, x, y, symbols, dx, dy, z = 0.0, dz=1.0, edgecolor='black',facecolor='blue', alpha=0.1):
        """Create a new button that will be displayed in the layout
        
        Arguments:
            button: <str>     
                Unique button name.
            x: <float>           
                Keyboard row (0->row with Esc, 5->row with Spacebar)    
            y: <float>           
                Keyboard column (0->Esc,Tab,Caps,Shift_l,Ctrl_l, 
                    alphabetic key size=1, size of Spacebar is 5).
            symbols: list(<str>)     
                List of strings, where each string represents 
                    a symbol that maps to the button.
            dx: <float>          
                Height of the button (alphabetic key height is 1.0)
            dy: <float>          
                Width of the button (alphabetic key width is 1.0)
            z: <float>           
                Bottom of the button (default=0.0)
            dz: <float>          
                Top of the button (default=1.0 but this is meant to be 
                    used to represent user data when plotting in 3D).
            edgecolor: <str>     
                Initial edgecolor.
            edgecolor: <str>     
                Initial facecolor.
            edgecolor: <str>     
                Initial alpha-channel value.
                    
        Returns:
            <int>
            -1: error, raises exception
            1: successfult unbinding of a symbol from a button
            
        Raises:
            Exception: Wrong button name.
            UserWarning: Non-unique symbol-to-button binding.
        """        
        if(button in self._K.keys()):    
            raise Exception("layout.createButton(..., button, ...): Button "+button+" is already used.")
            return -1
        else:
            self._K[button]  = {'symbol':symbols, 'graphics': {'x':x, 'y':y, 'z':z, 'dx':dx, 'dy':dy, 'dz':dz, 'edgecolor':edgecolor, 'facecolor':facecolor, 'alpha':alpha}, 'value': {}}
            # redo mapping
            self._M = {} 
            # symbol to button mapping
            _doubleBind = self._updateSymbolToButtonMap()
            if(len(_doubleBind)>0):
                warnings.warn('Symbol-to-button map is not unique. The dictionary of {symbol:[button1, button2, ...]} is printed to console.', UserWarning, stacklevel=1)
                print(_doubleBind)
            return 1

    #%% Delete button  
    def deleteButton(self, button):
        """Remove a button from layout.
        
        Arguments:
            button: <str>     
                Name f an existing button.
                    
        Returns:
            <int>
            -1: error, raises exception
            1: successfult unbinding of a symbol from a button
            
        Raises:
            Exception: Wrong button name.
        """     
        if(button in self._K.keys()):  
            del(self.K[button])
            # redo mapping
            self._M = {} 
            # symbol to button mapping
            self._updateSymbolToButtonMap()
            return 1
        else:
            raise Exception("layout.deleteButton(..., button, ...): Button "+button+" does not exist.")
            return -1

    #%% Translate symbol to button
    def symbol2button(self, symbol):
        """Translate a symbol to a button.
        
        Arguments:
            symbol: <str>     
                Symbol within a layout
                    
        Returns:
            <str>
                Button from self.allButtons.
            <None>
                Symbol is not bound to any button in the layout.
        """   
        try:
            return self._M[symbol]
        except KeyError:
            return None
        
    #%% Get list of all registered buttons  
    def getButtonList(self):
        """Get a list of all buttons in a layout.
        
        This method returns a list of all buttons in the layout. 
        The returned list is updated according to any introduced 
        changes to original layout (binding, unbinding, 
        button creation, button removal).
        
        Arguments:
                    
        Returns:
            list(<str>)
                List of all buttons in the layout.
        """   
        # return a list of symbol currenly bound to buttons
        return list(flatten([k for k in self._K]))    
    
    #%% Get list of all registered symbols  
    def getSymbolList(self):
        """Get a list of all symbols in a layout.
        
        This method returns a list of all symbols in the layout. 
        The returned list is updated according to any introduced 
        changes to original layout (binding, unbinding, 
        button creation, button removal).
        
        Arguments:
                    
        Returns:
            list(<str>)
                List of all symbols in the layout.
        """   
        # return a list of symbol currenly bound to buttons
        return list(flatten([m for m in self._M]))
    
    #%% Get dictionary that translate a button to a list of bound symbols
    ### retunrs
    #   Dictionary {button=<str>:[symbols=<str>]}
    def getButtonToSymbolDict(self):
        """Get a dictionary storing button-to-symbol map.
        
        This method returns a dictionary in form:
            {button1: [symbol1, symbol2, ...],
             button2: [symbol3, symbol4, ...]}
        
        Arguments:
                    
        Returns:
            dict{button1: [symbol1, symbol2, ...],
                 button2: [symbol3, symbol4, ...]}
                Map button-to-symbol.
        """   
        # return a dictionary of buttons and symbols
        return {k:self._K[k]['symbol'] for k in self._K}
    
    #%% Get dictionary that translate a symbol to a button
    def getSymbolToButtonDict(self):
        """Get a dictionary storing button-to-symbol map.
        
        This method returns a dictionary in form:
            {symbol1: button1,
             symbol2: button2,
             symbol3: button1, ...}
        Notice, multiple symbols are ound to the same button 
        (e.g. button 'Z' has symbols 'z', 'Z' bound to it).
        
        Arguments:
                    
        Raises:
            UserWarning: Mapping is not unique.
                
        Returns:
            dict{symbol1: button1,
                 symbol2: button2,
                 symbol3: button1, ...}
                Map symbol-to-button.
        """   
        # redo mapping
        self._M = {} 
        # symbol to button mapping
        _doubleBind = self._updateSymbolToButtonMap()
        if(len(_doubleBind)>0):
            warnings.warn('Symbol-to-button map is not unique. The dictionary of {symbol:[button1, button2, ...]} is printed to console.', UserWarning, stacklevel=1)
            print(_doubleBind)
        return self._M
    
    #%% Set value of button(s)
    def setButtonValue(self, button, labels, value): 
        """Change a value of a button.
        
        This method enables to change the look of the layout when 
        plotted or store additional information 
        (allowed but not recommended).
        
        Arguments:
            button: list(<str>)
                A list of valid button names (e.g. self.allButtons) 
            labels: list(<str>)
                A list (up to 4 items) to change properties of a button.
                    E.g. ['graphics', 'x'], ['graphics', 'edgecolor'],
                         ['graphics', 'facecolor'], ['graphics', 'dx'],
                         ['graphics', 'alpha']

        Raises:
            UserWarning: If len(labels)>4.
                
        Returns:
        """   
        for b in button:
            if(len(labels)==1):
                self._K[b][labels[0]] = value
            elif(len(labels)==2):
                self._K[b][labels[0]][labels[1]] = value
            elif(len(labels)==3):
                self._K[b][labels[0]][labels[1]][labels[2]] = value
            elif(len(labels)==4):
                self._K[b][labels[0]][labels[1]][labels[2]][labels[3]] = value
            else:  
                warnings.warn('Only 4 levels are currently implemented.', UserWarning, stacklevel=1)
    
    #%% Return value of button
    def getButtonValue(self, button, labels):   
        """Get a value of a button.
        
        Getter method that returns a value assigned to a button.
        
        Arguments:
            button: <str>
                A valid button name (see self.allButtons).
            labels: list(<str>)
                A list (up to 4 items) to change properties of a button.
                    E.g. ['graphics', 'x'], ['graphics', 'edgecolor'],
                         ['graphics', 'facecolor'], ['graphics', 'dx'],
                         ['graphics', 'alpha']

        Raises:
            UserWarning: If len(labels)>4.
                
        Returns:
            <str>,<list>,<int>,<other>
                Returns a value stored within a button structure.
        """   
        if(len(labels)==1):
            return self._K[button][labels[0]]
        elif(len(labels)==2):
            return self._K[button][labels[0]][labels[1]]
        elif(len(labels)==3):
            return self._K[button][labels[0]][labels[1]][labels[2]]
        elif(len(labels)==4):
            return self._K[button][labels[0]][labels[1]][labels[2]][labels[3]]
        else:
            warnings.warn('Only 4 levels are currently implemented.', UserWarning, stacklevel=1)
            
    #%% Plot layout in 3D
    def plotKeyboard3D(self, axis, defaultLook=True, nameShow=True, bindShow=False, dzShow=True, textOffset=[0.0, 0.0, 0.0], aspectRatioModifier=[1.0, 1.0, 1.0], fontSize=10):
        """Produce a 3D plot of the keyboard layout.
        
        Arguments:
            axis: <axis>
                A subplot axis.
            defaultLook: <bool>
                True: (default) Applies predefined settings to create 
                    a nice and easy to read plot
                False: plot bar-graph to the axis, do not apply 
                    any changes to the axis
            nameShow: <bool>
                True: (default) plot the button names
                False: button names are not plotted
            bindShow: <bool>
                True: plot bound symbols
                False: (default) do not plot bound symbols
            dzShow: <bool>
                True: (default) plot the value ['graphics', 'dz'], 
                    or in other words, the height of the button 
                    to better visualize the data
                False: value is not plotted
            textOffset: list(<float>, <float>, <float>)
                [0.0, 0.0, 0.0]: (default) offset to the plotted text 
                    (depends on nameShow, bindShow, dzShow)
            aspectRatioModifier:
                [1.0, 1.0, 1.0]: aspect ration modification 
            fontSize=: <float>
                10: (default) font size of the text
                
        Raises:
                
        Returns:
            bars: list(<axis.bar3d handles>)
                handles to the bars representing the buttons
            texts: list(<axis.text handles>)
                handles to the plotted text 
                    (depends on nameShow, bindShow, dzShow)
        """           
        # abstract the "graphics" values and "names" from the internal structure _K
        xs, ys, zs    = [self._K[k]['graphics']['x'] for k in self._K],  [self._K[k]['graphics']['y'] for k in self._K],  [self._K[k]['graphics']['z'] for k in self._K]
        dxs, dys, dzs = [self._K[k]['graphics']['dx'] for k in self._K], [self._K[k]['graphics']['dy'] for k in self._K], [self._K[k]['graphics']['dz'] for k in self._K]
        facecolors, edgecolors, alphas = [self._K[k]['graphics']['facecolor'] for k in self._K], [self._K[k]['graphics']['edgecolor'] for k in self._K], [self._K[k]['graphics']['alpha'] for k in self._K]
        names = [k for k in self._K]
        binds = [self._K[k]['symbol'] for k in self._K]
        # handles to be returned
        bars = []
        texts = []
        # plotting and texting
        for x,y,z,dx,dy,dz,facecolor,edgecolor,alpha,name,bind in zip(xs,ys,zs,dxs,dys,dzs,facecolors,edgecolors,alphas,names,binds):
            bars.append( axis.bar3d(x, y, z, dx, dy, dz, alpha=alpha/2, edgecolor=edgecolor, color=facecolor) )
            if(nameShow):
                if(bindShow):
                    bindingStr = " "
                    texts.append( axis.text(x+textOffset[0]+0.35 ,y+textOffset[1]+0.25,z+textOffset[2],name,       horizontalalignment='left', verticalalignment='bottom', rotation_mode='anchor', fontsize=fontSize, weight='bold' ) )
                    bindingStr = bindingStr.join(bind)
                    texts.append( axis.text(x+textOffset[0]+0.75,y+textOffset[1]+0.25,z+textOffset[2],bindingStr, horizontalalignment='left', verticalalignment='bottom', rotation_mode='anchor', fontsize=fontSize ) )
                else:
                    texts.append( axis.text(x+textOffset[0]+0.35 ,y+textOffset[1]+0.25,z+textOffset[2],name,       horizontalalignment='left', verticalalignment='bottom', rotation_mode='anchor', fontsize=fontSize, weight='bold'  ) )
            if(dzShow):
                texts.append( axis.text(x+textOffset[0]+0.75,y+textOffset[1]+0.25,z+textOffset[2],'{:.2f}'.format(dz), horizontalalignment='left', verticalalignment='bottom', rotation_mode='anchor', fontsize=fontSize ) )
        # apply default look
        if(defaultLook):
            axis.view_init(60, -30)
            axis.set_xlim([0,6])
            if(self._keyboardType=='external'):
                axis.set_ylim([0,17.75])
                axis.set_box_aspect([1*aspectRatioModifier[0],17.75/6*aspectRatioModifier[1],1*aspectRatioModifier[2]])
            else:
                axis.set_ylim([0,14.5])
                axis.set_box_aspect([1*aspectRatioModifier[0],14.5/6*aspectRatioModifier[1],1*aspectRatioModifier[2]])
            axis.grid(False)
            axis.set_xticks([])
            axis.set_yticks([])
            axis.set_zticks([])
        # return
        return bars, texts
    
    #%% Plot layout in 2D
    def plotKeyboard2D(self, axis, defaultLook=True, nameShow=True, bindShow=False, dzShow=True, textOffset=[0.0, 0.0, 0.0], fontSize=10):
        """Produce a 2D plot of the keyboard layout.
        
        Arguments:
            axis: <axis>
                A subplot axis.
            defaultLook: <bool>
                True: (default) Applies predefined settings to create 
                    a nice and easy to read plot
                False: plot bar-graph to the axis, do not apply 
                    any changes to the axis
            nameShow: <bool>
                True: (default) plot the button names
                False: button names are not plotted
            bindShow: <bool>
                True: plot bound symbols
                False: (default) do not plot bound symbols
            dzShow: <bool>
                True: (default) plot the value ['graphics', 'dz']
                False: value is not plotted
            textOffset: list(<float>, <float>, <float>)
                [0.0, 0.0, 0.0]: (default) offset to the plotted text 
                    (depends on nameShow, bindShow, dzShow)
            fontSize=: <float>
                10: (default) font size of the text
                
        Raises:
                
        Returns:
            bars: list(<patches.Rectangle handles>)
                handles to the patches (Rectangles) representing the buttons
            texts: list(<axis.text handles>)
                handles to the plotted text 
                    (depends on nameShow, bindShow, dzShow)
        """           
        # abstract the "graphics" values and "names" from the internal structure _K
        xs, ys = [self._K[k]['graphics']['x'] for k in self._K],  [self._K[k]['graphics']['y'] for k in self._K]
        dxs, dys, dzs = [self._K[k]['graphics']['dx'] for k in self._K], [self._K[k]['graphics']['dy'] for k in self._K], [self._K[k]['graphics']['dz'] for k in self._K]
        facecolors, edgecolors, alphas = [self._K[k]['graphics']['facecolor'] for k in self._K], [self._K[k]['graphics']['edgecolor'] for k in self._K], [self._K[k]['graphics']['alpha'] for k in self._K]
        names = [k for k in self._K]
        binds = [self._K[k]['symbol'] for k in self._K]
        # handles to be returned
        bars = []
        texts = []
        # plotting and texting
        for x,y,dx,dy,dz,facecolor,edgecolor,alpha,name,bind in zip(xs,ys,dxs,dys,dzs,facecolors,edgecolors,alphas,names,binds):
            bars.append( axis.add_patch( patches.Rectangle((y, x), dy, dx,linewidth=1, alpha=alpha, edgecolor=edgecolor, facecolor=facecolor) ) )
            if(nameShow):
                if(bindShow):
                    bindingStr = " "
                    texts.append( axis.text(y+textOffset[1]+0.25,x+textOffset[0]+0.35,name,       horizontalalignment='left', verticalalignment='bottom', rotation_mode='anchor', fontsize=fontSize, weight='bold' ) )
                    bindingStr = bindingStr.join(bind)
                    texts.append( axis.text(y+textOffset[1]+0.25,x+textOffset[0]+0.75,bindingStr, horizontalalignment='left', verticalalignment='bottom', rotation_mode='anchor', fontsize=fontSize, rotation=0 ) )
                else:
                    texts.append( axis.text(y+textOffset[1]+0.25,x+textOffset[0]+0.35,name,       horizontalalignment='left', verticalalignment='bottom', rotation_mode='anchor', fontsize=fontSize, weight='bold' ) )
            if(dzShow):
                texts.append( axis.text(y+textOffset[1]+0.25, x+textOffset[0]+0.75, '{:.2f}'.format(dz), horizontalalignment='left', verticalalignment='bottom', rotation_mode='anchor', fontsize=fontSize ) )
        # apply default look
        if(defaultLook):
            axis.set_ylim([0,6])
            if(self._keyboardType=='external'):
                axis.set_xlim([0,17.75])
                axis.set_box_aspect(6/17.75)
            else:
                axis.set_xlim([0,14.5])
                axis.set_box_aspect(6/14.5)
            axis.grid(False)
            axis.set_xticks([])
            axis.set_yticks([])
            # reverse the Y-axis
            axis.invert_yaxis()
        # return
        return bars, texts
    
    #%% Plot layout in 2D
    def plotButtonRelations(self, axis, relations):
        """Produce a 2D plot of the keyboard layout.
        
        Arguments:
            axis: <axis>
                A subplot axis.
            groups: <list(<list(<str>)>)>
                A list of lists, where every list includes strings, 
                referencing button names.
            relations: <dict(<float>)>
                A dictionary where the key is a tupple of button names
                (button1, button2) and the float is the value of 
                relation.
            defaultLook: <bool>
                True: (default) Applies predefined settings to create 
                    a nice and easy to read plot
                False: plot bar-graph to the axis, do not apply 
                    any changes to the axis
            facecolor: <str> or <list(<int>)>
                'blue': (default) inital value of button color
                
        Raises:
                
        Returns:
            bars: list(<patches.Rectangle handles>)
                handles to the patches (Rectangles) representing the buttons
            texts: list(<axis.text handles>)
                handles to the plotted text 
                    (depends on nameShow, bindShow, dzShow)
        """           
        for key, value in relations.items():
            buttonA = key[0]
            buttonB = key[1]
            if(not np.isnan(value[0])):
                # get the coordinates
                xA, yA = self._K[buttonA]['graphics']['x'] + (self._K[buttonA]['graphics']['dx']/2), self._K[buttonA]['graphics']['y'] + (self._K[buttonA]['graphics']['dy']/2)
                xB, yB = self._K[buttonB]['graphics']['x'] + (self._K[buttonB]['graphics']['dx']/2), self._K[buttonB]['graphics']['y'] + (self._K[buttonB]['graphics']['dy']/2)
                # coordinates depend on axis type (2D / 3D)
                if  axis.name == "3d":
                    warnings.warn('layout.plotButtonRelations(...) is currently not implemented for 3D plots.', UserWarning, stacklevel=1)
                    return
                else:
                    axis.arrow(yA, xA, yB-yA, xB-xA,  width=value[0], facecolor=value[1], head_width=value[0]*3, shape='full', length_includes_head=True, alpha=0.25)
                    
                    