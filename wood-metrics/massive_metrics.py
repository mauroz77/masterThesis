__author__ = 'mauriciomartinezjimenez'
from sys import argv
import os.path
import os;
import metrics

output_file_name = "output.txt"
output_file = open(output_file_name,"w")

'''
This file allows to calculate the wood's metrics to a list set of proteins specified in a file
'''
script, filename = argv

proteins = []

def process_input_file(file):
    output_file.write("r_min|p_min|SR|SLR|r_prim_min|p_prim_min"+os.linesep)
    print("r_min|p_min|SR|SLR|r_prim_min|p_prim_min")
    if os.path.isfile(filename):
        my_file = open(filename,"r")
        line = my_file.readline()
        processLine(line)

        while line:
            line = my_file.readline()
            if(line != ""):
                processLine(line)
        my_file.close()

        return proteins
    else:
        print("No file found " + file)

    output_file.close()

def processLine(line):
    print("Execute  metrics_by_protein to ["+line+"]")
    metrics_by_protein = metrics.get_metrics(line.rstrip())
    output_file.write(metrics_by_protein + os.linesep)
    #print(metrics_by_protein)



# Main del programa
if filename != "":
    process_input_file(filename)
else:
    print("No file")
