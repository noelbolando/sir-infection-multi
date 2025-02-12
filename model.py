"""
This file contains all the model classes needed for the SIR model.
"""

import mesa
from mesa import Model
import networkx as nx

from agents import State, RVirusAgent, LVirusAgent

# Generalized function to find the number of agents for each state.
def number_state(model, state):
    return sum(1 for a in model.grid.get_all_cell_contents() if a.state is state)

# Specific function to find the number of R INFECTED agents.
def number_r_infected(model):
    return number_state(model, State.R_INFECTED)

# Specific funtion to find the number of R SUSCEPTIBLE agents.
def number_r_susceptible(model):
    return number_state(model, State.R_SUSCEPTIBLE)

# Specific function to find the number of R RESISTANT agents.
def number_r_resistant(model):
    return number_state(model, State.R_RESISTANT)

# Specific function to find the number of L INFECTED agents.
def number_l_infected(model):
    return number_state(model, State.L_INFECTED)

# Specific funtion to find the number of L SUSCEPTIBLE agents.
def number_l_susceptible(model):
    return number_state(model, State.L_SUSCEPTIBLE)

# Specific function to find the number of L RESISTANT agents.
def number_l_resistant(model):
    return number_state(model, State.L_RESISTANT)

class VirusOnNetwork(Model):
    """A virus model with some number of agents."""

    """Define the model attributes."""
    def __init__(
            self,
            num_nodes=20,
            avg_node_degree=3,
            gain_resistance_chance=0.5,
            
            # R traits
            initial_r_outbreak_size=1,
            virus_r_spread_chance=0.4,
            virus_r_check_frequency=0.4,
            r_recovery_chance=0.3,
            
            # L traits
            initial_l_outbreak_size=1,
            virus_l_spread_chance=0.4,
            virus_l_check_frequency=0.4,
            l_recovery_chance=0.3,
            
            seed=None
    ):
        super().__init__(seed=seed)
        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        self.grid = mesa.space.NetworkGrid(self.G)
        self.gain_resistance_chance = gain_resistance_chance

        # Outbreak size calculator
        self.initial_r_outbreak_size = initial_r_outbreak_size
        self.initial_l_outbreak_size = initial_l_outbreak_size 
        initial_outbreak_size = self.initial_r_outbreak_size + self.initial_l_outbreak_size

        # R initializers
        self.initial_r_outbreak_size = (initial_r_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes)
        self.virus_r_spread_chance = virus_r_spread_chance
        self.virus_r_check_frequency = virus_r_check_frequency
        self.r_recovery_chance = r_recovery_chance

        # L initializers
        self.initial_l_outbreak_size = (initial_l_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes)
        self.virus_l_spread_chance = virus_l_spread_chance
        self.virus_l_check_frequency = virus_l_check_frequency
        self.l_recovery_chance = l_recovery_chance


        self.datacollector = mesa.DataCollector(
            {
                "R Infected": number_r_infected,
                "R Susceptible": number_r_susceptible,
                "R Resistant": number_r_resistant,
                "L Infected": number_l_infected,
                "L Susceptible": number_l_susceptible,
                "L Resistant": number_l_resistant
            }
        )
    
        # Create SUSCEPTIBLE agents.
        for node in self.G.nodes():
            # R SUSCEPTIBLE agents
            a = RVirusAgent(
                self,
                State.R_SUSCEPTIBLE,
                self.gain_resistance_chance,
                self.virus_r_spread_chance,
                self.virus_r_check_frequency,
                self.r_recovery_chance,
            ),
            # L SUSCEPTIBLE agents
            b = LVirusAgent(
                self,
                State.L_SUSCEPTIBLE,
                self.gain_resistance_chance,
                self.virus_l_spread_chance,
                self.virus_l_check_frequency,
                self.l_recovery_chance,
            )
        
            # Add the SUSCEPTIBLE agents to the model.
            self.grid.place_agent(a, b, node)

        # Infect some of the R agents added to the model.
        infected_r_nodes = self.random.sample(list(self.G), self.initial_r_outbreak_size)
        # Randomly infect some of the agents based on the initial_outbreak_size variable.
        for a in self.grid.get_cell_list_contents(infected_r_nodes):
            a.state = State.R_INFECTED
       
        # Infect some of the L agents added to the model.
        infected_l_nodes = self.random.sample(list(self.G), self.initial_l_outbreak_size)
        # Randomly infect some of the agents based on the initial_outbreak_size variable.
        for b in self.grid.get_cell_list_contents(infected_l_nodes):
            b.state = State.L_INFECTED
        
        self.running = True
        self.datacollector.collect(self)
    
    # Define the agent steps and call them.
    def step(self):
        """Call the agent steps."""
        self.agents.shuffle_do("step")
        # Collect data throughout the steps
        self.datacollector.collect(self)   
