# Multi-Infectious Virus - SIR Model #
This project explores how multiple viruses spread over various susceptible populations.

As assumption I make with this model:
We have two distinct susceptible states, two distinct infection states, and two possible recovery states.

This project investigates how different suceptible populations respond to salient infections. One population is more susceptible to one disease than another and vice versa. 

Note that this model does not explicitly look at any specific infectious disease spread although analogous parallels may be drawn between the two (patterns, amiright?)
An example of such a spread is analagous to how information propogates through populations based on an emotional appeal to political ideology.

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
and have fun playing with the webpage tool.

Be brave and question everything.
