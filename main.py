from math import *
from random import randint

inner_thylakoid = {
    'H+': 0,
    'O2': 0,
    'H2O': 24
}

stroma = {
    'H+': 0,
    'ADP': 18,
    'ATP': 0,
    'NADP+': 12,
    'NADPH': 0,
    'CO2': 12,
    'RuDP': 6,
    'PGA': 0,
    'PGAL': 0,
    'PGAL_storage': 0,
    'C6H12O6': 0
}

transport_electrons = [0, 0]

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
        
    def check_oxidation(self, transport_type):
        if self.energy >= 1000:
            self.electrons -= 2
            self.energy -= 1000
            transport_electrons[transport_type] += 2
    
    def photo_reaction(self, labmda):
        absorved = True if self.light_chlorophyllA(labmda) > randint(0, 100) else False
        if absorved and self.electrons != 0:
            frequency = SPEED_OF_LIGHT / labmda
            light_energy = PLANK_MODIFIED * frequency
            self.energy += light_energy
            #print(f'Energy absorved: {light_energy}')
            #print(f'Energy: {self.energy}')
        
    
    def light_chlorophyllA(self, labmda):
        return 35*sin(-5 + labmda*1/35)+35
    

photosystem1 = Photosystem(23, 12, 40)
photosystem2 = Photosystem(23, 12, 40)

def synthase_of_glicose():
    if stroma['ADP'] >= 2 and stroma['PGAL_storage'] >= 2:
        stroma['ADP'] -= 2
        stroma['PGAL_storage'] -= 2

        stroma['ATP'] += 2
        stroma['C6H12O6'] += 1


def calvin_cicle():
    if stroma['CO2'] >= 1 and stroma['RuDP'] >= 1 and stroma['ATP'] >= 2:
        stroma['CO2'] -= 1
        stroma['RuDP'] -= 1
        stroma['ATP'] -= 2

        stroma['ADP'] += 2
        stroma['PGA'] += 2

    if stroma['PGA'] >= 2 and stroma['NADPH'] >= 2:
        stroma['PGA'] -=2
        stroma['NADPH'] -= 2

        stroma['NADP+'] += 2
        stroma['PGAL'] += 2

    if stroma['PGAL'] >= 6 and stroma['ATP'] >= 3 :
        stroma['PGAL'] -= 5
        stroma['ATP'] -= 3

        stroma['PGAL_storage'] += 1
        stroma['ADP'] += 3
        stroma['RuDP'] += 3


def ATPase():
    global inner_thylakoid, stroma
    if inner_thylakoid['H+'] > stroma['H+']:
        inner_thylakoid['H+'] -= 1
        stroma['H+'] += 1

        if stroma['ADP'] >= 1 and inner_thylakoid['H+'] >= 1:
            stroma['ADP'] -= 1
            stroma['ATP'] += 1


def water_photolysis():
    global h2o_molecules, o2_molecules
    if photosystem1.electrons == 0 and inner_thylakoid['H2O'] > 0:
        inner_thylakoid['H2O'] -= 1
        inner_thylakoid['O2'] += 1/2
        inner_thylakoid['H+'] += 2
        photosystem1.electrons += 2
        

def protein_hydro():
    global inner_thylakoid
    if transport_electrons[0] >= 2 and stroma['H+'] >= 2: 
        inner_thylakoid['H+'] += 2
        stroma['H+'] -= 2
        transport_electrons[0] -= 2
        photosystem2.electrons += 2 


def nadpp_reduction():
    global stroma
    if transport_electrons[1] >= 2 and stroma['H+'] >= 2 and stroma['NADP+'] >= 1:
        stroma['NADP+'] -= 1
        stroma['H+'] -= 2
        transport_electrons[1] -= 2

        stroma['NADPH'] += 1
        stroma['H+'] += 1


while True:
    for i in range(0, light_intensity):
        photosystem1.photo_reaction(557)
        photosystem1.check_oxidation(0)
        water_photolysis()

    protein_hydro()

    for i in range(0, light_intensity):
        photosystem2.photo_reaction(557)
        photosystem2.check_oxidation(1)

    nadpp_reduction()
    ATPase()
    calvin_cicle()
    synthase_of_glicose()
        
    print(f'inner_thylacoid: {inner_thylakoid}, stroma: {stroma}, tp: {transport_electrons}')