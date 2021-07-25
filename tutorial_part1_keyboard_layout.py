# -*- coding: utf-8 -*-
""" MagPie-ML Tutorial PART 1
        @author: Martin Garaj
        #tested with: 
            Windows 10, Spyder 3.3.6, Python 3.7
        #version: 1.0
    
    In this brief tutorial we will setup keyboard layout object 
    which represents the physical keyboard we use for typing.
    Furthemrnore, we will adjust the symbol-to-button mapping, which 
    is crucial for proper function of the key logger (Tutotial part 2).
"""

#%% Imports
import magpie_ml as mp

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec



#%% Lets start with 2 predefined keyboard layouts
#   There are several parameters to adjust the layout such that it 
#   matches the layout of our physical keyboard.
#   Lets create and plot 2 layouts with different parameters:
layout1 = mp.layout( keyboardType='external', language='englishUS', qwerty=True,  shift_l_long=True,  enter_tall=True  )
layout2 = mp.layout( keyboardType='builtin',  language='englishUK', qwerty=False, shift_l_long=False, enter_tall=False ) 

#   Highlight the differences between buttons (we will discuss this later)
#   Highlight the "keyboardType" parameter
layout1.setButtonValue(layout1.extendedButtons, ['graphics','facecolor'], 'black')
layout2.setButtonValue(layout2.extendedButtons, ['graphics','facecolor'], 'black')
#   Highlight the "qwerty" parameter
layout1.setButtonValue(['Z'],                   ['graphics','facecolor'], 'red'  )
layout2.setButtonValue(['Z'],                   ['graphics','facecolor'], 'red'  )
#   Highlight the "shift_l_long" parameter
layout1.setButtonValue(['Shift_l'],             ['graphics','facecolor'], 'green')
layout2.setButtonValue(['Shift_l'],             ['graphics','facecolor'], 'green')
layout2.setButtonValue(['s10'],                 ['graphics','facecolor'], 'green')
#   Highlight the "enter_tall" parameter
layout1.setButtonValue(['Enter'],               ['graphics','facecolor'], 'yellow')
layout2.setButtonValue(['s6'],                  ['graphics','facecolor'], 'yellow')
layout2.setButtonValue(['Enter'],               ['graphics','facecolor'], 'yellow')
layout2.setButtonValue(['s6'],                  ['graphics','facecolor'], 'yellow')



#   Lets plot the layouts as subplots
plt.close('all')
fig = plt.figure(constrained_layout=True)
gs = GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[1,0])
ax3 = fig.add_subplot(gs[0,1])
ax4 = fig.add_subplot(gs[1,1])

#   Visualize the 2 layouts to see the differences
layout1.plotKeyboard2D(ax1, defaultLook=True, nameShow=True, bindShow=True, dzShow=False, textOffset=[0.0, 0.0, 0.0], fontSize = 8)
ax1.set_title('Parameters: keyboardType=\'external\', language=\'englishUS\', qwerty=True,  shift_l_long=True,  enter_tall=True')
ax1.set_ylabel('layout1')
layout2.plotKeyboard2D(ax2, defaultLook=True, nameShow=True, bindShow=True, dzShow=False, textOffset=[0.0, 0.0, 0.0], fontSize = 8)
ax2.set_title('Parameters: keyboardType=\'builtin\',  language=\'englishUK\', qwerty=False, shift_l_long=False, enter_tall=False')
ax2.set_ylabel('layout2')



### Lets change symbol-to-button mupping
#   Changing this mapping is crucial in case we are using different laguage or 
#   there is a specific symbol not found on English US or UK keyboard.
#   For instance, the symbol 'ä' is not part of aforementioned keyboards, but 
#   we want the logger to catch it. Now, notice, it doesn't matter whether 
#   the symbol is input as Alt+a, or Ctrl+a, or is mapped to button 'A' 
#   directly. For all the above cases, the symbol 'ä' is mapped to button 'A'.
layout1.bindSymbolToButton('ä', 'A')
#   Now lets rebind some other symbol, which is already bout to existing 
#   button, such as '?' to 's6'
layout2.unbindSymbolFromButton('?', 's9')
layout2.bindSymbolToButton('?', 's6')


# Highlioght the changes
layout1.setButtonValue(layout1.allButtons, ['graphics','facecolor'], 'blue')
layout1.setButtonValue(['A'], ['graphics','facecolor'], 'red')
layout2.setButtonValue(layout2.allButtons, ['graphics','facecolor'], 'blue')
layout2.setButtonValue(['s6', 's9'], ['graphics','facecolor'], 'red')

#   Visualize the 2 layouts to see the differences
layout1.plotKeyboard2D(ax3, defaultLook=True, nameShow=True, bindShow=True, dzShow=False, textOffset=[0.0, 0.0, 0.0], fontSize = 8)
ax3.set_title('Binding: symbol \'ä\' bound to button \'A\'')
ax3.set_ylabel('layout1')
layout2.plotKeyboard2D(ax4, defaultLook=True, nameShow=True, bindShow=True, dzShow=False, textOffset=[0.0, 0.0, 0.0], fontSize = 8)
ax4.set_title('Rebinding: symbol \'?\' unbound from \'s9\' and bound to \'s6\'')
# plot a relation between the buttons
layout2.plotButtonRelations(ax4, { ('s9','s6'): ( 0.1 , 'black') } )
ax4.set_ylabel('layout2')



### Lets explore the layout class a bit more
layout3 = mp.layout( keyboardType='external',  language='englishUK', qwerty=True, shift_l_long=True, enter_tall=True ) 
layout3.setButtonValue(layout3.allButtons, ['graphics','facecolor'], 'black')
layout3.setButtonValue(layout3.allButtons, ['graphics','alpha'], 0.1)
layout3.setButtonValue(layout3.rightHandButtons+layout3.leftHandButtons, ['graphics','alpha'], 0.3)

layout3.setButtonValue(layout3.finger1Buttons, ['graphics','facecolor'], 'yellow')
layout3.setButtonValue(layout3.finger2Buttons, ['graphics','facecolor'], 'green')
layout3.setButtonValue(layout3.finger3Buttons, ['graphics','facecolor'], 'blue')
layout3.setButtonValue(layout3.finger4Buttons, ['graphics','facecolor'], 'red')
layout3.setButtonValue(layout3.finger7Buttons, ['graphics','facecolor'], 'orange')
layout3.setButtonValue(layout3.finger8Buttons, ['graphics','facecolor'], 'purple')
layout3.setButtonValue(layout3.finger9Buttons, ['graphics','facecolor'], 'brown')
layout3.setButtonValue(layout3.finger10Buttons, ['graphics','facecolor'], 'black')


fig = plt.figure()
gs = GridSpec(1, 1, figure=fig)
ax5 = fig.add_subplot(gs[0, 0])

layout3.plotKeyboard2D(ax5, defaultLook=True, nameShow=True, bindShow=False, dzShow=False, textOffset=[0.0, 0.0, 0.0], fontSize = 8)
ax5.set_title('Illustration of predefined sets of buttons bound to specific fingers')