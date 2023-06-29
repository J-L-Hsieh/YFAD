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
from yeast.python.yeast_modal import p1_modal,p2_modal

import time

feature_name_dict = {"GO_MF(Queried)":"Queried term", "GO_BP(Queried)":"Queried Term", "GO_CC(Queried)":"Queried Term", "Protein_Domain(Queried)":"Queried Term", "Mutant_Phenotype(Queried)":"Queried Term", "Pathway(Queried)":"Queried Term", "Disease(Queried)":"Queried Term", "Transcriptional_Regulation(Queried)":"Queried Term", "Physical_Interaction(Queried)":"Queried Term", "Genetic_Interaction(Queried)":"Queried Term",
                    "GO_MF":"GO_MF", "GO_BP":"GO_BP", "GO_CC":"GO_CC", "Disease":"Disease", "Pathway":"Pathway", "Protein_Domain":"Protein Domain", "Mutant_Phenotype":"Mutant Phenotype", "Transcriptional_Regulation":"Transcriptional Regulation", "Physical_Interaction":"Physical Interaction", "Genetic_Interaction":"Genetic Interaction",
                    "SystematicName":"Systematic Name", "StandardName":"Strandard Name", "GeneDescription":"Gene Description", "EvidenceCode":"Evidence Code", "DomainDescription":"Domain Description", "StartCoordinate":"Start Coordinate", "EndCoordinate":"End Coordinate",
                    "SystematicName(Bait)":"Systematic Name(Bait)", "StandardName(Bait)":"Standard Name (Bait)", "SystematicName(Hit)":"Systematic Name (Hit)", "StandardName(Hit)":"Standard Name (Hit)", "ExperimentType":"Experiment Type"}

def base(request):
    return(render(request,'base.html',locals()))
def home(request):
    return(render(request,'home.html',locals()))
def download(request):
    return(render(request,'download.html',locals()))
def contact(request):
    return(render(request,'contact.html',locals()))
def help(request):
    return(render(request,'help.html',locals()))

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
#         # y = change_table.loc[x, :]
#         y = [change_table.loc[term_name]['%s_name'%feature] for term_name in x]


#         return y
#     column_name=[]
#     try:
#         connect = sqlite3.connect('db.sqlite3')
#         change_table = pd.read_sql("""SELECT * FROM %s_id_to_name""" %feature, connect, index_col='%s_id' %feature)
#     finally:
#         connect.close()
#     # column_value['%s_name' %feature] = column_value.apply(lambda x: change_table.loc[x, :])
#     # column_value['%s_name' %feature] = column_value.apply(test)
#     column_name = column_value.apply(test)

#     # for value in column_value:
#     #     if value is None :
#     #         column_name.append(value)
#     #     else:
#     #         value = eval(value)
#             # term_name = change_table.loc[value, :]
#     return column_name
#     pass

'''----------------------------------------------------------------------------'''


def yeast_browser(request):
    feature = request.POST.get('first_feature')
    table_column = request.POST.get('other_feature')[:-1]
    search_feature = table_column.split(',')

    if feature == 'Protein_Domain':
        select = """
            SELECT `%s(Queried)`, %s, %s_name FROM %s_10_length;
        """%(feature, table_column, feature, feature)
    else:
        select = """
            SELECT `%s(Queried)`, %s FROM %s_10_length;
        """%(feature, table_column, feature)

    try:
        connect = sqlite3.connect('db.sqlite3')
        table = pd.read_sql(select, connect)

    finally:
        connect.close()


    '''---將Protein Domain id換成name 新增Detail欄位---'''

    if feature == 'Protein_Domain':
        table ['Detail'] = table['%s(Queried)'%feature]
        table ['Protein_Domain(Queried)'] = table['Protein_Domain_name']
        table = table.drop(columns = ['Protein_Domain_name'])
    else:
        table ['Detail'] = table['%s(Queried)'%feature]

    '''---將Protein Domain id換成name 新增Detail欄位---'''
    table = table.fillna('-')
    # print(table.head(5))
    '''------tooltips------'''
    # count_name_table =  table[['count','SystematicName']]
    # table = table.drop(columns=['count', 'SystematicName'])
    '''------tooltips------'''

    table_columns = table.columns.values.tolist()
    columns = []
    for i in table_columns:
        columns.append({'title': i})

    '''------tooltips------'''
    # count_name_table = count_name_table.values.tolist()
    '''------tooltips------'''

    table = table.values.tolist()

    # response = {'table' : table, 'columns': columns, 'count_name_table':count_name_table}
    response = {'table' : table, 'columns': columns}

    return JsonResponse(response)
'''----------------------------------------------------------------------------'''
def yeast_p1_modal(request):

    evidence_table = p1_modal(request)
    # print(evidence_table)
    response = {"evidence_table" : evidence_table}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''
def yeast_network(request):
    feature = request.POST.get('feature')
    term_id = request.POST.get('id')
    term_name = request.POST.get('name')
    # print('-------------')
    # print(feature)
    try:
        connect = sqlite3.connect('db.sqlite3')
        if feature =="Protein_Domain":
            select = """
                SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Protein_Domain_id, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, count, SystematicName
                FROM %s_1_to_10
                WHERE `%s(Queried)` IN ("%s");
            """%(feature, feature, feature, term_id)
        else:
            select = """
                SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Protein_Domain_id, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, count, SystematicName
                FROM %s_1_to_10
                WHERE `%s(Queried)` IN ("%s");
            """%(feature, feature, feature, term_name)
        table = pd.read_sql('%s' %select, connect)

    finally:
        connect.close()

    # 刪除空值的欄位
    associated_table = table.dropna(axis='columns')


    column_name = associated_table.columns.values.tolist()
    for i in column_name:
        if i == 'Protein_Domain':
            associated_table = associated_table.drop(columns = ['Protein_Domain_id'])

    associated_table = associated_table.drop(columns = ['count', 'SystematicName'])

    associated_table['%s(Queried)'%feature] = term_name

    network_data = network(associated_table, feature)

    column_order = associated_table.columns.values.tolist()
    column_order = column_order[0:]

    response={'network_data':network_data,"column_order":column_order}

    return JsonResponse(response)

def yeast_associated(request):

    feature = request.POST.get('feature')
    term_id = request.POST.get('id')
    term_name = request.POST.get('name')

    try:
        connect = sqlite3.connect('db.sqlite3')
        if feature == "Protein_Domain":
            select = """
                SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Protein_Domain_id, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, count, SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
            """%(feature, feature, feature, term_id)
        else:
            select = """
                SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Protein_Domain_id, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, count, SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
            """%(feature, feature, feature, term_name)
        table = pd.read_sql('%s' %select, connect)

        if feature == "Protein_Domain":
            select = """
                SELECT * FROM %s_10_length WHERE `%s(Queried)` IN ("%s");
            """%(feature, feature, term_id)
        else:
            select = """
                SELECT * FROM %s_10_length WHERE `%s(Queried)` IN ("%s");
            """%(feature, feature, term_name)

        number_table =  pd.read_sql('%s' %select, connect)

        if feature == "Protein_Domain":
            number_table["Protein_Domain(Queried)"] = number_table["Protein_Domain_name"]
            number_table = number_table.drop(columns=["Protein_Domain_name"])
        elif feature == "Transcriptional_Regulation":
            number_table = number_table.drop(columns=["Transcriptional_Regulation_id"])

        number_table = number_table.mask(number_table == 0).dropna(axis=1)
        # print(number_table)

    finally:
        connect.close()
    '''----處理id 換成name----'''
    # if feature =='Transcriptional_Regulation' or feature =='Physical_Interaction' or feature =='Genetic_Interaction' or feature =='Protein_Domain':
        # table['%s(Queried)'%feature] = table['%s_name'%feature]
        # table = table.drop(columns=['%s_name'%feature])

    # 刪除空值的欄位
    associated_table = table.dropna(axis='columns')

    all_tables = associated_analysis(associated_table, feature, term_name)

    column_name = associated_table.columns.values.tolist()
    for i in column_name:
        if i == 'Protein_Domain':
            associated_table = associated_table.drop(columns = ['Protein_Domain_id'])

    associated_table = associated_table.drop(columns = ['count', 'SystematicName'])

    associated_table['%s(Queried)'%feature] = term_name

    # network_data = network(associated_table, feature)
    #拿出column term_name
    # associated_table = associated_table.to_html(index= None,classes="table table-bordered table-hover dataTable no-footer ")
    # associated_table = associated_table.replace('table','table id="associated_table"',1)
    number_table = number_table.rename(columns=feature_name_dict)
    number_table = number_table.to_html(index= None,classes="table table-bordered table-hover dataTable no-footer ")
    number_table = number_table.replace('table','table id="associated_table"',1)

    response={'associated_table':number_table , 'all_tables':all_tables}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''
def yeast_name(request):
    first_feature = request.POST.get('first_feature')
    second_feature = request.POST.get('second_feature')
    first_feature = first_feature.split('*')
    second_feature = second_feature.split('*')
    print(second_feature, first_feature)

    try:
        connect = sqlite3.connect('db.sqlite3')
        db_cursor = connect.cursor()

        for  i in range(2):
            if i == 1:
                select = """
                    SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s")
                """%(first_feature[0], first_feature[0], first_feature[1])
                # print(select)
                first_table = pd.read_sql('%s' %select, connect)
            else:
                select = """
                    SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s")
                """%(second_feature[0], second_feature[0], second_feature[1])
                second_table = pd.read_sql('%s' %select, connect)


        first_names = eval(first_table.iat[0,1])
        second_names = eval(second_table.iat[0,1])
        first_names_for_evidence = tuple(first_names)
        second_names_for_evidence = tuple(second_names)

        # sql_string = """
        #     SELECT  SystematicName, StrandardName, GeneDessciption 
        #     FROM %s_evidence 
        #     WHERE `SystematicName` IN `%s`
        # """%(first_feature[0], first_names_for_evidence)
        # first_description_table = pd.read_sql('%s'%sql_string, connect)
        # print(first_description_table)


        if first_feature[0]=='Protein_Domain':
            select = """
                SELECT Protein_Domain_name FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
            """%(first_feature[0], first_feature[0], first_feature[1])
            first_pd_id = db_cursor.execute(select).fetchone()
            first_pd_id = first_pd_id[0]
            print(first_pd_id,'-----')
        if second_feature[0]=='Protein_Domain':
            select = """
                SELECT Protein_Domain_name FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
            """%(second_feature[0], second_feature[0], second_feature[1])
            second_pd_id = db_cursor.execute(select).fetchone()
            second_pd_id = second_pd_id[0]
    finally:
        connect.close()
    print(first_table)




    first_name_table = pd.DataFrame(list(zip(first_names,['true']*len(first_names))),columns=['all','%s'%first_feature[2]])
    second_name_table = pd.DataFrame(list(zip(second_names,['true']*len(second_names))),columns=['all','%s'%second_feature[2]])
    both_contain = pd.merge(first_name_table, second_name_table, how="inner")

    union = pd.merge(first_name_table, second_name_table, how="outer")
    union = union.fillna('false')

    second_contain = union[union["%s"%first_feature[2]] == 'false']
    queried_contain = union[union["%s"%second_feature[2]] == 'false']

    if first_feature[0]=='Protein_Domain':
        both_contain = both_contain.rename(columns={'%s'%first_feature[1]:'%s'%first_pd_id})
        second_contain = second_contain.rename(columns={'%s'%first_feature[1]:'%s'%first_pd_id})
        queried_contain = queried_contain.rename(columns={'%s'%first_feature[1]:'%s'%first_pd_id})

    if second_feature[0]=='Protein_Domain':
        both_contain = both_contain.rename(columns={"%s"%second_feature[1]:"%s"%second_pd_id})
        second_contain = second_contain.rename(columns={"%s"%second_feature[1]:"%s"%second_pd_id})
        queried_contain = queried_contain.rename(columns={"%s"%second_feature[1]:"%s"%second_pd_id})


    both_contain = both_contain.fillna('false')
    both_contain = both_contain.to_html(index=None, classes='table table-bordered table-hover dataTable no-footer')
    both_contain = both_contain.replace('table', 'table id="both_name_table"')
    print(second_contain)

    second_contain = second_contain.to_html(index=None, classes='table table-bordered table-hover dataTable no-footer')
    second_contain = second_contain.replace('table', 'table id="second_table"')
    print("queried_contain",queried_contain)

    queried_contain = queried_contain.to_html(index=None, classes='table table-bordered table-hover dataTable no-footer ')
    queried_contain = queried_contain.replace('table', 'table id="queried_table"')

    response = {'both_contain':both_contain, 'second_contain':second_contain, 'queried_contain':queried_contain}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''

def yeast_modal(request):
    evidence_table = p2_modal(request)
    response ={'evidence_table':evidence_table}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''
def Protein_Domain_href(term_id, term_name):
    return "<a href='https://www.ebi.ac.uk/interpro/entry/pfam/%s/' target='_blank'>%s</a>"%(term_id, term_name)

def yeast_evidence(request):
    feature = request.POST.get('feature').split('%')
    print(feature)
    feature1 = feature[0]
    feature2 = feature[3]
    id_query = feature[1]
    name_query = feature[2]
    id_associated = feature[4]
    name_associated = feature[5]
    systematice_name = feature[6]
    connect = sqlite3.connect('db.sqlite3')
    print(feature)
    if feature1 == 'false':
        pass
    else:
        if feature1 == 'Physical_Interaction':
            select1 = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN ("%s") AND `StandardName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN ("%s") AND `StandardName(Bait)` IN ("%s"));
            """%(feature1, systematice_name, id_query, systematice_name, id_query)

        elif feature1 == 'Genetic_Interaction':
            select1 = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN ("%s") AND `StandardName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN ("%s") AND `StandardName(Bait)` IN ("%s"));
            """%(feature1, systematice_name, id_query, systematice_name, id_query)
        elif feature1 == 'Transcriptional_Regulation':
            select1 = """
                SELECT * FROM %s_evidence WHERE SystematicName IN ("%s") AND StandardName IN ("%s");
            """%(feature1, systematice_name, id_query)
        else:
            select1 = """
                SELECT * FROM %s_evidence WHERE SystematicName IN ("%s") AND %s IN ("%s");
            """%(feature1, systematice_name, feature1, id_query)

    if feature2 == 'false':
        pass

    else:
        if feature2 == 'Physical_Interaction':
            select2 = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN ("%s") AND `StandardName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN ("%s") AND `StandardName(Bait)` IN ("%s"));
            """%(feature2, systematice_name, id_associated, systematice_name, id_associated)


        elif feature2 == 'Genetic_Interaction':
            select2 = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN ("%s") AND `StandardName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN ("%s") AND `StandardName(Bait)` IN ("%s"));
            """%(feature2, systematice_name, id_associated, systematice_name, id_associated)
        elif feature2 == 'Transcriptional_Rugulation':
            select2 = """
                SELECT * FROM %s_evidence WHERE SystematicName IN ("%s") AND %s IN ("%s");
            """%(feature2, systematice_name, feature2, id_associated)
        else:
            select2 = """
                SELECT * FROM %s_evidence WHERE SystematicName IN ("%s") AND %s IN ("%s");
            """%(feature2, systematice_name, feature2, id_associated)

    print(select1)
    try:

        if feature1 == 'false':
            feature1_table = 'no table'

        else:

            feature1_table = pd.read_sql(select1, connect)

            if feature1 == 'Physical_Interaction':
                feature1_table['SystematicName(Bait)']=feature1_table['Bait_link']
                feature1_table['SystematicName(Hit)']=feature1_table['Hit_link']
                feature1_table = feature1_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

            elif feature1 == 'Genetic_Interaction':
                feature1_table['SystematicName(Bait)']=feature1_table['Bait_link']
                feature1_table['SystematicName(Hit)']=feature1_table['Hit_link']
                feature1_table = feature1_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

            elif feature1 == 'Protein_Domain':
                feature1_table['SystematicName']=feature1_table['gene_link']
                feature1_table = feature1_table.drop(columns=['gene_link', 'term_link'])
                feature1_table["Protein_Domain"] = feature1_table.apply(lambda x :Protein_Domain_href(x['Protein_Domain'], name_query), axis=1)

            elif feature1 =="GO_MF" or feature1 =="GO_BP" or feature1 =="GO_CC":
                feature1_table["EvidenceCode"] = feature1_table.apply(lambda x: x["EvidenceCode"].replace('<a ', '<a target="_blank"'), axis=1)
                feature1_table['SystematicName']=feature1_table['gene_link']
                feature1_table['%s'%feature1]=feature1_table['term_link']

                feature1_table = feature1_table.drop(columns=['gene_link', 'term_link'])

                
            else:
                feature1_table['SystematicName']=feature1_table['gene_link']
                feature1_table['%s'%feature1]=feature1_table['term_link']

            feature1_table = feature1_table.rename(columns=feature_name_dict)
            feature1_table = feature1_table.to_html(index= None, classes="table table-bordered table-hover dataTable no-footer",escape=False)
            feature1_table = feature1_table.replace('table', 'table id="feature1_table"', 1)

        if feature2 == 'false':
            feature2_table = 'no table'

        else:
            feature2_table = pd.read_sql(select2, connect)

            if feature2 == 'Physical_Interaction':
                feature2_table['SystematicName(Bait)']=feature2_table['Bait_link']
                feature2_table['SystematicName(Hit)']=feature2_table['Hit_link']
                feature2_table = feature2_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

            elif feature2 == 'Genetic_Interaction':
                feature2_table['SystematicName(Bait)']=feature2_table['Bait_link']
                feature2_table['SystematicName(Hit)']=feature2_table['Hit_link']
                feature2_table = feature2_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

            elif feature2 == 'Protein_Domain':
                feature2_table['SystematicName']=feature2_table['gene_link']
                feature2_table = feature2_table.drop(columns=['gene_link', 'term_link'])
                feature2_table["Protein_Domain"] = feature2_table.apply(lambda x :Protein_Domain_href(x['Protein_Domain'], name_query), axis=1)

            elif feature2 =="GO_MF" or feature2 =="GO_BP" or feature2 =="GO_CC":
                feature2_table["EvidenceCode"] = feature2_table.apply(lambda x: x["EvidenceCode"].replace('<a ', '<a target="_blank"'), axis=1)
                feature2_table['SystematicName']=feature2_table['gene_link']
                feature2_table['%s'%feature2]=feature2_table['term_link']
                
                feature2_table = feature2_table.drop(columns=['gene_link', 'term_link'])

            else:
                feature2_table['SystematicName']=feature2_table['gene_link']
                feature2_table['%s'%feature2]=feature2_table['term_link']
                feature2_table = feature2_table.drop(columns=['gene_link', 'term_link'])

            feature2_table = feature2_table.rename(columns=feature_name_dict)
            feature2_table = feature2_table.to_html(index= None, classes="table table-bordered table-hover dataTable no-footer",escape=False)
            feature2_table = feature2_table.replace('table', 'table id="feature2_table"', 1)
    finally:
        connect.close()
    response = {'feature1_table' : feature1_table, 'feature2_table' : feature2_table}
    return JsonResponse(response)
