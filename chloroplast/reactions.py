from random import randint
from chloroplast.chemistry import *


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

light_intensity = 10

SPEED_OF_LIGHT = 3 * 10**8
PLANK_MODIFIED = 1 * 10**-6 

inner_thylakoid_system = 0
stroma_system = 0
transport_electrons = [0, 0]

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
        
    def check_oxidation(self, transport_type, oxi_energy):
        if self.energy >= oxi_energy:
            self.electrons -= 2
            self.energy -= oxi_energy
            transport_electrons[transport_type] += 2
    
    def photo_reaction(self, labmda):
        absorved = True if self.light_chlorophyllA(labmda) < randint(0, 100) else False
        if absorved and self.electrons != 0:
            frequency = SPEED_OF_LIGHT / labmda
            light_energy = PLANK_MODIFIED * frequency
            self.energy += light_energy
            #print(f'Energy absorved: {light_energy}')
            #print(f'Energy: {self.energy}')
        
    
    def light_chlorophyllA(self, x):
        labmda = x - 400
        if 0 <= labmda < 25:
            return 1.32 * labmda + 134
        elif 25 <= labmda < 50:
            return -2.6 * labmda + 134
        elif 50 <= labmda < 200:
            return 4
        elif 200 <= labmda < 250:
            return 0.1 * labmda - 16
        elif 250 <= labmda < 270:
            return 2.04 * labmda - 500
        elif 270 <= labmda <= 300:
            return -1.57 * labmda + 474
    

photosystem1 = Photosystem(23, 12, 40)
photosystem2 = Photosystem(23, 12, 40)

def synthase_of_glicose():
    stroma_system.do_reaction(2*[PGAL_S, ADP], 2*[ATP]+[GLICOSE])


def calvin_cicle():
    stroma_system.do_reaction([CARBON_DIOXIDE]+[RUDP]+2*[ATP], 2*[ADP, PGA])
    stroma_system.do_reaction(2*[PGA, NADPH], 2*[NADPP, PGAL])
    stroma_system.do_reaction(5*[PGAL]+3*[ATP], [PGAL_S]+3*[ADP, RUDP])


def atpase():
    global inner_thylakoid_system, stroma_system
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


def show_status():
    print(f'Thylakoid: Water {inner_thylakoid_system.length(WATER)} | Oxygen {inner_thylakoid_system.length(OXYGEN)} | H+ {inner_thylakoid_system.length(HYDROGEN_CATION)}  ', end='/  ')
    print(f'Stroma: ADP {stroma_system.length(ADP)} | ATP {stroma_system.length(ATP)} | NAPH+ {stroma_system.length(NADPP)} | NADPH {stroma_system.length(NADPH)} | CO2 {stroma_system.length(CARBON_DIOXIDE)} | PGAL {stroma_system.length(PGAL_S)} | Glicose {stroma_system.length(GLICOSE)} | H+ {stroma_system.length(HYDROGEN_CATION)} | Ep1 {photosystem1.energy:.2f} | Ep2 {photosystem2.energy:.2f}')


def simulation(h2o, co2, rudp, adp, nadpp, oxi_energy, radiation_intervales):
    random_radiations = []
    for radiation in radiation_intervales:
        random_radiations.append(randint(radiation[0], radiation[1]))

    final_radiation = random_radiations[randint(0, len(radiation_intervales) - 1)]

    global inner_thylakoid_system, stroma_system
    inner_thylakoid_system = System(h2o * [WATER])
    stroma_system = System(adp*[ADP] + nadpp*[NADPP] + co2*[CARBON_DIOXIDE] + rudp*[RUDP])

    while True:
        for i in range(0, light_intensity):
            photosystem1.photo_reaction(final_radiation)
            photosystem1.check_oxidation(0, oxi_energy)
            water_photolysis()

        protein_hydro()

        for i in range(0, light_intensity):
            photosystem2.photo_reaction(425)
            photosystem2.check_oxidation(1, final_radiation)

        atpase()
        nadpp_reduction()
        calvin_cicle()
        synthase_of_glicose()
        
        show_status()
