from sys import argv

__author__ = 'mauriciomartinezjimenez'
'''
Read a file and returns an array of positions
'''

script, filename = argv

positions = []

def read_input_file(file):
    my_file = open(filename,"r")
    line = my_file.readline()
    processLine(line)

    while line:
        line = my_file.readline()
        processLine(line)
    my_file.close()

    return positions


def line_contains_positions(splited_line):
    if(len(splited_line) != 3): # agregar Validar que son numeros)
        return False
    return True


'''
Process  each line of the input file, reading the coordinates and assign them to a list.
'''
def processLine(line):
    elementsbyline = line.split()

    if(line_contains_positions(elementsbyline)):
        positions.append((float(elementsbyline[0]), float(elementsbyline[1]), float(elementsbyline[2])))
