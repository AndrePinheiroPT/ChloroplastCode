from math import *
from random import randint
from chemistry import *

HYDROGEN_CATION = Molecules('H+', 'Hydrogen cation')
WATER = Molecules('H2O', 'Water')
ADP = Molecules('C10H15N5O10P2', 'ADP')
ATP = Molecules('C10H15N5O10P3', 'ATP')
NADPP = Molecules('C21H29N7O17P3', 'NADP+')
NADPH = Molecules('C21H30N7O17P3', 'NADPH')
CARBON_DIOXIDE = Molecules('CO2', 'Carbon dioxide')
RUDP = Molecules('C5H12O11P2', 'RuDP')
PGAL_S = Molecules('C3H7O6P_S', 'PGAL_S')
PGAL = Molecules('C3H5O5P','PGAL')
GLICOSE = Molecules('C6H12O6', 'Glicose')
PGA = Molecules('C3H7O7P', 'PGA')
OXYGEN_ATOM = Molecules('O', 'Oxygen atom')
OXYGEN = Molecules('O2', 'Oxygen') 

inner_thylakoid_system = System(24*[WATER])
stroma_system = System(18*[ADP]+12*[NADPP, CARBON_DIOXIDE]+6*[RUDP])
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
    stroma_system.do_reaction(2*[PGAL_S, ADP], 2*[ATP]+[GLICOSE])


def calvin_cicle():
    stroma_system.do_reaction([CARBON_DIOXIDE]+[RUDP]+2*[ATP], 2*[ADP, PGA])

    stroma_system.do_reaction(2*[PGA, NADPH], 2*[NADP, PGAL])

    stroma_system.do_reaction(5*[PGAL]+3*[ATP], [PGAL_S]+3*[ADP, RUDP])


def ATPase():
    if inner_thylakoid_system.length(HYDROGEN_CATION) > stroma_system.length(HYDROGEN_CATION):
        inner_thylakoid_system.remove_molecule(HYDROGEN_CATION)
        stroma_system.add_molecule(HYDROGEN_CATION)

        if stroma_system.length(ADP) >= 1 and inner_thylakoid_system.length(HYDROGEN_CATION) >= 1:
            stroma_system.do_reaction([ADP], [ATP])


def water_photolysis():
    if photosystem1.electrons == 0 and inner_thylakoid_system.length(WATER) > 0:
        inner_thylakoid_system.do_reaction([WATER], 2*[HYDROGEN_CATION]+[OXYGEN_ATOM])
        if inner_thylakoid_system.length(OXYGEN_ATOM) > 1:
            inner_thylakoid_system.do_reaction(2*[OXYGEN_ATOM], [OXYGEN])

        photosystem1.electrons += 2
        

def protein_hydro():
    global inner_thylakoid
    if transport_electrons[0] >= 2 and stroma_system.length(HYDROGEN_CATION) >= 2: 
        for i in range(0, 2):
            inner_thylakoid_system.add_molecule(HYDROGEN_CATION)
            stroma_system.remove_molecule(HYDROGEN_CATION)

        transport_electrons[0] -= 2
        photosystem2.electrons += 2 


def nadpp_reduction():
    if transport_electrons[1] >= 2 and stroma_system.length(HYDROGEN_CATION) >= 2 and stroma_system.length(NADPP) >= 1:
        stroma_system.do_reaction([NADPP]+2*[HYDROGEN_CATION], [NADPH, HYDROGEN_CATION])
        transport_electrons[1] -= 2


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
        
    #print(f'inner_thylacoid: {inner_thylakoid}, stroma: {stroma}, tp: {transport_electrons}')