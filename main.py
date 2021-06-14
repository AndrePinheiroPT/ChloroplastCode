from time import sleep
from chloroplast.reactions import simulation

variables = [
    ['nº H2O', 0],
    ['nº CO2', 0],
    ['nº RuDP', 0],
    ['nº ADP', 0],
    ['nº NADP+', 0],
    ['Oxitation energy', 0],
    ['Radiation', []]
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
        for k in range(0, 6):
            while True:
                try:
                    variables[k][1] = int(input(f'{variables[k][0]}: '))
                except ValueError:
                    print('Please, type a integer! ')
                else:
                    break

        line()

        print('Now set the radiation intervales:')
        while True:
            radiation = []
            for i in range(1, 3):
                while True:
                    try:
                        radiation.append(int(input(f'Value {i}: ')))
                    except ValueError:
                        print('Please, type a integer! ')
                    else:
                        break
            
            variables[6][1].append(radiation)
            cont = 'N'
            while True:
                cont = input('One more? [Y/N] ').strip().upper()
                if cont.find('Y') != -1 or cont.find('N') != -1:
                    line()
                    break

            if cont == 'N':
                break

        for k in range(0, 7):
            print(f'{variables[k][0]}: {variables[k][1]}')

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
simulation(*[variables[i][1] for i in range(0, 7)])
