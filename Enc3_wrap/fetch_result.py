from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import numpy as np
from itertools import product
import itertools
import numbers
from pgmpy.readwrite import BIFReader

from pgmpy.extern import tabulate

nodes = ['A', 'B', 'C'] # store the nodes in a list
simple_example = BayesianModel()
simple_example.add_nodes_from(nodes)

simple_example = BayesianModel([('A', 'B'),
                                ('B', 'C'),
                                ('A', 'C')])

# define individual
cpd_A = TabularCPD(variable = 'A', variable_card = 2, values = [[0.1, 0.9]])
# define the ones with evidence
# as explained in the pgmpy library, this matrix is transformed actually
cpd_B = TabularCPD(variable = 'B', variable_card = 2,
                   values = [[0.1, 0.2],
                             [0.9, 0.8]],
                   evidence = ['A'],
                   evidence_card = [2])

cpd_C = TabularCPD(variable = 'C', variable_card = 3,
                   values = [[0.7, 0.4, 1/3 , 0.2],
                             [0.0, 0.3, 1/3, 0.3],
                             [0.3, 0.3, 1/3, 0.5]],
                   evidence = ['A', 'B'],
                   evidence_card =[2, 2])

def row_to_col(l):
    result = []
    if l:
        for j in range(0, len(l[0])):
            result.append([e[j] for e in l])
    #print(result)
    return result


def mytable(cpt):
    evidence = cpt.variables[1:]
    evidence_card = cpt.cardinality[1:]
    reverse_ev = list(reversed(evidence))
    reverse_ec = list(reversed(evidence_card))
    #evidence_card.reverse()
    #print(reverse_ev, reverse_ec)
    headers_list = []
    #print(evidence, evidence_card)
    if reverse_ev:
        col_indexes = np.array(list(product(*[range(i) for i in reverse_ec])))
        #print(col_indexes)
        for i in range(len(reverse_ec)):
            column_header = [('{s}'.format(s = reverse_ev[i]), d) for d in col_indexes.T[i]]
            #column_header = [evidence[i]] + ['{s}_{d}'.format(s=evidence[i], d=d) for d in col_indexes.T[i]]
            headers_list.append(column_header)
            #headers_list.insert(0, column_header)
        #print('header', headers_list)
        # reverse here
        headers_list = list(reversed(headers_list))
        # for the variables
        variable_array = [('{s}'.format(s = cpt.variable),i) for i in range(cpt.variable_card)]
        #print(variable_array)

        ### you need to check the length of the evs, var array and values to make sure this work#######
        ### future implement
        evs = row_to_col(headers_list)


        values = cpt.get_values()

        mycpt = []
        for i in range(0, len(values)):
            mycpt = mycpt + [(variable_array[i][0], variable_array[i][1], j, x) for (j, x) in zip(evs, values[i]) ]

       # print('fectch', mycpt)
    else:
        # case without evidence
        # for the variables
        variable_array = [('{s}'.format(s=cpt.variable), i) for i in range(cpt.variable_card)]

        ### you need to check the length of the evs, var array and values to make sure this work#######
        ### future implement
        values = cpt.get_values()
        mycpt = []
        for i in range(0, len(values)):
            mycpt = mycpt + [(variable_array[i][0], variable_array[i][1], [], x) for x in values[i]]

        #print('fetch-', mycpt)

    return mycpt

    #labeled_rows = np.hstack((np.array(variable_array).T, cpt.get_values())).tolist()
    #print(labeled_rows)

reader = BIFReader('/Users/tianyangsun/Documents/Project/Github_repo/bifs/cancer.bif')
earthquake_model = reader.get_model()


# associate the tables with the networks
simple_example.add_cpds(cpd_A, cpd_B, cpd_C)
#print(earthquake_model.get_cpds('E'))
#mytable(earthquake_model.get_cpds('Cancer'))
