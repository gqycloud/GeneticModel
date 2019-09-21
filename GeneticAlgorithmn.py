import math
import random
import matplotlib.pyplot as plot

def main():  
    
  #Starting population of prey and predator organisms 
  starting_males = 10
  starting_females = 10
  predators = 10
  
  print('generating population...')
  population= initialize_population(starting_males, starting_females, predators)
  print('beginning population...')
  plot_population(population)
  print('begin interactions ...')
  population = populations_interact(population, 20)
  print('final population')
  plot_population(population)
  
  
def initialize_population(starting_males, starting_females, predators): 
    population = []
    for i in range(starting_males):
        x = random.randint(-50, 50)
        y = random.randint(-50, 50) 
        color = random.randint(0, 50000) 
        group = 'male_prey'
        population.append(Organism(group, x, y, color))
    for i in range(starting_females):
        x = random.randint(-50, 50)
        y = random.randint(-50, 50) 
        color = random.randint(0, 50000) 
        group = 'female_prey'
        population.append(Organism(group, x, y, color))
    for i in range(predators):
        x = random.randint(-50, 50)
        y = random.randint(-50, 50) 
        color = random.randint(0, 50000) 
        group = 'predators'
        population.append(Organism(group, x, y, color))   
    return population
      
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
        organism.interact(population)
    return population

def clean_population(population): 
    for organism in population: 
        organism.die(population)
    return population


def plot_population(population): 
    x = []
    y = []
    color = []
    for organism in population: 
        x.append(organism.x)
        y.append(organism.y)
        color.append(organism.color)
        
    fig, ax = plot.subplots()
    ax.scatter(x , y, c=color)
    
    ax.set_title('Population Plot')
    ax.grid(True)
    fig.tight_layout()
    plot.show()

class Organism(): 
    #Each organism will have a type and a starting location in the 'environment'
    #The color and the age only matter for the prey population    
    def __init__(self, group, startx, starty, color):
        self.group = group
        self.x = startx
        self.y = starty
        self.age = 0
        if(group == 'predator'): 
            self.color = 99999
        else:
            self.color = color
        
    #At each iteration all the organisms will move randomly
    def move(self): 
        self.x += random.randint(-5, 5) #start with 5 for now we can make this a variable later
        self.y += random.randint(-5, 5)
        self.age += 1
        
    #At the end of each iteration we will check if the organism has died of old age
    def die(self, population):
        if self.age > 10: #we can play around with this 
            population.remove(self)
            
    def interact(self, population): 
        #Generate a list of prey neighbors
        neighbors = filter(lambda population: filter_neighbors(self, population), population)
        preys = filter(filter_prey, neighbors)        
        
        if self.group == 'female_prey':            
                if (self.age > 3): #reproductive age 
                   population = reproduce(self, preys, population)
        elif self.group == 'predator':
            population = eat_prey(population, preys)


def eat_prey(population, preys): 
     most_colorful = max(preys, key=get_most_colorful)
     population.remove(most_colorful)
     return population
            
def reproduce(target_prey, neighbor_preys, population):
    reproductive_preys = filter(filter_reproductive_prey, neighbor_preys)
    reproductive_male_preys = filter(filter_male_prey, reproductive_preys)
    most_colorful_reproductive = max(reproductive_male_preys, key=get_most_colorful)
    for i in range(0, 1): #number of children per iteration
        x = random.randint(-100, 100)
        y = random.randint(-100, 100) 
        color = (target_prey.color + most_colorful_reproductive.color)/2
        random_group = random.randint(0, 2)
        if (random_group == 0): 
            group = 'female_prey'
        else: 
            group = 'male_prey'
        population.append(Organism(group, x, y, color))
    return population

def filter_male_prey(organism):
    if(organism.group == 'male_prey'): 
        return organism 
    
def filter_reproductive_prey(organism): 
    if(organism.age > 3): 
        return organism
      
def filter_prey(organism): 
    if(organism.group != 'predator'): 
        return organism
                
def filter_neighbors(organism, neighbor):
    distance = math.sqrt(abs(organism.x-neighbor.x)^2 + abs(organism.y-neighbor.y)^2);
    if distance < 10: #start with 10 for now, we can make this a variable later
        return neighbor

def get_most_colorful(prey): 
    return prey.color
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    main()