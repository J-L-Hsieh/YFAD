import re
from unittest import result
import numpy as np
import pandas as pd
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


def enrichment_program(input_list,type_input,p):
    # https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html


    # ================================================================================================
    # ================================================================================================
    # print(input_list,type_input,p)
    print(input_list,type_input)
    input_list = eval(input_list)
    domain_data = pd.read_csv("/home/chunlin/Desktop/New/web_tool/protein_domain_map_id.csv")


    D = [6611 for n in range(len(domain_data))]
    C = list(domain_data["count"])

    B = [len(input_list) for n in range(len(domain_data))]

    list_A = list(range(len(domain_data)))
    A = list(range(len(domain_data)))
    test = list(range(len(domain_data)))


    for n in range(len(domain_data["protein_domain"])):
        list_A[n] = list(set(input_list)&set(domain_data["Systematic Name"][n].replace("[",'').replace("]",'').replace("'",'').replace(' ','').split(',')))
        A[n] = len(list_A[n])
        test[n] = fisher(A[n], B[n], C[n], D[n])




    cut_off = 0.01
    P_value_corr_FDR = multipletests(test,alpha=cut_off, method= "fdr_bh")
    P_value_corr_Bon = multipletests(test,alpha=cut_off, method= "bonferroni")

    result = pd.DataFrame({"Domain_id":domain_data["protein_domain"],"P-value":test,"FDR":P_value_corr_FDR[1],"Bonferroni":P_value_corr_Bon[1]})


    # print(len(P_value_corr_FDR))
    # print("[ [小於cut off 回傳True], [校正後的P-value], [corrected alpha for Sidak method], [corrected alpha for Bonferroni method] ]")
    # print(type_input)
    # print(result)
    if type_input == 'none':
        result = result[result["FDR"]<= float(p)]
        catch_num = 1
    elif type_input == 'FDR':
        result = result[result["FDR"]<= float(p)]
        catch_num = 2
    elif type_input == 'Bonferroni':
        result = result[result["Bonferroni"]<= float(p)]
        catch_num = 3
    index1 = list(result.index)
    analysis = []
    for i in index1 :
            analysis.append({'Domain Name':result.loc[i][0],'Expext Ratio':str(C[i])+'/'+str(D[i])+'('+str(C[i]/D[i]*100)[0:5]+'%)','Observed Ratio':str(A[i])+'/'+str(B[i])+'('+str(A[i]/B[i]*100)[0:5]+'%)','P-value':result.loc[i][catch_num]})
    index1 = list(result.index)
    # print(index1)
    input_true = ['true']*len(input_list)
    df_input = pd.DataFrame(list(zip(input_list,input_true)),columns=['all','input'])

    all_table = []
    for i in range(len(index1)):
        table = []
        df_input_copy = df_input.copy()
        table_true = ['true']*C[index1[i]]
        table_name = eval(domain_data.iat[index1[i],2])
        df_domain = pd.DataFrame(list(zip(table_name,table_true)),columns=['all','domain'])
        df_merge = pd.merge(df_domain,df_input_copy,how="outer")
        df_merge = df_merge.fillna('false')
        df_merge = df_merge.to_json(orient="records")
        # print(df_merge)
        all_table.append(df_merge)
    response = []
    response.append(analysis)
    response.append(all_table)
    return response
