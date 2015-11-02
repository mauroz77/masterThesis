from sys import argv
import os.path
import sys

__author__ = 'mauriciomartinezjimenez'
'''
Read a file and returns an array of positions
'''

script, filename = argv

positions = []

def read_input_file(file):
    try:
        #print("pdb_positions_reader.read_input_file "+file)
        #positions.count()
        positions[:] = []
        my_file = open(file,"r")

        line = my_file.readline()
        processLine(line)

        while line:
            line = my_file.readline()
            processLine(line)
        my_file.close()

        return positions

    except IOError:
        sys.exit("File ["+file + "] does not exist!")


def line_contains_positions(splited_line):
    if(len(splited_line) != 3): # agregar Validar que son numeros)
        return False
    return True


'''
Process  each line of the input file, reading the coordinates and assign them to a list.
'''
def processLine(line):
    elementsbyline = line.split()

    if len(elementsbyline) > 10:
        if(elementsbyline[0] == 'ATOM' and elementsbyline[2] == "CA"):
            positions.append((float(elementsbyline[6]), float(elementsbyline[7]), float(elementsbyline[8])))

