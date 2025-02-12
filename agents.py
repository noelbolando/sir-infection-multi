"""
The file contains all the agent classes needed for the SIR model.
"""

from enum import Enum
from mesa import Agent

class State(Enum):
    """Defining the initial state (number) of susceptible, infected, and resistant agents."""
    R_SUSCEPTIBLE = 0
    R_INFECTED = 1
    R_RESISTANT = 2
    L_SUSCEPTIBLE = 3
    L_INFECTED = 4
    L_RESISTANT = 5

class RVirusAgent(Agent):
    """Individual virus agent definition, properties, and interaction methods."""

    def __init__(
            self,
            model,
            initial_state,

            initial_r_outbreak_size,
            virus_r_spread_chance, # The probability of a SUSCEPTIBLE agent becoming INFECTED
            virus_r_check_frequency, # A function to check if SUSCEPTIBLE agents have become INFECTED
            r_recovery_chance, # The probability of an INFECTED agent recovering. Note that this does not guarantee becoming RESISTANT
            gain_resistance_chance,
            ):
        super().__init__(model)

        # Define the initial state of agents
        self.state = initial_state

        # Define the properties of the R agents
        self.initial_r_outbreak_sie = initial_r_outbreak_size
        self.virus_r_spread_chance = virus_r_spread_chance
        self.virus_r_check_frequency = virus_r_check_frequency
        self.r_recovery_chance = r_recovery_chance
        self.gain_resistance_chance = gain_resistance_chance
        

    def try_to_infect_neighbors(self):
        """Define how SUSCEPTIBLE agents become INFECTED"""
        neighbors_nodes = self.model.grid.get_neighborhood(
            self.pos, include_center=False
        )
        # Find the SUSCEPTIBLE R neighbors
        r_susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.R_SUSCEPTIBLE
        ]
        for a in r_susceptible_neighbors:
            # If the chance of getting infected for a SUSCEPTIBLE agent is 
            # less than the virus_spread_chance metric, 
            # then the SUSCPTIBLE agent becomes an INFECTED agent
            if self.random.random() < self.virus_r_spread_chance:
                a.state = State.R_INFECTED
    
    def try_gain_r_resistance(self):
        """Define how INFECTED agents become RESISTANT"""
        # If the gain_resistance_chance of the INFECTED agent is 
        # less than the gain_resistance_chance metric
        if self.random.random() < self.gain_resistance_chance:
            # Then the agent is RESISTANT
            self.state = State.R_RESISTANT
    
    def try_remove_r_infection(self):
        """Define whether an agent is SUSCEPTIBLE or INFECTED based on recovery_chance metric"""
        # If the recovery_chance of the agent is less than the recovery_chance metric:
        if self.random.random() < self.r_recovery_chance:
            # Then the agent is SUSCEPTIBLE to infection
            self.state = State.R_SUSCEPTIBLE
            self.try_gain_r_resistance()
        else:
            # Otherwise, the agent is INFECTED
            self.state = State.R_INFECTED

    def try_check_r_situation(self):
        """Check to see if an INFECTED agent can become RESISTANT"""
        if (self.random.random() < self.virus_r_check_frequency) and (
            self.state is State.R_INFECTED
        ):
            self.try_remove_r_infection()
    
    def step(self):
        """Define the steps for agents within the model"""
        # If the agent is INFECTED, they will try to infect their neighbors
        if self.state is State.R_INFECTED:
            self.try_to_infect_neighbors()
        # If the agent is INFECTED, check the situation to see if the infection
        # can be removed
        self.try_check_r_situation()

class LVirusAgent(Agent):
    """Individual virus agent definition, properties, and interaction methods."""

    def __init__(
            self,
            model,
            initial_state,

            initial_l_outbreak_size,
            virus_l_spread_chance, # The probability of a SUSCEPTIBLE agent becoming INFECTED
            virus_l_check_frequency, # A function to check if SUSCEPTIBLE agents have become INFECTED
            l_recovery_chance, # The probability of an INFECTED agent recovering. Note that this does not guarantee becoming RESISTANT 
            gain_resistance_chance # The probability of an INFECTED agent becoming RESISTANT
    ):
        super().__init__(model)

        # Define the initial state of agents
        self.state = initial_state
        
        # Define the properties of the L agents
        self.initial_l_outbreak_size = initial_l_outbreak_size
        self.virus_l_spread_chance = virus_l_spread_chance
        self.virus_l_check_frequency = virus_l_check_frequency
        self.l_recovery_chance = l_recovery_chance
        self.gain_resistance_chance = gain_resistance_chance

    def try_to_infect_neighbors(self):
        """Define how SUSCEPTIBLE agents become INFECTED"""
        neighbors_nodes = self.model.grid.get_neighborhood(
            self.pos, include_center=False
        )
        # Find the SUSCEPTIBLE L neighbors
        l_susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.L_SUSCEPTIBLE
        ]
        for a in l_susceptible_neighbors:
            # If the chance of getting infected for a SUSCEPTIBLE agent is 
            # less than the virus_spread_chance metric, 
            # then the SUSCPTIBLE agent becomes an INFECTED agent
            if self.random.random() < self.virus_l_spread_chance:
                a.state = State.L_INFECTED
    
    def try_gain_l_resistance(self):
        """Define how INFECTED agents become RESISTANT"""
        # If the gain_resistance_chance of the INFECTED agent is 
        # less than the gain_resistance_chance metric
        if self.random.random() < self.gain_resistance_chance:
            # Then the agent is RESISTANT
            self.state = State.L_RESISTANT
    
    def try_remove_l_infection(self):
        """Define whether an agent is SUSCEPTIBLE or INFECTED based on recovery_chance metric"""
        # If the recovery_chance of the agent is less than the recovery_chance metric:
        if self.random.random() < self.l_recovery_chance:
            # Then the agent is SUSCEPTIBLE to infection
            self.state = State.L_SUSCEPTIBLE
            self.try_gain_l_resistance()
        else:
            # Otherwise, the agent is INFECTED
            self.state = State.L_INFECTED
    
    def try_check_l_situation(self):
        """Check to see if an INFECTED agent can become RESISTANT"""
        if (self.random.random() < self.virus_l_check_frequency) and (
            self.state is State.L_INFECTED
        ):
            self.try_remove_l_infection()
    
    def step(self):
        """Define the steps for agents within the model"""
        # If the agent is INFECTED, they will try to infect their neighbors
        if self.state is State.L_INFECTED:
            self.try_to_infect_neighbors()
        # If the agent is INFECTED, check the situation to see if the infection
        # can be removed
        self.try_check_l_situation()