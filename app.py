"""
This file instantiates a web page using Solara.
This makes it possible to interact with the model and display some cool visualizations.

To initialize the app:
    solara run app.py
"""

import math
from mesa.visualization import Slider, SolaraViz, make_plot_component, make_space_component
import solara

from model import State, VirusOnNetwork

# Define how the agents are portrayed.
def agent_portrayal(agent):
    node_color_dict = {
        State.R_INFECTED: "tab:red",
        State.R_SUSCEPTIBLE: "tab:green",
        State.R_RESISTANT: "tab:gray",

        State.L_INFECTED: "tab:blue",
        State.L_SUSCEPTIBLE: "tab:green",
        State.L_RESISTANT: "tab:gray"
    }
    return {"color": node_color_dict[agent.state], "size": 100}

# Define how the model parameters will be displayed.
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed"
    },
    "num_nodes": Slider(
        label="Number of Agents",
        value=20,
        min=10,
        max=50,
        step=1
    ),
    "avg_node_degree": Slider(
        label="Avg Node Degree",
        value=3,
        min=3,
        max=8,
        step=1
    ),
    "initial_r_outbreak_size": Slider(
        label="Initial R Outbreak Size",
        value=1,
        min=1,
        max=10,
        step=1
    ),
    "initial_l_outbreak_size": Slider(
        label="Initial L Outbreak Size",
        value=1,
        min=1,
        max=10,
        step=1
    ),
    "virus_r_spread_chance": Slider(
        label="R Infection Rate",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "virus_l_spread_chance": Slider(
        label="L Infection Rate",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "virus_check_r_frequency": Slider(
        label="R Virus Check Frequency",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "virus_check_l_frequency": Slider(
        label="L Virus Check Frequency",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "r_recovery_chance": Slider(
        label="R Chance of Recovery",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "l_recovery_chance": Slider(
        label="L Chance of Recovery",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "gain_resistance_chance": Slider(
        label="Chance of Gaining Resistance",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
}

# Setup for the model process visualization.
def post_process_lineplot(ax):
    ax.set_ylim(ymin=0)
    ax.set_ylabel("Number of Agents")
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

SpacePlot = make_space_component(agent_portrayal)
StatePlot = make_plot_component(
    {"R Infected": "tab:red", 
     "R Susceptible": "tab:green", 
     "R Resistant": "tab:gray",
     "L Infected": "tab:blue", 
     "L Susceptible": "tab:green", 
     "L Resistant": "tab:gray"},
    post_process=post_process_lineplot
)

model1 = VirusOnNetwork()

# Setting up the web page
page = SolaraViz(
    model1,
    components=[
        SpacePlot,
        StatePlot
    ],
    model_params=model_params,
    name="SIR Multi-Virus Model"
)

# Initializing an instance of the web page
page 
