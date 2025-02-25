"""
The file contains all the agent classes needed for the SIR model.
"""

from enum import Enum
from mesa import Agent

class State(Enum):
    """Defining the initial state (number) of susceptible, infected, and resistant agents."""
    SUSCEPTIBLE = 0
    INFECTEDRED = 1 # Susceptible agents exposed to propaganda of red virus
    INFECTEDBLUE = 2 # Susceptible agents exposed to propaganda of blue virus
    RESISTANT = 3

class VirusAgent(Agent):
    """Individual virus agent definition, properties, and interaction methods."""

    def __init__(
            self,
            model,
            initial_state,

            red_virus_spread_chance, # The probability of a SUSCEPTIBLE agent becoming INFECTED
            virus_check_frequency, # A function to check if SUSCEPTIBLE agents have become INFECTED
            blue_virus_spread_chance, # The probability of a SUSCEPTIBLE agent becoming INFECTED
            recovery_chance, # The probability of an INFECTED agent recovering. Note that this does not guarantee becoming RESISTANT 
            gain_resistance_chance, # The probability of an INFECTED agent becoming RESISTANT
    ):
        super().__init__(model)

        # Define the initial state of agents
        self.state = initial_state

        # Define the properties of the agents
        self.red_virus_spread_chance = red_virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.blue_virus_spread_chance = blue_virus_spread_chance
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance

    def try_to_infect_neighbors(self):
        """Define how SUSCEPTIBLE agents become INFECTED"""
        neighbors_nodes = self.model.grid.get_neighborhood(
            self.pos, include_center=False
        )
        # Find the SUSCEPTIBLE neighbors
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]
        for a in susceptible_neighbors:
            if self.random.random() < self.red_virus_spread_chance:
                a.state = State.INFECTEDRED
            elif self.random.random() < self.blue_virus_spread_chance:
                a.state = State.INFECTEDBLUE
    
    def try_gain_resistance(self):
        """Define how INFECTED agents become RESISTANT"""
        if self.random.random() < self.gain_resistance_chance:
            self.state = State.RESISTANT
    
    def try_remove_infection(self):
        """Define whether an agent is SUSCEPTIBLE or INFECTED based on recovery_chance metric"""
        if self.state == State.INFECTEDRED:
            if self.random.random() < self.recovery_chance:
                self.state = State.SUSCEPTIBLE
                self.try_gain_resistance()
            else:
                self.state = State.INFECTEDRED
        elif self.state == State.INFECTEDBLUE:
            if self.random.random() < self.recovery_chance:
                self.state = State.SUSCEPTIBLE
                self.try_gain_resistance()
            else:
                self.state = State.INFECTEDBLUE


    def try_check_situation(self):
        """Check to see if an INFECTED agent can become RESISTANT"""
        if (self.random.random() < self.virus_check_frequency) and (
            self.state is State.INFECTEDRED or State.INFECTEDBLUE
        ):
            self.try_remove_infection()
    
    def step(self):
        """Define the steps for agents within the model"""
        if self.state is State.INFECTEDRED or State.INFECTEDBLUE:
            self.try_to_infect_neighbors()
        self.try_check_situation()
