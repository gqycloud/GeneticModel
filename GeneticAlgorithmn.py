import math
import random
import matplotlib.pyplot as plot

def main():  

  starting_population = [
     {'group': 'male_prey', 'number': 10, 'color': get_random_color, 'max_age': 2, 'interaction': male_interaction},
     {'group': 'female_prey', 'number': 10, 'color': get_random_color, 'max_age': 2, 'interaction': reproduce},
     {'group': 'predators', 'number': 10, 'color': get_predator_color, 'max_age': 5, 'interaction': eat_prey}
     ]
    
  print('generating population...')
  population= initialize_population(starting_population)
  print('beginning population...')
  plot_population(population)
  print('begin interactions ...')
  population = populations_interact(population, 10)
  print('final population')
  plot_population(population)

#Initialization 
def initialize_population(starting_population): 
    population = []
    for organism_type in starting_population: 
        for organism in range(0, organism_type['number']): 
             x = random.randint(-100, 100)
             y = random.randint(-100, 100)
             population.append(Organism(
                     x, 
                     y, 
                     organism_type['group'], 
                     organism_type['max_age'], 
                     organism_type['color'](), 
                     organism_type['interaction']))
    return population
  
#Interacting    
def populations_interact(population, cycles): 
    for i in range(0,cycles): 
       population = population_move(population)
       population = population_interact(population)
       population = clean_population(population)
       plot_population(population)
    return population

def population_move(population): 
    for organism in population:
        organism.move()
    return population

def population_interact(population): 
    for organism in population: 
        organism.interact(organism, population)
    return population

def clean_population(population): 
    for organism in population: 
        organism.die(population)
    return population

#Visualization
def plot_population(population): 
    predator_x = []
    predator_y = []
    predator_color = []

    prey_x = []
    prey_y = []
    prey_color = []
    for organism in population: 
        if(organism.group == 'predators'): 
            predator_x.append(organism.x)
            predator_y.append(organism.y)
            predator_color.append(organism.color)
        else: 
            prey_x.append(organism.x)
            prey_y.append(organism.y)
            prey_color.append(organism.color)
    
    fig, ax = plot.subplots()
    ax.scatter(prey_x, prey_y, c=prey_color, marker='o')
    ax.scatter(predator_x, predator_y, c=predator_color, marker='*')
    
    ax.set_title('Population Plot')
    ax.grid(True)
    fig.tight_layout()
    plot.show()

#Organism Modeling 
class Organism():   
    def __init__(self, startx, starty, group, max_age, color, interaction):
        self.group = group
        self.x = startx
        self.y = starty
        self.age = 0
        self.color = color
        self.interact = interaction
        self.max_age = max_age
        
    #At each iteration all the organisms will move randomly
    def move(self): 
        self.x += random.randint(-5, 5) 
        self.y += random.randint(-5, 5)
        self.age += 1
        
    #At the end of each iteration we will check if the organism has died of old age
    def die(self, population):
        if self.age > self.max_age:
            population.remove(self)

# Filtering functions
def get_nearby_preys(target, population): 
        neighbors = list(filter(lambda population: filter_neighbors(target, population), population))
        preys = list(filter(filter_prey, neighbors) ) 
        return preys

def filter_neighbors(organism, neighbor):
    distance = math.sqrt(abs(organism.x-neighbor.x)^2 + abs(organism.y-neighbor.y)^2);
    if distance < 10: #start with 10 for now, we can make this a variable later
        return True
    else: 
        return False
    
def filter_prey(organism): 
    if(organism.group != 'predators'): 
        return True
    else: 
        return False
    
def filter_male_prey(organism):
    if(organism.group == 'male_prey'): 
        return True
    else: 
        return False
      
def get_most_colorful(prey): 
    return prey.color      
        
#Prey functions             
def get_random_color(): 
    return random.randint(0, 50000)   

def reproduce(target_prey, population):
    reproduction_options = get_nearby_male_prey(target_prey, population)
    if(reproduction_options): 
        reproduction_canidate = max(reproduction_options, key=get_most_colorful)
        for i in range(0, 1): #number of children per iteration
            x = random.randint(-100, 100)
            y = random.randint(-100, 100) 
            color = (target_prey.color + reproduction_canidate.color)/2
            random_group = random.randint(0, 2)
            if (random_group == 0): 
                group = 'female_prey'
                interaction = reproduce
            else: 
                group = 'male_prey'
                interaction = male_interaction
            population.append(Organism(x, y, group, 10, color, interaction))
    return population

def get_nearby_male_prey(target, population): 
    prey_neighbors = get_nearby_preys(target, population)  
    male_prey = list(filter(filter_male_prey, prey_neighbors))
    return male_prey

def male_interaction(organism, population): 
    return population

#Predator functions
def get_predator_color(): 
    return 99999             
     
def eat_prey(target_predator, population):    
     prey_neighbors = get_nearby_preys(target_predator, population)     
     if(prey_neighbors): 
         target_prey = max(prey_neighbors, key=get_most_colorful)
         population.remove(target_prey)
     return population
               
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    main()
