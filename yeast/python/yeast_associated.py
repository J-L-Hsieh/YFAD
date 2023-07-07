import pandas as pd
import sqlite3

def round_float(p_value):
    try:
        # print(type(p_value))
        p_value = str(p_value).split('e')
        p_value[0] = round(float(p_value[0]),2)
        p_value_round_2 = str(p_value[0]) + 'e' + str(p_value[1])
        return p_value_round_2
    except:
        return p_value

def associated_analysis(associated_table, table_name, name):
    associated_table = pd.DataFrame(associated_table)
    '''-------------------------queried feature data---------------------'''
    # print(associated_table)
    queried_feature = associated_table.at[0,'%s(Queried)'%table_name]
    queried_count = associated_table.at[0,'count']
    queried_name = associated_table.at[0,'SystematicName']

    '''------------------------------------------------------------------'''

    associated_table = associated_table.drop(columns = ['%s(Queried)' %table_name, 'count', 'SystematicName'])
    features = associated_table.columns.values.tolist()

    '''------------------回傳資料為各個table及column的順序--------------------'''
    for feature in features:
        if feature == 'Protein_Domain':
            protein_name = eval(associated_table.at[0, 'Protein_Domain'])
            associated_table['Protein_Domain'] = associated_table['Protein_Domain_id']
            features.remove('Protein_Domain_id')

    response ={}
    try:
        connect = sqlite3.connect('db.sqlite3')

        for feature in features:
            term_id = eval(associated_table.at[0,'%s' %feature])


            feature_name = '\",\"'.join(term_id)
            # print(len(feature_name.split(",")))
            select  = """
                SELECT `%s(Queried)`,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
            """%(feature, feature, feature, feature_name)
            feature_systematic = pd.read_sql('%s' %select, connect)
            print(select)
            feature_systematic["Term A (The Queried Term)"] = queried_feature
            feature_systematic['N<sub>A</sub>'] = str(len(eval(queried_name)))
            feature_systematic["N<sub>B</sub>"] = feature_systematic.apply(lambda x: str(len(eval(x['SystematicName']))), axis=1)
            feature_systematic['N<sub>AB</sub>'] = feature_systematic.apply(lambda x: intersection(queried_name, x['SystematicName']), axis=1)
            feature_systematic['Corrected p-value'] = feature_systematic.apply(lambda x: yeast_enrichment(queried_name, x['SystematicName']), axis=1)

            if feature == 'Protein_Domain':
                term_b = [p_name+'*'+p_id for p_name, p_id in zip(protein_name, term_id)]
                feature_systematic["Term B (The Associated Term)"] = term_b
            else:
                print(len(feature_systematic))
                print(len(term_id))
                term_b = [name+'*'+name for name in term_id]
                feature_systematic["Term B (The Associated Term)"] = term_b
            # print(feature_systematic, '--------')

            feature_systematic = feature_systematic.rename(columns={'%s(Queried)'%feature:'Detail'})

            feature_systematic = feature_systematic.drop(['SystematicName'], axis=1)
            feature_systematic = feature_systematic[['Term A (The Queried Term)', 'Term B (The Associated Term)', 'Corrected p-value', 'N<sub>A</sub>', 'N<sub>B</sub>', 'N<sub>AB</sub>', 'Detail']]

            feature_systematic = feature_systematic.sort_values(by=['Corrected p-value'], ascending=True)
            # print(feature_systematic)
            feature_systematic['Corrected p-value'] = feature_systematic.apply(lambda x:("{:.2e}".format(x['Corrected p-value'])), axis=1)

            print(feature_systematic)

            feature_systematic = feature_systematic.to_html(index= None,classes="table table-bordered table-hover dataTable no-footer", escape=False)
            feature_systematic = feature_systematic.replace('table', 'table id="%s_table"'%feature, 1)
            response['%s'%feature] = feature_systematic

            column_order = features[0:]
            response['column_order'] = column_order
    finally:
        connect.close()
    return response

def intersection(queried_name,domain_name):

    queried_name = eval(queried_name)
    domain_name = eval(domain_name)
    list_A = list(set(queried_name)&set(domain_name))
    # print(list_A)
    A = len(list_A)
    # B = len(queried_name)
    return str(A)

'''-----------------------------------------yeast enrichment---------------------------------------'''
import scipy.stats
from statsmodels.stats.multitest import multipletests

def fisher(A,B,C,D) :

    T = int(A)      #交集數         1      剩下的交集處
    S = int(B)      #輸入 genes數   18    輸入一總數
    G = int(C)      #genes 樣本數   1117   篩選的樣本
    F = int(D)      #總 genes數     6572  輸入二總數

    S_T = S-T
    G_T = G-T
    F_G_S_T = F-G-S+T

    oddsratio, pvalue_greater = scipy.stats.fisher_exact( [ [T,G_T] , [S_T,F_G_S_T]] ,'greater')
    oddsratio, pvalue_less = scipy.stats.fisher_exact( [ [T,G_T] , [S_T,F_G_S_T]] ,'less')

    return pvalue_greater


def yeast_enrichment(queried_name,domain_name):

    queried_name = eval(queried_name)
    domain_name = eval(domain_name)


    D = 6611
    C = len(domain_name)

    B = len(queried_name)



    list_A = list(set(queried_name)&set(domain_name))
    A = len(list_A)
    test = fisher(A, B, C, D)



    cut_off = 0.01
    P_value_corr_FDR = multipletests(test,alpha=cut_off, method= "fdr_bh")
    P_value_corr_Bon = multipletests(test,alpha=cut_off, method= "bonferroni")


    result = pd.DataFrame({"P-value":test, "FDR":P_value_corr_FDR[1], "Bonferroni":P_value_corr_Bon[1]})
    result = result[result["FDR"]<=0.01]
    # print(type(result.iat[0,1]))
    # response = []
    # response.extend([str(A)+'/'+str(B),str(C)+'/'+str(D),result.iat[0,1]])
    # reponse = "{:.2e}".format(result.iat[0,1])
    return result.iat[0,1]
