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
from yeast.python.yeast_modal import p1_modal, p2_modal

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


def yeast_browser(request):
    feature = request.POST.get('query_feature')
    table_column = request.POST.get('other_feature')[:-1]
    search_feature = table_column.split(',')

    browser_feature_name_dict = {"GO_MF(Queried)":"GO_MF (Queried)", "GO_BP(Queried)":"GO_BP (Queried)", "GO_CC(Queried)":"GO_CC (Queried)", "Protein_Domain(Queried)":"Protein_Domain (Queried)", "Mutant_Phenotype(Queried)":"Mutant_Phenotype (Queried)", "Pathway(Queried)":"Pathway (Queried)", "Disease(Queried)":"Disease (Queried)", "Transcriptional_Regulation(Queried)":"Transcriptional_Regulation (Queried)", "Physical_Interaction(Queried)":"Physical_Interaction (Queried)", "Genetic_Interaction(Queried)":"Genetic_Interaction (Queried)",
                    "GO_MF":"GO_MF", "GO_BP":"GO_BP", "GO_CC":"GO_CC", "Disease":"Disease", "Pathway":"Pathway", "Protein_Domain":"Protein Domain", "Mutant_Phenotype":"Mutant Phenotype", "Transcriptional_Regulation":"Transcriptional Regulation", "Physical_Interaction":"Physical Interaction", "Genetic_Interaction":"Genetic Interaction", "Detail":"Detail"
    }
    if feature == 'Protein_Domain':
        select = """
            SELECT `%s(Queried)`, %s, %s_name FROM `%s_10_length`;
        """%(feature, table_column, feature, feature)

    elif feature == 'Transcriptional_Regulation':
        select = """
            SELECT `%s(Queried)`, %s, %s_id FROM `%s_10_length`;
        """%(feature, table_column, feature, feature)

    else:
        select = """
            SELECT `%s(Queried)`, %s FROM `%s_10_length`;
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

    elif feature == 'Transcriptional_Regulation':
        table.rename({'Transcriptional_Regulaiton_id':'Detail'})

    else:
        table ['Detail'] = table['%s(Queried)'%feature]

    table = table.fillna('-')

    table_columns = table.columns.values.tolist()
    columns = []
    for i in table_columns:
        columns.append({'title': browser_feature_name_dict[i]})


    table = table.values.tolist()

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
    feature_query = request.POST.get('query')
    term_id = request.POST.get('id')
    term_name = request.POST.get('name')
    # print('-------------')
    # print(feature_query)
    try:
        connect = sqlite3.connect('db.sqlite3')
        if feature_query =="Protein_Domain":
            select = """
                SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Protein_Domain_id, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, count, SystematicName
                FROM %s_1_to_10
                WHERE `%s(Queried)` IN ("%s");
            """%(feature_query, feature_query, feature_query, term_id)
        else:
            select = """
                SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Protein_Domain_id, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, count, SystematicName
                FROM %s_1_to_10
                WHERE `%s(Queried)` IN ("%s");
            """%(feature_query, feature_query, feature_query, term_name)
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

    associated_table['%s(Queried)'%feature_query] = term_name

    network_data = network(associated_table, feature_query)

    column_order = associated_table.columns.values.tolist()
    column_order = column_order[0:]

    response={'network_data':network_data,"column_order":column_order}

    return JsonResponse(response)

def yeast_associated(request):

    feature_query = request.POST.get('query')
    term_id = request.POST.get('id')
    term_name = request.POST.get('name')

    try:
        connect = sqlite3.connect('db.sqlite3')
        if feature_query == "Protein_Domain":
            select = """
                SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Protein_Domain_id, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, count, SystematicName
                FROM %s_1_to_10
                WHERE `%s(Queried)` IN ("%s");
            """%(feature_query, feature_query, feature_query, term_id)

        else:
            select = """
                SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Protein_Domain_id, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Transcriptional_Regulation_name, Physical_Interaction, Genetic_Interaction, count, SystematicName
                FROM %s_1_to_10
                WHERE `%s(Queried)` IN ("%s");
            """%(feature_query, feature_query, feature_query, term_name)

        table = pd.read_sql('%s' %select, connect)

        if feature_query == "Protein_Domain":
            select = """
                SELECT * FROM %s_10_length WHERE `%s(Queried)` IN ("%s");
            """%(feature_query, feature_query, term_id)
        else:
            select = """
                SELECT * FROM %s_10_length WHERE `%s(Queried)` IN ("%s");
            """%(feature_query, feature_query, term_name)

        number_table =  pd.read_sql('%s' %select, connect)

        if feature_query == "Protein_Domain":
            number_table["Protein_Domain(Queried)"] = number_table["Protein_Domain_name"]
            number_table = number_table.drop(columns=["Protein_Domain_name"])
        elif feature_query == "Transcriptional_Regulation":
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

    all_tables = associated_analysis(associated_table, feature_query, term_name)

    column_name = associated_table.columns.values.tolist()
    for i in column_name:
        if i == 'Protein_Domain':
            associated_table = associated_table.drop(columns = ['Protein_Domain_id'])
        elif i== "Transcriptional_Regulation":
            associated_table = associated_table.drop( columns = ['Transcriptional_Regulation'])
            associated_table = associated_table.rename(columns={'Transcriptional_Regulation_name':'Transcriptional_Regulation'})

    associated_table = associated_table.drop(columns = ['count', 'SystematicName'])

    associated_table['%s(Queried)'%feature_query] = term_name

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
    query_feature = request.POST.get('query_feature')
    associate_feature = request.POST.get('associate_feature')
    query_feature = query_feature.split('*')
    associate_feature = associate_feature.split('*')
    # print(associate_feature, query_feature)

    feature_query = query_feature[0]
    id_query = query_feature[1]
    name_query = query_feature[2]
    feature_associated = associate_feature[0]
    id_associated = associate_feature[1]
    name_associated = associate_feature[2]

    try:
        connect = sqlite3.connect('db.sqlite3')
        db_cursor = connect.cursor()


        if feature_query == 'Transcriptional_Regulation':
            select = """
                SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s")
            """%(feature_query, feature_query, name_query)
            # print(select)

        else:
            select = """
                SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s")
            """%(feature_query, feature_query, id_query)
            # print(select)

        first_table = pd.read_sql('%s' %select, connect)

        if feature_associated == 'Transcriptional_Regulation':
            select = """
                SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s")
            """%(feature_associated, feature_associated, name_associated)
        else:
            select = """
                SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s")
            """%(feature_associated, feature_associated, id_associated)
        second_table = pd.read_sql('%s' %select, connect)

        first_names = eval(first_table.iat[0,1])
        second_names = eval(second_table.iat[0,1])
        first_names_for_evidence = tuple(first_names)
        second_names_for_evidence = tuple(second_names)
        # print(len(first_names), '------', len(second_names))



        if feature_query == 'Physical_Interaction':
            select1 = """
                SELECT DISTINCT `SystematicName(Bait)`, `Bait_link`, `StandardName(Bait)` FROM %s_evidence WHERE `SystematicName(Bait)` IN %s AND `StandardName(Hit)` IN ('%s') OR (`SystematicName(Hit)` IN %s AND `StandardName(Bait)` IN ('%s'));
            """%(feature_query, first_names_for_evidence, id_query, first_names_for_evidence, id_query)

        elif feature_query == 'Genetic_Interaction':
            select1 = """
                SELECT DISTINCT `SystematicName(Bait)`, `Bait_link`, `StandardName(Bait)` FROM %s_evidence WHERE `SystematicName(Bait)` IN %s AND `StandardName(Hit)` IN ('%s') OR (`SystematicName(Hit)` IN %s AND `StandardName(Bait)` IN ('%s'));
            """%(feature_query, first_names_for_evidence, id_query, first_names_for_evidence, id_query)

        elif feature_query == 'Transcriptional_Regulation':
            select1 = """
                SELECT DISTINCT `SystematicName`, `gene_link`, `StandardName` FROM %s_evidence WHERE `SystematicName` IN %s AND `Transcriptional_Regulation` IN ("%s");
            """%(feature_query, first_names_for_evidence, id_query)
            # print(select1)
        else:
            select1 = """
                SELECT DISTINCT `SystematicName`, `gene_link`, `StandardName` FROM %s_evidence WHERE `SystematicName` IN %s AND `%s` IN ("%s");
            """%(feature_query, first_names_for_evidence, feature_query, id_query)

        evidence_table_query = pd.read_sql('%s' %select1, connect)
        # print(evidence_table_query)

        if feature_associated == 'Physical_Interaction':
            select2 = """
                SELECT DISTINCT `SystematicName(Bait)`, `Bait_link`, `StandardName(Bait)` FROM %s_evidence WHERE `SystematicName(Bait)` IN %s AND `StandardName(Hit)` IN ('%s') OR (`SystematicName(Hit)` IN %s AND `StandardName(Bait)` IN ('%s'));
            """%(feature_associated, second_names_for_evidence, id_associated, second_names_for_evidence, id_associated)

        elif feature_associated == 'Genetic_Interaction':
            select2 = """
                SELECT DISTINCT `SystematicName(Bait)`, `Bait_link`, `StandardName(Bait)` FROM %s_evidence WHERE `SystematicName(Bait)` IN %s AND `StandardName(Hit)` IN ('%s') OR (`SystematicName(Hit)` IN %s AND `StandardName(Bait)` IN ('%s'));
            """%(feature_associated, second_names_for_evidence, id_associated, second_names_for_evidence, id_associated)

        elif feature_associated == 'Transcriptional_Regulation':
            select2 = """
                SELECT DISTINCT `SystematicName`, `gene_link`, `StandardName` FROM %s_evidence WHERE `SystematicName` IN %s AND `Transcriptional_Regulation` IN ("%s");
            """%(feature_associated, second_names_for_evidence, id_associated)
        else:
            select2 = """
                SELECT DISTINCT `SystematicName`, `gene_link`, `StandardName` FROM %s_evidence WHERE `SystematicName` IN %s AND `%s` IN ("%s");
            """%(feature_associated, second_names_for_evidence, feature_associated, id_associated)

        evidence_table_associated = pd.read_sql('%s' %select2, connect)

        if query_feature[0]=='Protein_Domain':
            select = """
                SELECT Protein_Domain_name FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
            """%(query_feature[0], query_feature[0], query_feature[1])
            first_pd_id = db_cursor.execute(select).fetchone()
            first_pd_id = first_pd_id[0]
        if associate_feature[0]=='Protein_Domain':
            select = """
                SELECT Protein_Domain_name FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
            """%(associate_feature[0], associate_feature[0], associate_feature[1])
            second_pd_id = db_cursor.execute(select).fetchone()
            second_pd_id = second_pd_id[0]

    finally:
        connect.close()
    # print(first_table)




    first_name_table = pd.DataFrame(list(zip(first_names,['true']*len(first_names))),columns=['all','%s'%query_feature[2]])
    second_name_table = pd.DataFrame(list(zip(second_names,['true']*len(second_names))),columns=['all','%s'%associate_feature[2]])
    both_contain = pd.merge(first_name_table, second_name_table, how="inner")

    union = pd.merge(first_name_table, second_name_table, how="outer")
    union = union.fillna('false')

    second_contain = union[union["%s"%query_feature[2]] == 'false']
    queried_contain = union[union["%s"%associate_feature[2]] == 'false']

    if query_feature[0]=='Protein_Domain':
        both_contain = both_contain.rename(columns={'%s'%query_feature[1]:'%s'%first_pd_id})
        second_contain = second_contain.rename(columns={'%s'%query_feature[1]:'%s'%first_pd_id})
        queried_contain = queried_contain.rename(columns={'%s'%query_feature[1]:'%s'%first_pd_id})

    if associate_feature[0]=='Protein_Domain':
        both_contain = both_contain.rename(columns={"%s"%associate_feature[1]:"%s"%second_pd_id})
        second_contain = second_contain.rename(columns={"%s"%associate_feature[1]:"%s"%second_pd_id})
        queried_contain = queried_contain.rename(columns={"%s"%associate_feature[1]:"%s"%second_pd_id})


    both_contain = both_contain.fillna('false')

    if feature_query == "Physical_Interaction"or feature_query == "Genetic_Interaction":

        both_contain = pd.merge(evidence_table_query, both_contain, left_on="SystematicName(Bait)", right_on="all", how="inner")
        both_contain['SystematicName(Bait)'] = both_contain['Bait_link']
        both_contain['Evidence'] = both_contain['all']
        both_contain = both_contain.drop(columns=['Bait_link', 'all'])


        queried_contain = pd.merge(evidence_table_query, queried_contain, left_on="SystematicName(Bait)", right_on="all", how="inner")
        queried_contain['SystematicName(Bait)'] = queried_contain['Bait_link']
        queried_contain['Evidence'] = queried_contain['all']
        queried_contain = queried_contain.drop(columns=['Bait_link', 'all'])


    else:

        both_contain = pd.merge(evidence_table_query, both_contain, left_on="SystematicName", right_on="all", how="inner")
        both_contain['SystematicName'] = both_contain['gene_link']
        both_contain['Evidence'] = both_contain['all']
        both_contain = both_contain.drop(columns=['gene_link', 'all'])

        queried_contain = pd.merge(evidence_table_query, queried_contain, left_on="SystematicName", right_on="all", how="inner")
        queried_contain['SystematicName'] = queried_contain['gene_link']
        queried_contain['Evidence'] = queried_contain['all']
        queried_contain = queried_contain.drop(columns=['gene_link', 'all'])

    if feature_associated == "Physical_Interaction" or feature_associated =="Genetic_Interaction":

        second_contain = pd.merge(evidence_table_associated, second_contain, left_on="SystematicName(Bait)", right_on="all", how="inner")
        second_contain['SystematicName(Bait)'] = second_contain['Bait_link']
        second_contain['Evidence'] = second_contain['all']
        second_contain = second_contain.drop(columns=['Bait_link', 'all'])

    else:
        # print(evidence_table_associated)
        second_contain = pd.merge(evidence_table_associated, second_contain, left_on="SystematicName", right_on="all", how="inner")
        second_contain['SystematicName'] = second_contain['gene_link']
        second_contain['Evidence'] = second_contain['all']
        second_contain = second_contain.drop(columns=['gene_link', 'all'])

    # print(both_contain)
    both_contain = both_contain.rename(columns=feature_name_dict)
    both_contain = both_contain.fillna('-')
    both_contain = both_contain.to_html(index=None, classes='table table-bordered table-hover dataTable no-footer', escape=False)
    both_contain = both_contain.replace('table', 'table id="both_name_table"')
    # print(second_contain)

    second_contain = second_contain.rename(columns=feature_name_dict)
    second_contain = second_contain.fillna('-')
    second_contain = second_contain.to_html(index=None, classes='table table-bordered table-hover dataTable no-footer', escape=False)
    second_contain = second_contain.replace('table', 'table id="second_table"')
    # print("queried_contain",queried_contain)

    queried_contain = queried_contain.rename(columns=feature_name_dict)
    queried_contain = queried_contain.fillna('-')
    queried_contain = queried_contain.to_html(index=None, classes='table table-bordered table-hover dataTable no-footer ', escape=False)
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
    # print(feature)
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
                SELECT * FROM %s_evidence WHERE SystematicName IN ("%s") AND `Transcriptional_Regulation` IN ("%s");
            """%(feature1, systematice_name, id_query)
        else:
            select1 = """
                SELECT * FROM %s_evidence WHERE SystematicName IN ("%s") AND %s IN ("%s");
            """%(feature1, systematice_name, feature1, id_query)
        # print(select1)
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

        elif feature2 == 'Transcriptional_Regulation':
            select2 = """
                SELECT * FROM %s_evidence WHERE SystematicName IN ("%s") AND `Transcriptional_Regulation` IN ("%s");
            """%(feature2, systematice_name, id_associated)
            # print(select2)
        else:
            select2 = """
                SELECT * FROM %s_evidence WHERE SystematicName IN ("%s") AND %s IN ("%s");
            """%(feature2, systematice_name, feature2, id_associated)

    # print(select1)
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
                feature1_table["Protein_Domain"] = feature1_table.apply(lambda x :Protein_Domain_href(x['Protein_Domain'], x['DomainDescription']), axis=1)

                feature1_table = feature1_table.drop(columns=['DomainDescription'])

            elif feature1 =="GO_MF" or feature1 =="GO_BP" or feature1 =="GO_CC":
                feature1_table["EvidenceCode"] = feature1_table.apply(lambda x: x["EvidenceCode"].replace('<a ', '<a target="_blank"'), axis=1)
                feature1_table['SystematicName']=feature1_table['gene_link']
                feature1_table['%s'%feature1]=feature1_table['term_link']

                feature1_table = feature1_table.drop(columns=['gene_link', 'term_link'])


            else:
                feature1_table['SystematicName']=feature1_table['gene_link']
                feature1_table['%s'%feature1]=feature1_table['term_link']
                feature1_table = feature1_table.drop(columns=['gene_link', 'term_link'])


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
                feature2_table["Protein_Domain"] = feature2_table.apply(lambda x :Protein_Domain_href(x['Protein_Domain'], x['DomainDescription']), axis=1)

                feature2_table = feature2_table.drop(columns=['DomainDescription'])


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
