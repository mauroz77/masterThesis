#!/usr/bin/python
from math import sqrt
from sys import argv
import pdb_positions_reader
import math

script, filename = argv

positions = []

'''
Calculate the centroid from a list of points. Returns a tuple with the result.
'''
def calculate_centroid(points):
    sumx = 0.0
    sumy = 0.0
    sumz = 0.0
    for i in points:
        sumx += i[0]
        sumy += i[1]
        sumz += i[2]
    return (sumx / len(points), sumy / len(points), sumz / len(points))


'''
calculates the euclidean distance between two points
'''
def euclidean_distance(point_a, point_b):
    # print("distance between: ",point_a, " and ", point_b)
    componentx = (point_a[0] - point_b[0]) ** 2
    componenty = (point_a[1] - point_b[1]) ** 2
    componentz = (point_a[2] - point_b[2]) ** 2
    return sqrt(componentx + componenty + componentz)


'''
Calculate dn_min as the minimum distance to the centroid of a neighbouring of 10 from N terminus (ignoring the
first 10 residues
'''
def dn_min(positions, centroid):
    distances = []
    for i in range(10, 20):
        #print("Tomo a ", positions[i], "en ", i)
        distances.append(euclidean_distance(positions[i], centroid))
    #print("nDistances: ", distances)
    #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    return min(distances)


'''
Calculate dc_min as the minimum distance to the centroid of a neighbouring of 10 from C terminus (ignoring the
last 10 residues
'''
def dc_min(positions, centroid):
    distances = []
    size = len(positions)
    for i in range(size - 10, size - 20, -1):
        #print("Tomo a ", positions[i], "en ", i)
        distances.append(euclidean_distance(positions[i], centroid))
    #print("cDistances: ", distances)
    #print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    return min(distances)


'''
Calculates r_min as the Ratio of minimun distances of near-terminal segments to the centroid (dc_min/dn_min)
'''
def r_min(positions):
    centroid = calculate_centroid(positions)
    dc_min_value = dc_min(positions, centroid)
    dn_min_value = dn_min(positions, centroid)
    #print("dc_min_value: ", dc_min_value)
    #print("-------------------------------")
    #print("dn_min_value: ", dn_min_value)
    #print("-------------------------------")
    return dc_min_value / dn_min_value


'''
Calculate Proportion of length (Pmin) until closest to the centroid, measured from the N-terminus.
Pmin = i/n where n is the number of residues
'''
def p_min(positions, centroid):
    distances = []
    for i in  positions:
        distances.append(euclidean_distance(i, centroid))
    return distances.index(min(distances))

'''
Calculate Actual number of previous contacts, counting from N terminus. [A previous contact with a residue at position
i <= 7 from the N-Terminus is deemed to occur when a residue  numbered from 1 to i-6 comes within 13 Amstrongs of
residue i.]
'''
def actual_previous_contacts_n(positions):
    list_result = [0] * len(positions)
    for i in range(6, len(positions)):
        for j in range(0, i - 6):
            if euclidean_distance(positions[j], positions[i]) <= 13:
                #print("Ha comparado ", i, j, positions[j], positions[i], euclidean_distance(positions[j], positions[i]))
                list_result[i] += 1
    return list_result


'''
Calculate Actual number of previous contacts, counting from C terminus.
'''
def actual_previous_contacts_c(positions):
    list_result = [0] * len(positions)
    n = len(positions)
    for i in range(0, n - 7):
        for j in range(i + 1, n - 5):
            if euclidean_distance(positions[j], positions[i]) <= 13:
                #print("Ha comparadooo ", i, j, positions[j], positions[i],
                      #euclidean_distance(positions[j], positions[i]))
                list_result[i] += 1
    return list_result


def divide_in_groups(positions):
    groups = []
    actual_contacts_n = actual_previous_contacts_n(positions)
    #print("actual_contacts_n ", len(actual_contacts_n), actual_contacts_n)

    actual_contacts_c = actual_previous_contacts_c(positions)
    #print("actual_contacts_c ",len(actual_contacts_c), actual_contacts_c)
    sum_n = 0
    sum_c = 0
    current_sum_previous_contacts = 0
    for i in range(0, len(positions)):
        if actual_contacts_n[i] > 0 and  actual_contacts_c[i] > 0:
            groups.append((actual_contacts_n[i] + sum_n,actual_contacts_c[i] + sum_c,[i]))
            #print("Greater ",actual_contacts_n[i], actual_contacts_c[i], "current ", sum_n, sum_c)
            sum_n = 0
            sum_c = 0
        else:
            #print("No Greater ",actual_contacts_n[i], actual_contacts_c[i], sum_n, sum_c)
            sum_n = sum_n + actual_contacts_n[i]
            sum_c = sum_c + actual_contacts_c[i]
            if sum_n > 0 and sum_c > 0:
                #print("Por suma: ",(sum_n,sum_c))
                groups.append((sum_n,sum_c))
                sum_n = 0
                sum_c = 0
    # if there was a group forming, it's added to the result
    #if sum_c > 0 and s

    return groups

    print("Grupos ",groups)


'''
calculates the sum of ratios (SR)
'''
def calculate_sr(groups):
    sum = 0
    for i in groups:
        sum += float(i[0])/float(i[1])
        #print("s ",sum, i[0], i[1])

    return sum / len(groups)



'''
calculates the sum of logaritmic ratios (SLR)
'''
def calculate_slr(groups):
    sum = 0
    for i in groups:
        sum += math.log10(float(i[0]))- math.log10(float(i[1]))
        #print("s ",sum, i[0], i[1])

    return sum / len(groups)


'''
Calculates binary value for r_mim
'''
def r_prim_min(r_min_value):
    res = 0
    if r_min_value >= 1:
        res = 1
    return res


'''
Calculates binary value for p_mim
'''
def p_prim_min(p_min_value):
    res = 0
    if p_min_value <= 0.5:
        res = 1
    return res


def print_metrics(filename):
    # Read the c betha residues from the pdb file
    positions = pdb_positions_reader.read_input_file(filename)

    # Calculate the centroid
    centroid = calculate_centroid(positions)

    # Calculate p_min
    p_min_val = p_min(positions,centroid)

    # Caculate r_min
    r_min_val = r_min(positions)

    # Calculate the groups that allows the correct calculus of the radios
    groups = divide_in_groups(positions)

    # calculate the sum of ratios
    sum_ratios = calculate_sr(groups)

    # Calculate the sum of logarithmic ratios
    sum_log_ratios = calculate_slr(groups)

    # Calculate binary value for sum of ratios
    binary_sum_ratios = r_prim_min(r_min_val)

    # Calculate binary value for p_min
    binary_p_min = p_prim_min(p_min_val)

    # .rjust(padding,' ')


    print("r_min\tp_min\tSR\tSLR\tr_prim_min\tp_prim_min")

    print(str(round(r_min_val,5))+"\t"+str(round(p_min_val,5))+"\t"+
          str(round(sum_ratios,5))
          +"\t"+str(round(sum_log_ratios,5))+"\t"+str(round(binary_sum_ratios,5))
          +"\t"+str(round(binary_p_min,5)))


# Main del programa

if filename != "":
    print_metrics(filename)
    '''
    positions = pdb_positions_reader.read_input_file(filename)


    print("Read: ", len(positions), " positions")

    print("centroid: ", calculate_centroid(positions))

    centroid = calculate_centroid(positions)

    p_min = p_min(positions,centroid)

    print("Pmin: ", p_min)


    print("total: ", len(positions))

    r_min_val = r_min(positions)

    print("Ratio: ", r_min_val)

    groups = divide_in_groups(positions)

    print("Number of groups: ",len(groups))

    print("RS: ",calculate_sr(groups))
    print("RLS: ",calculate_slr(groups))
    print("p_prim_min ", p_prim_min(p_min))
    print("r_prim_min ", r_prim_min(r_min_val))
    '''



else:
    print("No file!")
