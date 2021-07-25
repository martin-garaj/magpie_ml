# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 19:35:19 2020

@author: Martin
"""

#%% Imports - analytics
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ANALYTICS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class analytics:
    """A class to represent analysis of log file.

    Analytics class merges the analysis of the log file. 
    The main purpose is to parse the log file and extract 
    useful timing information, while handling possible 
    missing data (NaNs).

    Attributes:

    Methods:
        analytics(buttons, path='loggedData.txt')
        getTiming(buttons=buttons)
        getChronologicalTiming(buttons=buttons)
        getChronOccuranceyMatrix(eventList, buttons=buttons)
        plotMatrixHeatmap(ax, matrix, buttons, defaultLook=True)
        
    """
    def __init__(self, buttons, path='loggedData.txt'):
        # read data
        self._df = pd.read_csv(path, delimiter='\t')
#        self._df['Time']   = self._df['Time'].astype(float)
        self._df['Key']    = self._df['Key'].str.strip()
        self._df['Button'] = self._df['Button'].str.strip()
#        self._df['Event']  = self._df['Event'].astype(int)
        
        # check appended data (every appended data start by headline "Time	Key	Button	Event")
        appendEvents = self._df.loc[(self._df['Time'] == 'Time')]
        # get last line
        lastLineIdx = self._df.tail(1).index[0]
        
        # change the headers to appropriate types (int, float) so that we can do mathematical operations over them
        for idx in appendEvents.index:
            self._df['Time'][idx] = 0.0
            self._df['Event'][idx] = 0
        self._df['Time']   = self._df['Time'].astype(float)
        self._df['Event']  = self._df['Event'].astype(int)            
            
        for idx, val in enumerate(appendEvents.index):
            if(val != appendEvents.index[-1]): # not last
                timeAdd = self._df['Time'][val - 1] # get time from preceding line
                timeAdd = timeAdd + 60 # add extra 1 minute
                # add time 
                self._df['Time'][val+1:appendEvents.index[idx+1]] = self._df['Time'][val+1:appendEvents.index[idx+1]] + timeAdd
            else:
                timeAdd = self._df['Time'][val - 1] # get time from preceding line
                timeAdd += 60 # add extra 1 minute
                # add time 
                self._df['Time'][val+1:lastLineIdx+1] = self._df['Time'][val+1:lastLineIdx+1] + timeAdd
                
        # drop header lines
        self._df = self._df.drop(appendEvents.index.values)

        # get all symbols recognized by keyboardLayout
        self._buttons = buttons
        
    #%% get timing of button presses, releases and press duration
    def getTiming(self, buttons=[]):
        """Get chronological list of events for given buttons
        
        Arguments:
            buttons: list(<str>)
                buttons: (default) list of buttons
                    
        Returns:
            timeIn: dict(<button>: [<time>])
                dictionary of buttons with list of key press times
            timeOut: dict(<button>: [<time>])
                dictionary of buttons with list of key release times
            timeDur: dict(<button>: [<period>])
                dictionary of buttons with list of press period [s] 
            
        Raises:
        """
        if(len(buttons)==0):
            buttons = self._buttons
        # get the maximum count of events for every button (from event counter)
        maxCounter = {}
        for button in buttons:
            tempRows = self._df.loc[(self._df['Button'] == button)]
            if(len(tempRows['Event']>0)):
                maxCounter[button] = max(abs(tempRows['Event']))
            else:
                maxCounter[button] = 0
        # initialize dictionaries with "buttons" as keys and empty list() as values
        timeIn  = {}
        timeOut = {}
        timeDur = {}
        for button in buttons: 
            timeIn[button]     = np.empty(maxCounter[button])
            timeIn[button][:]  = np.nan
            timeOut[button]    = np.empty(maxCounter[button])
            timeOut[button][:] = np.nan
            timeDur[button]    = np.empty(maxCounter[button])
            timeDur[button][:] = np.nan
        # fill-in 
        for time, key, button, event in zip( self._df['Time'], self._df['Key'], self._df['Button'], self._df['Event'] ):
            if(button in buttons):
                # decode event
                eventType  = np.sign(event)
                eventCount = abs(event)-1
                # Press event
                if(eventType>=0):
                    timeIn[button][eventCount] = time
                # Release event            
                elif(eventType<0): 
                    timeOut[button][eventCount] = time
        for button in buttons:
            for tPress, tRelease in zip(timeIn[button], timeOut[button]):
                timeDur[button] = np.subtract(timeOut[button], timeIn[button])
        return timeIn, timeOut, timeDur
    
    #%% get chronological list of pressed buttons
    def getChronologicalTiming(self, buttons=[]):
        """Get chronological list of events for given buttons
        
        Arguments:
            buttons: list(<str>)
                buttons: (default) list of buttons
                    
        Returns:
            chronologicalListIn: list(<str>)
                chronological list of button presses
            chronologicalListOut: list(<str>)
                chronological list of button releases
            
        Raises:
            Exception: The log file is wrongly parsed.
        """
        # buttons=[]     make default value self._buttons
        if(len(buttons)==0):
            buttons = self._buttons
        # lists of chronological events
        chronologicalListIn  = []
        chronologicalListOut = []
        # parse the file
        for time, key, button, event in zip( self._df['Time'], self._df['Key'], self._df['Button'], self._df['Event'] ):
            # check if button is in the requested list
            if(button in buttons):
                # decode event
                eventType  = np.sign(event)
                eventCount = abs(event)-1
                # add to the list
                if(eventType>=0):
                    chronologicalListIn.append([time, key, button, eventCount])
                elif(eventType<0):
                    chronologicalListOut.append([time, key, button, eventCount])
                    
        # check if lists are chronological
        for idx in range(0, len(chronologicalListIn)-1):
            if(chronologicalListIn[idx]>chronologicalListIn[idx+1]):
                raise Exception("layout.getChronologicalTiming(..): "'Time'" is not purely ascending in chronologicalListIn at "+str(chronologicalListIn[idx])+" ")
        for idx in range(0, len(chronologicalListOut)-1):
            if(chronologicalListOut[idx]>chronologicalListOut[idx+1]):
                raise Exception("layout.getChronologicalTiming(..): "'Time'" is not purely ascending in chronologicalListIn at "+str(chronologicalListOut[idx])+" ")
                
        return chronologicalListIn, chronologicalListOut
    
    # #%% occurance matrix
    # def getChronOccuranceyMatrix(self, eventList, buttons=[]):
    #     """Calculate occurance matrix of given buttons
        
    #     Arguments:
    #         eventList: list([time, symbol, button, event], ...)
    #             List of parsed events from the log file
    #         buttons: list(<str>)
    #             buttons: (default) list of buttons
                    
    #     Returns:
    #         <matrix>
    #             Matrix with occurances f(Y|X), where X is a button on x-axis 
    #             and preceedes the press of button Y on y-axis
            
    #     Raises:
    #     """
    #     # buttons=[] make default value self._buttons
    #     if(len(buttons)==0):
    #         buttons = self._buttons
    #     # matrix size
    #     mSize = len(buttons)
    #     # matrix
    #     MchronOccur = np.zeros((mSize,mSize))
    #     # loop through eventList and fill in the matrix MchronOccur
    #     prevIter = iter(eventList)
    #     prevEvent = next(prevIter)
    #     for event in eventList:
    #         eventTime, eventTKey, eventButton, eventCount = event
    #         if(eventButton in buttons):
    #             prevEventButton = prevEvent[2]
    #             mX = buttons.index(eventButton)
    #             mY = buttons.index(prevEventButton)
    #             MchronOccur[mX][mY] += 1 # increment count of p(eventButton|prevEventButton) probability
    #             # set the previous event
    #             prevEvent = event
    #     return MchronOccur
    
    #%% occurance matrix with time limit
    def getTimeCorrelationOcccuranceMatrix(self, eventList, timeLimit, buttons=[]):
        """Calculate time correletaion of occurance matrix of given buttons
        
        Arguments:
            eventList: list([time, symbol, button, event], ...)
                List of parsed events from the log file
            timeLimit: <float>
                A time limit beyond which the entry is considered outlier and 
                left out.
            buttons: list(<str>)
                buttons: (default) list of buttons
                    
        Returns:
            <matrix>
                Matrix with mean time of occurances f(Y|X), 
                where X is a button on x-axis and preceedes 
                the press of button Y on y-axis
            <matrix>
                Matrix with covariance time of occurances f(Y|X), 
                where X is a button on x-axis and preceedes 
                the press of button Y on y-axis
            <matrix>
                Matrix with occurances f(Y|X), where X is a button on x-axis 
                and preceedes the press of button Y on y-axis
            
        Raises:
        """
        # buttons=[] make default value self._buttons
        if(len(buttons)==0):
            buttons = self._buttons
        # matrix size
        mSize = len(buttons)
        # matrices storing results
        _meanM = np.zeros((mSize, mSize))
        _corrM = np.zeros((mSize, mSize))
        _countM = np.zeros((mSize, mSize))
        # get buffers storing values to calculate _mean and _corr
        _buffer={}
        for x in range(0, mSize):
            for y in range(0, mSize):
                _buffer[(x,y)] = []
        # parse the data in the eventList
        prevIter = iter(eventList)
        prevEvent = next(prevIter)
        # for every event
        for event in eventList:
            eventTime, eventKey, eventButton, eventCount = event
            # for every button
            if(eventButton in buttons):
                # get the button name and time
                prevEventButton = prevEvent[2]
                prevEventTime = prevEvent[0]
                # get indices within the matrix
                mX = buttons.index(eventButton)
                mY = buttons.index(prevEventButton)
                # calculate period of time between events
                period = eventTime - prevEventTime
                # if the pause is not too great (elss than timeLimit), then count the values
                if(period <= timeLimit):
                    # append period to the list of f(x|y)
                    _buffer[(mX,mY)].append(period)
                    # keep total count in matrix
                    _countM[mX][mY] += 1
                # set the previous event
                prevEvent = event
                
        for k in _buffer.keys():
            # key "k" is a tupple of coordinates
            mX = k[0]
            mY = k[1]
            _meanM[mX][mY] = np.mean(_buffer[(mX,mY)])
            if(not _buffer[(mX,mY)] ):
                _corrM[mX][mY] = np.nan
#                print(_buffer[(mX,mY)])
            else:
                _corrM[mX][mY] = float( np.cov( _buffer[(mX,mY)] ) )
            
        return _meanM , _corrM , _countM
    
    #%% plot heat map of a matrix
    def plotMatrixHeatmap(self, axis, matrix, matrixLabels, defaultLook=True, fontSize=10):
        """Plot a heatmap of a matrix
        
        Arguments:
            axis: <axis>
                matplotlib handle to subplot axis.
            matrix: [[<float>, <float>, ...],[<float>, <float>, ...]]
                2D matrix of values to he plotted as heatmap
            matrixLabels: list(<str>)
                list of strings used as labels for ticks along the axes
            defaultLook: <bool>
                True: (default) apply axis labels and plot values
                False: just plot the heatmap
            fontSize: <int>
                10: (default) size of plotted text if defaultLook==True
                    
        Returns:
            <axis.imshow handle>
                handle to the plot
            
        Raises:
        """
        im = axis.imshow(matrix)
        axis.set_xticks(np.arange(len(matrixLabels)))
        axis.set_yticks(np.arange(len(matrixLabels)))
        axis.set_xticklabels(matrixLabels)
        axis.set_yticklabels(matrixLabels)
        if(defaultLook):
            # Rotate the tick labels and set their alignment.
            plt.setp(axis.get_xticklabels(), rotation=0, ha="right", rotation_mode="anchor")
            
            # add the text, but adjust formatting according to numbers being plotted (decimal or whole)
            maxNumber = np.max(np.absolute(matrix))
            if(maxNumber > 9.9):
                # plot whole numbers
                for i in range(len(matrixLabels)):
                    for j in range(len(matrixLabels)):
                        axis.text(j, i, int(matrix[i, j]), ha="center", va="center", color="w", fontsize=fontSize)
            else:
                # plot floats
                for i in range(len(matrixLabels)):
                    for j in range(len(matrixLabels)):
                        axis.text(j, i, '{:.2f}'.format(matrix[i, j]), ha="center", va="center", color="w", fontsize=fontSize)
            # set labels
            axis.set_title("value of  f(x)|y (e.g. probability p(X|Y))")
            axis.set_xlabel("f(Y)")
            axis.set_ylabel("f(X)")
        return im