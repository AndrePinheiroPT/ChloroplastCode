from math import *
from random import randint

o2_molecules = 0
h2o_molecules = 9
light_intensity = 10

SPEED_OF_LIGHT = 3 * 10**8
PLANK_MODIFIED = 1 * 10**-6 

class Photosystem:
    def __init__(self,
                 chlorophyllA_length,
                 chlorophyllB_length,
                 beta_carotene_length):
        
        self.chlorophyllA_length = chlorophyllA_length
        self.chlorophyllB_length = chlorophyllB_length
        self.beta_carotene_length = beta_carotene_length
        self.energy = 0
        self.electrons = 2
        
    def check_oxidation(self):
        if self.energy >= 1000:
            self.electrons -= 2
            self.energy -= 1000
    
    def photo_reaction(self, labmda):
        absorved = True if self.light_chlorophyllA(labmda) > randint(0, 100) else False
        if absorved and self.electrons != 0:
            frequency = SPEED_OF_LIGHT / labmda
            light_energy = PLANK_MODIFIED * frequency
            self.energy += light_energy
            print(f'Energy absorved: {light_energy}')
            print(f'Energy: {self.energy}')
        
    
    def light_chlorophyllA(self, labmda):
        return 35*sin(-5 + labmda*1/35)+35
    

photosystem1 = Photosystem(23, 12, 40)

def water_photolysis():
    global h2o_molecules, o2_molecules
    if photosystem1.electrons == 0 and h2o_molecules > 0:
        h2o_molecules -= 1
        o2_molecules += 1/2
        photosystem1.electrons += 2
        

while True:
    for i in range(0, light_intensity):
        photosystem1.photo_reaction(557)
        photosystem1.check_oxidation()
        water_photolysis()
        
    print(f'H20 molecules: {h2o_molecules}')