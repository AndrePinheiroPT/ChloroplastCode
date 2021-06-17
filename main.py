from chloroplast.reactions import simulation
from menu_tools import *

variables = {
    'nº H2O': 0,
    'nº CO2': 0,
    'nº RuDP': 0,
    'nº ADP': 0,
    'nº NADP+': 0,
    'Oxitation energy': 0,
    'Light intensity': 0,
    'Radiation': []
}

try:
    file = open('RADIATION_INTERVALES.txt', 'r')
    values = file.read().split()
    variables['Radiation'] = [[int(values[i]), int(values[i + 1])] for i in range(0, len(values), 2)]
    file.close()
except Exception as error:
    print(f'There is a error in impress data: {error.__class__}')
    exit()


line()
print('ChloroplastCode v1.0.0\n\
Copyright \u00a9 André Pinheiro\n\
Read the licence for more information')

line()
print('Welcome to the ChloroplastCode! For start a simulation, you\n\
need the set the follow variables:')
    
# Menu loop for check values
state = True
while state:
    # Set all variables except "radiation"
    for key in variables:
        if key != 'Radiation':
            variables[key] = read_int(f'{key}: ')
    
    line()
    # Show all variable value typed
    for key in variables:
        print(f'{key} -> {variables[key]}')

    line()
    # Ask for check all values
    while True:
        cont = input('Are you sure? [Y/N] ').strip().upper()
        if cont == 'Y' or cont == 'N':
            state = False if cont == 'Y' else True
            break
    line()


# Load countdown and simulatin functions           
countdown()
simulation(*[value for key, value in variables.items()])
