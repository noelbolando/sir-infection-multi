# Multi-Infectious Virus - SIR Model #

Wandering through a land of the walking dead.
Don't mind me as I weep for what seems lost.
May we recall ourselves again.

This project explores how two viral infections spread over a susceptible population. It investigates how different susceptible populations respond to salient infections relative to the salience landscape of that population. This project was inspired by my curiosity wrapped up in a simple question: how does propoganda infect a population?

Note that this model does not explicitly look at any specific political ideologies, infectious diseases, religious groups, or otherwise pressumtive ideation. Such a claim would be a dishonor to the complexity of human behavior, socioeconomics, and epidimeology. However, analogous parallels may be drawn between this model and other patterns in society. An example of such a spread is analagous to how information propogates through populations based on an emotional appeal to political ideology. Aka: propoganda infection. 

## Project Details ##
As you'll see, there are three files in this repo:
1. 'agents.py': this file defines the properties of agents.
2. 'app.py': using Solara, this file defines an interactive visualization tool so that users can toggle different agent properties to see how quickly infection spreads and if/how recovery occurs accross the population.
3. 'model.py': this file defines the model itself and sets initial values for the properties of agents. 

## How to Use ##
This is pretty simple for those new to Python:
1. Clone all three files in this project.
2. Make sure all your packages are installed. Especially:
```` $ pip install enum ````
```` $ pip install mesa ````
```` $ pip install networkx ````
```` $ pip install solara ````
3. To run the app, key in the following command to your terminal:
```` $ solara run app.py````
and watch a population of susceptible agents descend into a reality infected by empty-promises.

Remember to be brave and question everything.
