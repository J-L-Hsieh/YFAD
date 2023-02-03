import pandas as pd
import sqlite3


def associated_analysis(associated_table,table_name):
    associated_table = pd.DataFrame(associated_table)
    '''-------------------------queried feature data---------------------'''
    # print(associated_table)
    queried_feature = associated_table.at[0,'%s(Queried)'%table_name]
    queried_count = associated_table.at[0,'count']
    queried_name = associated_table.at[0,'SystematicName']

    '''------------------------------------------------------------------'''
    # associated_table.drop(associated_table.columns[['%s' %table_name, 'count', 'SystematicName']],axis=1,inplace=True)
    associated_table = associated_table.drop(columns = ['%s(Queried)' %table_name, 'count', 'SystematicName'])

    column_name = associated_table.columns.values.tolist()
    column_order = column_name[0:]
    print(column_order)
    '''------------------回傳資料為各個table及column的順序--------------------'''
    response ={}
    for i in column_name:
        domain_name = eval(associated_table.at[0,'%s' %i])
        table = []
        if i == 'Protein_Domain_id':
            pass
        else:
            for j in domain_name:
                try:
                    connect = sqlite3.connect('db.sqlite3')
                    db_cursor = connect.cursor()
                    select = """
                        SELECT SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
                    """%(i, i, j)
                    domain_name = db_cursor.execute(select).fetchone()
                    print(domain_name)
                    domain_name = domain_name[0]
                    # print(domain_name)
                    # print(queried_name)
                    result_list = yeast_enrichment(queried_name,domain_name)
                    # print(result_list)
                    result_list.insert(0,queried_feature)
                    result_list.insert(1,j)
                    result_list.insert(7,'-')
                    #將每一列的資訊放進同一個list中,之後做成datatable
                    table.append(result_list)
                finally:
                    connect.close()
            columns_title = ['Queried %s Term(A)' %table_name,'Associated %s Term(B)' %i,'Observed Ratio','Expext Ratio','Signficance of Associated(p-value)','Detail']
            df_tables = pd.DataFrame(table,columns=columns_title).to_html(index= None,classes="table table-bordered table-hover dataTable no-footer")
            df_tables =df_tables.replace('table', 'table id="%s_table"'%i, 1)
            response['%s'%i] = df_tables
            response['column_order'] = column_order
    return response


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
    print(result)
    response = []
    response.extend([str(A)+'/'+str(B),str(C)+'/'+str(D),result.iat[0,1]])

    return response
