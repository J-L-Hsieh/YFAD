from django.shortcuts import render

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from select import select
import sqlite3

import pandas as pd
import json

from django.views.decorators.csrf import csrf_exempt
import os
from yeast.testdb import DatabaseManager

from yeast.python.enrichment import enrichment_program
from yeast.python.yeast_associated import associated_analysis
from yeast.python.yeast_network import network
from yeast.python.yeast_modal import modal

import time

def home(request):
    return(render(request,'base.html',locals()))
def yeast(request):
    return(render(request,'browse.html',locals()))
def yeast_associated_base(request):
    return(render(request,'yeast_associated.html',locals()))
def yeast_name_base(request):
    return(render(request, 'yeast_name.html',locals()))

'''----------------------------------------------------------------------------'''
# def id_to_name(column_value, feature):
#     def test(x):
#         if x is None:
#             return x
#         x = eval(x)
#         # print(x)
#         # y = change_table.loc[x, :]
#         y = [change_table.loc[name]['%s_name'%feature] for name in x]
#         # print(y, type(y))


#         # print(type(y))
#         return y
#     # print(column_value)
#     column_name=[]
#     try:
#         connect = sqlite3.connect('db.sqlite3')
#         change_table = pd.read_sql("""SELECT * FROM %s_id_to_name""" %feature, connect, index_col='%s_id' %feature)
#     finally:
#         connect.close()
#     # print(type(column_value))
#     # column_value['%s_name' %feature] = column_value.apply(lambda x: change_table.loc[x, :])
#     # column_value['%s_name' %feature] = column_value.apply(test)
#     column_name = column_value.apply(test)

#     # print('-----')
#     # print(column_value)
#     # for value in column_value:
#     #     if value is None :
#     #         column_name.append(value)
#     #     else:
#     #         value = eval(value)
#             # print(change_table.loc[value, :].tolist())
#             # name = change_table.loc[value, :]
#     return column_name
#     pass

'''----------------------------------------------------------------------------'''


def yeast_browser(request):
    table_name = request.POST.get('first_feature')
    table_column = request.POST.get('other_feature')[:-1]
    search_feature = table_column.split(',')

    if table_name == 'Protein_Domain':
        select = """
            SELECT `%s(Queried)`, %s, %s_name FROM %s_1_to_10;
        """%(table_name, table_column, table_name, table_name)
    else:
        select = """
            SELECT `%s(Queried)`, %s FROM %s_1_to_10;
        """%(table_name, table_column, table_name)

    try:
        connect = sqlite3.connect('db.sqlite3')
        table = pd.read_sql(select, connect)

    finally:
        connect.close()


    '''---將Protein Domain id換成name 新增Detail欄位---'''

    if table_name == 'Protein_Domain':
        table ['Protein_Domain(Queried)'] = table['Protein_Domain_name']
        table = table.drop(columns = ['Protein_Domain_name'])
    else:
        table ['Detail'] = table['%s(Queried)'%table_name]

    '''---將Protein Domain id換成name 新增Detail欄位---'''

    table = table.fillna('-')
    table_columns = table.columns.values.tolist()
    columns = []
    for i in table_columns:
        columns.append({'title': i})

    table = table.values.tolist()
    response = {'table' : table, 'columns': columns}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''

def yeast_associated(request):

    table_name = request.POST.get('table_name')
    row_name = request.POST.get('row_name')
    print(table_name)
    try:
        connect = sqlite3.connect('db.sqlite3')
        select = """
            SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, count, SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
        """%(table_name, table_name, table_name, row_name)
        table = pd.read_sql('%s' %select, connect)

    finally:
        connect.close()
    '''----處理id 換成name----'''
    # if table_name =='Transcriptional_Regulation' or table_name =='Physical_Interaction' or table_name =='Genetic_Interaction' or table_name =='Protein_Domain':
        # table['%s(Queried)'%table_name] = table['%s_name'%table_name]
        # table = table.drop(columns=['%s_name'%table_name])

    '''---------------------刪除不必要的欄位------------------------'''
    associated_table = table.dropna(axis='columns')
    all_tables = associated_analysis(associated_table, table_name)
    network_data = network(associated_table, table_name)
    # associated_table = associated_table.drop(['count','SystematicName'],axis=1)
    #拿出column name
    associated_table = associated_table.to_html(index= None,classes="table table-bordered table-hover dataTable no-footer")
    associated_table = associated_table.replace('table','table id="associated_table"',1)
    response={'associated_table':associated_table , 'all_tables':all_tables, 'network_data':network_data}
    # response={'associated_table':associated_table , 'network_data':network_data}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''
def yeast_name(request):
    first_feature = request.POST.get('first_feature')
    second_feature = request.POST.get('second_feature')
    first_feature = first_feature.split('$')
    second_feature = second_feature.split('$')
    try:
        connect = sqlite3.connect('db.sqlite3')
        for  i in range(2):
            if i == 1:
                select = """
                    SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ('%s')
                """%(first_feature[0], first_feature[0], first_feature[1])
                first_table = pd.read_sql('%s' %select, connect)
            else:
                select = """
                    SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ('%s')
                """%(second_feature[0], second_feature[0], second_feature[1])
                second_table = pd.read_sql('%s' %select, connect)
    finally:
        connect.close()
    print(first_feature[1])
    first_names = eval(first_table.iat[0,1])
    second_names = eval(second_table.iat[0,1])
    first_name_table = pd.DataFrame(list(zip(first_names,['true']*len(first_names))),columns=['all','%s'%first_feature[1]])
    second_name_table = pd.DataFrame(list(zip(second_names,['true']*len(second_names))),columns=['all','%s'%second_feature[1]])
    both_contain = pd.merge(first_name_table, second_name_table, how="inner")

    union = pd.merge(first_name_table, second_name_table, how="outer")
    union = union.fillna('false')
    queried_contain = union[union["%s"%first_feature[1]] == 'false']
    second_contain = union[union["%s"%second_feature[1]] == 'false']

    both_contain = both_contain.fillna('false')
    both_contain = both_contain.to_html(index=None, classes='table table-bordered table-hover dataTable no-footer')
    both_contain = both_contain.replace('table', 'table id="both_name_table"')

    queried_contain = queried_contain.to_html(index=None, classes='table table-bordered table-hover dataTable no-footer')
    queried_contain = queried_contain.replace('table', 'table id="queried_table"')

    second_contain = second_contain.to_html(index=None, classes='table table-bordered table-hover dataTable no-footer ')
    second_contain = second_contain.replace('table', 'table id="second_table"')

    response = {'both_contain':both_contain, 'queried_contain':queried_contain, 'second_contain':second_contain}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''

def yeast_modal(request):
    evidence_table = modal(request)
    response ={'evidence_table':evidence_table}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''

def yeast_evidence(request):
    feature = request.POST.get('feature').split('%')
    print(feature)
    feature1 = feature[0]
    feature2 = feature[2]
    name1 = feature[1]
    name2 = feature[3]
    systematice_name = feature[4]
    connect = sqlite3.connect('db.sqlite3')

    if feature1 == 'false':
        pass
    else:
        if feature1 == 'Physical_Interaction':
            select1 = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN ('%s') AND `SystematicName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN ("%s") AND `SystematicName(Bait)` IN ("%s"));
            """%(feature1, systematice_name, name1, systematice_name, name1)

        elif feature1 == 'Genetic_Interaction':
            select1 = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN ('%s') AND `SystematicName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN ("%s") AND `SystematicName(Bait)` IN ("%s"));
            """%(feature1, systematice_name, name1, systematice_name, name1)

        else:
            select1 = """
                SELECT * FROM %s_evidence WHERE SystematicName IN ('%s') AND %s IN ("%s");
            """%(feature1, systematice_name, feature1, name1)

    if feature2 == 'false':
        pass

    else:
        if feature2 == 'Physical_Interaction':
            select2 = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN ('%s') AND `SystematicName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN ("%s") AND `SystematicName(Bait)` IN ("%s"));
            """%(feature2, systematice_name, name2, systematice_name, name2)


        elif feature2 == 'Genetic_Interaction':
            select2 = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN ('%s') AND `SystematicName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN ("%s") AND `SystematicName(Bait)` IN ("%s"));
            """%(feature2, systematice_name, name2, systematice_name, name2)

        else:
            select2 = """
                SELECT * FROM %s_evidence WHERE SystematicName IN ('%s') AND %s IN ("%s");
            """%(feature2, systematice_name, feature2, name2)


    try:

        if feature1 == 'false':
            feature1_table = 'no table'

        else:

            feature1_table = pd.read_sql(select1, connect)

            if feature1 == 'Physical_Interaction':
                feature1_table['SystematicName(Bait)']=feature1_table['Bait_link']
                feature1_table['SystematicName(Hit)']=feature1_table['Hit_link']
                feature1_table['StandardName(Bait)']=feature1_table['term_link']
                feature1_table = feature1_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

            elif feature1 == 'Genetic_Interaction':
                feature1_table['SystematicName(Bait)']=feature1_table['Bait_link']
                feature1_table['SystematicName(Hit)']=feature1_table['Hit_link']
                feature1_table['StandardName(Bait)']=feature1_table['term_link']
                feature1_table = feature1_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

            else:
                feature1_table['SystematicName']=feature1_table['gene_link']
                feature1_table['%s'%feature1]=feature1_table['term_link']
                feature1_table = feature1_table.drop(columns=['gene_link', 'term_link'])

            feature1_table = feature1_table.to_html(index= None, classes="table table-bordered table-hover dataTable no-footer",escape=False)
            feature1_table = feature1_table.replace('table', 'table id="feature1_table"', 1)

        if feature2 == 'false':
            feature2_table = 'no table'

        else:
            feature2_table = pd.read_sql(select2, connect)

            if feature2 == 'Physical_Interaction':
                feature2_table['SystematicName(Bait)']=feature2_table['Bait_link']
                feature2_table['SystematicName(Hit)']=feature2_table['Hit_link']
                feature2_table['StandardName(Bait)']=feature2_table['term_link']
                feature2_table = feature2_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

            elif feature2 == 'Genetic_Interaction':
                feature2_table['SystematicName(Bait)']=feature2_table['Bait_link']
                feature2_table['SystematicName(Hit)']=feature2_table['Hit_link']
                feature2_table['StandardName(Bait)']=feature2_table['term_link']
                feature2_table = feature2_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

            else:
                feature2_table['SystematicName']=feature2_table['gene_link']
                feature2_table['%s'%feature2]=feature2_table['term_link']
                feature2_table = feature2_table.drop(columns=['gene_link', 'term_link'])

            feature2_table = feature2_table.to_html(index= None, classes="table table-bordered table-hover dataTable no-footer",escape=False)
            feature2_table = feature2_table.replace('table', 'table id="feature2_table"', 1)

    finally:
        connect.close()


    response = {'feature1_table' : feature1_table, 'feature2_table' : feature2_table}
    return JsonResponse(response)
