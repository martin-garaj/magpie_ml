# magpie_ml
Key stroke logger, visualization and analysis.

@author: Martin Garaj

# **Introduction**

*Magpie_ml* package is a product of Covid quarantine and its effect on mental health (typing timing characteristics, typing biases between right and left hand, and more). The main purpose is to observe changes that occur when we interract with a PC through a keyboard under stresfull situations. *Magpie_ml* package offers detailed key **logger**, keyboard **layout** to visualize the gathered data and **analytics** to produce data useful for machine learning applications (key-stroke timing information, adjacency matrix of sequential key presses, and more).


# **Tutorials**
Magpie-ml comes with 3 tutorials to lower the learning curve and let you copy-paste already tested code.


## *Tutorial part 1*

Here we show how to create and adjust the **layout** object to establist a proper representation of the physical keyboard. Since there is no unified way of representing keyboard presses at the Operating System (OS) level, the **layout** object creates a symbol-to-button map and visualize the keyboard layout as seen below.

![https://github.com/martin3366/magpie_ml/raw/main/images/layout_illustration.png](https://github.com/martin3366/magpie_ml/raw/main/images/layout_illustration.png)
*Left: different layout options, Right: binding and rebind of symbols to buttons*

For the purpose of analyzing the coordination between fingers, the following default mapping to fingers is included in the **layout** object.

![https://github.com/martin3366/magpie_ml/raw/main/images/layout_illustration_fingers.png](https://github.com/martin3366/magpie_ml/raw/main/images/layout_illustration_fingers.png)
*Buttons assigned to fingers across the keyboard*


## *Tutorial part 2*

The most important part in machine learning are data. In the part 2 we show how to start a logger that logs detailed data of key strokes data into a local file. The tutorial also shows the console output if **logger** object is initialized with *debug=True*, the output looks as follows:

![https://github.com/martin3366/magpie_ml/raw/main/images/logger_console.png](https://github.com/martin3366/magpie_ml/raw/main/images/logger_console.png)
*Console output when running logger with debug options*


## *Tutorial part 3*

Visualization and analysis are crucial in understanding patterns. Therefore, the part 3 shows the various ways to use the **analytics** object together with **layout** object to visualize the logged data using the **logger** object.

The **analytics** object provides methods to obtain timing information, such as duration of button press, transistion times from a button to button and others. For illustration the following figures show matrices of sample data from *loggedData.txt*.

![https://github.com/martin3366/magpie_ml/raw/main/images/matrix_count.png](https://github.com/martin3366/magpie_ml/raw/main/images/matrix_count.png)
*Adjacency matrix of total number of key presses of button1 given button2*

![https://github.com/martin3366/magpie_ml/raw/main/images/matrix_mean_time.png](https://github.com/martin3366/magpie_ml/raw/main/images/matrix_mean_time.png)
*Adjacency matrix of mean transition time from button1 to button2*

![https://github.com/martin3366/magpie_ml/raw/main/images/matrix_cov_time.png](https://github.com/martin3366/magpie_ml/raw/main/images/matrix_cov_time.png)
*Adjacency matrix of SQRT(covariance) of transition time from button1 to button2*

The **layout** object can help to visualize quantities related ti both: a) single button, b) a transition from button to button (adjacency matrices produced by **analytics**). The **layout** can plot these data in 2D and 3D. The data related to transitions (adjacency matrices) are visualized by arrows.

![https://github.com/martin3366/magpie_ml/raw/main/images/layout_timing.png](https://github.com/martin3366/magpie_ml/raw/main/images/layout_timing.png)
*Mean press time per button + longest transistions from left to right hand and vice-versa*


# **Conslusion**

I welcome feedback and new ideas. I hope this project can reveal your typing habbits and even typing changes due to these difficult times.


