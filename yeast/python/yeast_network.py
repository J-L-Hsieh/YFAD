import pandas as pd
import sqlite3


color_dict = {'GO_MF':'darkseagreen' ,'GO_BP':'darksalmon' ,'GO_CC':'lightskyblue' ,'Protein_Domain':'plum' ,'Mutant_Phenotype':'coral' ,'Pathway':'grey' ,'Disease':'mistyrose' ,'Transcriptional_Regulation':'deepskyblue' ,'Physical_Interaction':'gold','Genetic_Interaction':'teal',
            'GO_MF(Queried)':'darkseagreen' ,'GO_BP(Queried)':'darksalmon' ,'GO_CC(Queried)':'lightskyblue' ,'Protein_Domain(Queried)':'plum' ,'Mutant_Phenotype(Queried)':'coral' ,'Pathway(Queried)':'grey' ,'Disease(Queried)':'mistyrose' ,'Transcriptional_Regulation(Queried)':'deepskyblue' ,'Physical_Interaction(Queried)':'gold','Genetic_Interaction(Queried)':'teal'}

def network(associated_table):
    associated_table = pd.DataFrame(associated_table)
    '''-------------------------queried feature data---------------------'''
    queried_feature = associated_table.iat[0,0]
    queried_count = associated_table.iat[0,1]
    queried_name = associated_table.iat[0,2]
    '''------------------------------------------------------------------'''
    associated_table.drop(associated_table.columns[[1,2]],axis=1,inplace=True)
    column_name = associated_table.columns.values.tolist()
    column_order = column_name[1:]
    associated_table.drop(associated_table.columns[[0]],axis=1,inplace=True)
    nodes = []
    edges = []
    color = color_dict['%s'%column_name[0]]
    nodes.append({"id":'0', 'group':queried_feature, "label":queried_feature, 'color':color, 'shape':'box', 'type':'main'})
    '''---------------------------------加入每個特徵-----------------------------'''
    for i in range(len(column_order)):
        id_num = i+1
        color = color_dict['%s'%column_order[i]]
        # nodes.append({"id":'%s' %id_num ,"label":column_order[i], 'color':color})
        # edges.append({'from':'0','to':id_num})

        domain_name = eval(associated_table.iat[0,i])
        # print(domain_name)
        '''------------------------------加入個特徵下的各個類別-------------------------'''

        for j in range(len(domain_name)):
            nodes.append({'id':'{feature}_{name_in_feature}'.format(feature = id_num, name_in_feature = j), 'group':domain_name[j], 'label':domain_name[j], 'color':color, 'type':column_order[i]})
            edges.append({'from':0, 'to':'{feature}_{name_in_feature}'.format(feature = id_num, name_in_feature = j),'color':color})



    response = {'nodes':nodes, 'edges':edges}

    return response