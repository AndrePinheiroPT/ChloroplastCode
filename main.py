from time import sleep
from chloroplast.reactions import simulation

variables = [
    ['nº H2O', 0],
    ['nº CO2', 0],
    ['nº RuDP', 0],
    ['nº ADP', 0],
    ['nº NADP+', 0],
    ['oxitation energy', 0]
]


def line():
    print('~'*60)

def countdown():
    print('Starting the simulation in:')
    for cout in range(3, 0, -1):
        print(cout)
        sleep(1)

def menu():
    line()

    print('PhotoCode v1.0.0\n\
Copyright \u00a9 André Pinheiro\n\
Read the licence for more information')

    line()

    print('Welcome to the PhotoCode! For start a simulation, you\n\
need the set the follow variables:')
    while True:
        for variable in variables:
            while True:
                try:
                    variable[1] = int(input(f'{variable[0]}: '))
                except ValueError:
                    print('Please, type a integer! ')
                else:
                    break

        line()
        for variable in variables:
            print(f'{variable[0]}: {variable[1]}')
        line()

        while True:
            cont = input('Are you sure? [Y/N] ').strip().upper()
            if cont.find('Y') != -1 or cont.find('N') != -1:
                line()
                break

        if cont == 'Y':
            break
            
menu()
countdown()
simulation(variables[0][1], variables[1][1], variables[3][1],
           variables[4][1], variables[2][1], variables[5][1])

