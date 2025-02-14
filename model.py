"""
This file contains all the model classes needed for the SIR model.
"""

import mesa
from mesa import Model
import networkx as nx

from agents import State, VirusAgent

# Generalized function to find the number of agents for each state.
def number_state(model, state):
    return sum(1 for a in model.grid.get_all_cell_contents() if a.state is state)

# Specific function to find the number of INFECTED agents.
def number_red_infected(model):
    return number_state(model, State.INFECTEDRED)

# Specific function to find the other number of INFECTED agents.
def number_blue_infected(model):
    return number_state(model, State.INFECTEDBLUE)

# Specific funtion to find the number of SUSCEPTIBLE agents.
def number_susceptible(model):
    return number_state(model, State.SUSCEPTIBLE)

# Specific function to find the number of RESISTANT agents.
def number_resistant(model):
    return number_state(model, State.RESISTANT)

class VirusOnNetwork(Model):
    """A virus model with some number of agents."""

    """Define the model attributes."""
    def __init__(
            self,
            num_nodes=10,
            avg_node_degree=3,
            red_initial_outbreak_size=1,
            blue_initial_outbreak_size=1,
            red_virus_spread_chance=0.4,
            blue_virus_spread_chance=0.4,
            virus_check_frequency=0.4,
            recovery_chance=0.3,
            gain_resistance_chance=0.5,
            seed=None
    ):
        super().__init__(seed=seed)
        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = mesa.space.NetworkGrid(self.G)

        self.red_initial_outbreak_size = red_initial_outbreak_size
        self.blue_initial_outbreak_size = blue_initial_outbreak_size
        initial_outbreak_size = self.red_initial_outbreak_size + self.blue_initial_outbreak_size
        self.initial_outbreak_size = (initial_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes)

        self.red_virus_spread_chance = red_virus_spread_chance
        self.blue_virus_spread_chance = blue_virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance

        self.datacollector = mesa.DataCollector(
            {
                "Infected by Red Propaganda": number_red_infected,
                "Infected by Blue Propaganda": number_blue_infected,
                "Susceptible": number_susceptible,
                "Resistant": number_resistant,
            }
        )
    
        # Create SUSCEPTIBLE agents.
        for node in self.G.nodes():
            a = VirusAgent(
                self,
                State.SUSCEPTIBLE,
                self.red_virus_spread_chance,
                self.blue_virus_spread_chance,
                self.virus_check_frequency,
                self.recovery_chance,
                self.gain_resistance_chance
            )

            self.grid.place_agent(a, node)

        # Infect with Red Propaganda
        infected_nodes = self.random.sample(list(self.G), self.initial_outbreak_size)
        # Randomly infect some of the agents based on the initial_outbreak_size variables
        for a in self.grid.get_cell_list_contents(infected_nodes):
            a.state = State.INFECTEDRED
        # Infect with Blue Propaganda
        infected_nodes = self.random.sample(list(self.G), self.initial_outbreak_size)
        # Randomly infect some of the agents based on the initial_outbreak_size variable.
        for a in self.grid.get_cell_list_contents(infected_nodes):
            a.state = State.INFECTEDBLUE
        
        self.running = True
        self.datacollector.collect(self)
        
    # Define the agent steps and call them.
    def step(self):
        """Call the agent steps."""
        self.agents.shuffle_do("step")
        # Collect data throughout the steps
        self.datacollector.collect(self)   
