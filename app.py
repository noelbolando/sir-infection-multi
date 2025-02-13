"""
This file instantiates a web page using Solara.
This makes it possible to interact with the model and display some cool visualizations.

To initialize the app:
    solara run app.py
"""

from mesa.visualization import Slider, SolaraViz, make_plot_component, make_space_component
import solara

from model import State, VirusOnNetwork

# Define how the agents are portrayed.
def agent_portrayal(agent):
    node_color_dict = {
        State.INFECTED_GOP: "tab:red",
        State.INFECTED_DEM: "tab:blue",
        State.SUSCEPTIBLE: "tab:green",
        State.RESISTANT: "tab:gray"
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
        label="Population Size",
        value=10,
        min=10,
        max=50,
        step=1
    ),
    "avg_node_degree": Slider(
        label="Level of Agent Socialization",
        value=3,
        min=3,
        max=8,
        step=1
    ),
    "gop_initial_outbreak_size": Slider(
        label="Number of GOP Propoganda Agents",
        value=1,
        min=1,
        max=10,
        step=1
    ),
    "dem_initial_outbreak_size": Slider(
        label="Number of Dem Propoganda Agents",
        value=1,
        min=1,
        max=10,
        step=1
    ),
    "gop_virus_spread_chance": Slider(
        label="GOP Propogranda Infection Rate",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "dem_virus_spread_chance": Slider(
        label="Dem Propogranda Infection Rate",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "virus_check_frequency": Slider(
        label="Virus Checker",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "recovery_chance": Slider(
        label="Chance of Recovery from Propoganda",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1
    ),
    "gain_resistance_chance": Slider(
        label="Chance of Gaining Resistance to Propoganda",
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
    {"Susceptible": "tab:green", "Resistant": "tab:gray"},
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
    name="SIR Propoganda Spread Model"
)

# Initializing an instance of the web page
page 
