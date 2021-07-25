# -*- coding: utf-8 -*-
""" MagPie-ML Tutorial PART 3
        @author: Martin Garaj
        #tested with: 
            Windows 10, Spyder 3.3.6, Python 3.7
        #version: 1.0
    
    (Please, read Tutorila part 1 and 2 first)
    
    In this brief tutorial we will analyse our typing habbits 
    and uncover possible biases and indicators of mental health 
    from the logged data. 
    
    The analytics object introduced here provides useful functions to 
    parse the linear data from the logger and provide them multitude
    of formats that are necessary to perform analysis.
    
    The analysis is partially visualized using the layout object while
    the analysis object 
    
    
    We will visualize the logged keystrokes from the logger and 
    such the visualize the average period for which the key is pressed. 
    If the brain hemispheres are equally concentrated, 
    then we press the keys for a similar amout of time, 
    no matter whether we use right or left hand.
        A bad mood though, can reveal that fingers on one hand 
    are less certain and keep the buttons pressed for longer, 
    relative to the other hand.
        Further, we will observe, whether words, which require input 
    from both left and right hand (e.g. word "alert" is usually typed 
    a-left, l-right, e-left, r-left, t-left, so that there are 
    left->right transitions for a->l and right-left transitions l->e).
        We will use magpie for visualization, but also to transform 
    the data to proper machine learning formats, to create our own 
    typyng models (e.g. a ML model that will imitate the way we type).
"""


#%% Imports
import magpie_ml as mp

import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib.gridspec import GridSpec
import numpy as np


#%% User defined paramters
#   There are certain parameters which are unique from user-to-user
#   and therefore we will define them below and explain their purpose,
#   such that the user can tune them according to interest
maxTransitionPeriod = 1.500 # in [seconds], the maximum amount of time, 
#    for which we consider the pause between button presses to be 
#   relevant to our typing speed (e.g. if we take a deep breath from 
#   time to time for 1 [second] and stop typing, we dont want to count 
#   this to our regular typing speed)
minTransitionPeriod = 1.000 # in [seconds], the minimum amount of time 
#   for a successive transition from a button to button 
#   (e.g. we want to find a finger that takes the longest to press 
#   a button when we transition from one side of the keyboard to the 
#   other, then we want to exclude fast typing fingers and identify 
#   those that are slower)



#%% Get layout
#   Layout object object represents our keyboard. 
layout = mp.layout(keyboardType='external', language='englishUS', qwerty=True, shift_l_long=True, enter_tall=True)
# lets change some basic properties, such as color, alpha channel and height "dz"
#   'dz" will represent our data in 3D, therefore lets set it to 0.0
layout.setButtonValue(layout.allButtons,          ['graphics', 'facecolor'], 'white')
layout.setButtonValue(layout.allButtons,          ['graphics', 'alpha'],     0.3)
layout.setButtonValue(layout.allButtons,          ['graphics', 'dz'], 0.0)

# define a subset of buttons which we want to analyze
buttonAnalysis = layout.alphabetButtons + layout.punctuationButtons + ['9'] + ['0']



#%% Get analytics
#   Analytics object parses the data logged in a text file. 
#   Lets get the data of all the symbols present on our keyboard.
analytics = mp.analytics( layout.getSymbolList(), path='loggedData.txt' )



#%% Get timing information
#   Since the logger logs the time when the button is pressed and 
#   released, we can get precise timing for events (press/release) of 
#   every button, as well as the duration of how long the button 
#   is pressed.
timePress, timeRelease, timeDuration = analytics.getTiming(buttonAnalysis)

#   Calculate the mean duraition of every button being pressed.
timeDurMean = {}
#   Loop through a dictionary which holds durations of presses.  
for button, value in timeDuration.items():
    #   If there is NaN only, then button was not pressed at all.
    if(np.isnan(value).all()):
        timeDurMean[button] = 0.0
    else:
        timeDurMean[button] =  np.nanmean(timeDuration[button])

#   Use a color map to better visually represent the duration.
cmap = get_cmap('viridis')
#   Also, we normalize the mean duration to interval [0, 1] so we have 
#   simple way to obtain a color from a color map. This requires to 
#   know the maximum value.
maxTimeDurMean = max(timeDurMean.values()) 



#%% Plot the duration using the layout of our keyboard.
#   Now we want the plot of the layout to represent our data, 
#   that is the mean duration for which the button is pressed. 
#   We will represent the data both by color and by the height 
#   of the button (parameter "dz" in 3D)
for button, value in timeDurMean.items():
    #    Get [R,G,B] channel only, alpha channel is set separately
    try:
        rgb = cmap(value/maxTimeDurMean)[0:3] 
    except  ZeroDivisionError:
        rgb = cmap(0.0)[0:3]
    layout.setButtonValue([button], ['graphics','facecolor'], rgb)
    layout.setButtonValue([button], ['graphics','dz'], value*1000) #    multiplied by 1000 to go from [s] to [ms]
    
#   Close all previous figures    
plt.close('all')

#   Get a figure and subplots
fig = plt.figure()

gs = GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[:, 1], projection='3d', proj_type = 'ortho')


#   Now we use layout methods to give us the plots in 2D and 3D
layout.plotKeyboard2D(ax1, defaultLook=True, nameShow=True, bindShow=False, dzShow=True, textOffset=[0.0, 0.0, 0.0], fontSize = 8)
ax1.set_title('Mean time of press [ms] + Transition from right to left longer than '+str(minTransitionPeriod)+' [s] but shorten than ' + str(maxTransitionPeriod) + ' [s]')
layout.plotKeyboard2D(ax2, defaultLook=True, nameShow=True, bindShow=False, dzShow=True, textOffset=[0.0, 0.0, 0.0], fontSize = 8)
ax2.set_title('Mean time of press [ms] + Transition from left to right longer than '+str(minTransitionPeriod)+' [s] but shorten than ' + str(maxTransitionPeriod) + ' [s]')
layout.plotKeyboard3D(ax3, defaultLook=True, nameShow=True, bindShow=False, dzShow=True, textOffset=[0.0, 0.0, 0.0], aspectRatioModifier=[1.0, 1.0, 1.0], fontSize=8)
ax3.set_title('Mean time of press [ms] visualized in 3D')
fig.tight_layout()
plt.show()



#%% Chronological timing analyses
#   Lets start by obtaining a chronological order of the button presses
#   and releases as a chronological lists.
chronListPress, chronListRelease = analytics.getChronologicalTiming(buttonAnalysis)

#   Now we want to learn, how the brain processes the transition from 
#   one button to another.Therefore, we want to visualize the relation 
#   of button1 -> button2. To simplify the notation, 
#   we will borrow a notation from conditional probability distribution 
#   p(X|Y) (read as probability of value X, given value Y). 
#   In our case, will use F('A'|'B'), where the value returned by 
#   the function F() is:
#       a) mean time of transition
#       b) covariance of time transition
#       c) total number of transitions in our logged file
Mmean, Mcov, Mcount = analytics.getTimeCorrelationOcccuranceMatrix(chronListPress, timeLimit=maxTransitionPeriod, buttons=buttonAnalysis)
#   The data are represented as matrices, since it is the most natural 
#   way of representing such relations. This matrix is also known as 
#   Adjecency matrix in graph theory.

#   Lets see the matrices right away to understand them.
fig, ax4 = plt.subplots()
analytics.plotMatrixHeatmap(ax4, Mmean, buttonAnalysis, defaultLook=True, fontSize=6)
ax4.set_title('Matrix of mean-press-time (maxTransitionPeriod = '+str(maxTransitionPeriod)+' [s])')
ax4.set_ylabel("pressed button")
ax4.set_xlabel("preceeding button")
plt.show()

fig, ax5 = plt.subplots()
analytics.plotMatrixHeatmap(ax5, np.sqrt(Mcov), buttonAnalysis, defaultLook=True, fontSize=6)
ax5.set_title('Matrix of SQRT(covariance-press-time) (maxTransitionPeriod = '+str(maxTransitionPeriod)+' [s])')
ax5.set_ylabel("pressed button")
ax5.set_xlabel("preceeding button")
plt.show()

fig, ax6 = plt.subplots()
analytics.plotMatrixHeatmap(ax6, Mcount, buttonAnalysis, defaultLook=True, fontSize=6)
ax6.set_title('Key-stroke-count matrix (maxTransitionPeriod = '+str(maxTransitionPeriod)+' [s])')
ax6.set_ylabel("pressed button")
ax6.set_xlabel("preceeding button")
plt.show()

### Lets wisualize the matrix Mmean in a bit different way, using 2D layout.
#   Lets change the hard-to-read matrix into a dictionary of relations. 
#   The dictionary will take the buttons, and store the relation 
#   in between the buttons. In this case, the relation is the mean 
#   time of transition from one button to another.
meanTransitionLeftGivenRight = {}
for r in range(len(buttonAnalysis)):
    for l in range(len(buttonAnalysis)):
        buttonR, buttonL = buttonAnalysis[r], buttonAnalysis[l]
        if ( buttonR in layout.rightHandButtons and buttonL in layout.leftHandButtons ):
            lineColor = 'black'
            if(Mmean[l, r] > minTransitionPeriod):
                normalizedValue = ( Mmean[l, r]- minTransitionPeriod )/maxTransitionPeriod
                lineWidth = (normalizedValue+0.1)/2
                meanTransitionLeftGivenRight[buttonR, buttonL] = ( lineWidth, lineColor )
            else:
                meanTransitionLeftGivenRight[buttonR, buttonL] = ( np.nan, lineColor )
            
meanTransitionRightGivenLeft = {}
for r in range(len(buttonAnalysis)):
    for l in range(len(buttonAnalysis)):
        buttonR, buttonL = buttonAnalysis[r], buttonAnalysis[l]
        if ( buttonR in layout.rightHandButtons and buttonL in layout.leftHandButtons ):
            lineColor = 'black'
            if(Mmean[r, l] > minTransitionPeriod):
                normalizedValue = ( Mmean[r, l]- minTransitionPeriod )/maxTransitionPeriod
                lineWidth = (normalizedValue+0.1)/3
                meanTransitionRightGivenLeft[buttonL, buttonR] = ( lineWidth , lineColor )
            else:
                meanTransitionRightGivenLeft[buttonL, buttonR] = ( np.nan, lineColor )
            
#   Add to the 2D layout - ax1
layout.plotButtonRelations(ax1, meanTransitionLeftGivenRight)
#   Add to the 2D layout - ax2
layout.plotButtonRelations(ax2, meanTransitionRightGivenLeft)

