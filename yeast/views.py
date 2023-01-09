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

def yeast_browser(request):
    table_name = request.POST.get('first_feature')
    table_column = request.POST.get('other_feature')[:-1]
    first = time.time()
    sql = """
        SELECT `%s(Queried)`, %s FROM %s_1_to_10;
    """%(table_name, table_column, table_name)
    try:
        connect = sqlite3.connect('db.sqlite3')
        table = pd.read_sql(sql, connect)
    finally:
        connect.close()
    table = table.fillna('-')
    detail_column = ['-']*len(table)
    table['Detail'] = detail_column
    table_columns = table.columns.values.tolist()
    columns = []
    for i in table_columns:
        columns.append({'title': i})
    table = table.values.tolist()
    response = {'table':table, 'columns':columns}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''

def yeast_associated(request):

    table_name = request.POST.get('table_name')
    row_name = request.POST.get('row_name')
    try:
        connect = sqlite3.connect('db.sqlite3')
        select = """
            SELECT * FROM %s_1_to_10 WHERE `%s(Queried)` IN ('%s');
        """%(table_name, table_name, row_name)
        table = pd.read_sql('%s' %select, connect)
    finally:
        connect.close()
    '''---------------------刪除不必要的欄位------------------------'''
    associated_table = table.dropna(axis='columns')
    all_tables = associated_analysis(associated_table)
    network_data = network(associated_table)
    associated_table = associated_table.drop(['count','SystematicName'],axis=1)
    #拿出column name
    associated_table = associated_table.to_html(index= None,classes="table table-striped table-bordered")
    associated_table = associated_table.replace('table','table id="associated_table"',1)
    response={'associated_table':associated_table , 'all_tables':all_tables, 'network_data':network_data}
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
    both_contain = both_contain.to_html(index=None, classes='table table-striped table-bordered')
    both_contain = both_contain.replace('table', 'table id="both_name_table"')

    queried_contain = queried_contain.to_html(index=None, classes='table table-striped table-bordered')
    queried_contain = queried_contain.replace('table', 'table id="queried_table"')

    second_contain = second_contain.to_html(index=None, classes='table table-striped table-bordered')
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
            feature1_table = feature1_table.to_html(index= None, classes="table table-striped table-bordered",escape=False)
            feature1_table = feature1_table.replace('table', 'table id="feature1_table"', 1)

        if feature2 == 'false':
            feature2_table = 'no table'
        else:
            feature2_table = pd.read_sql(select2, connect)
            feature2_table = feature2_table.to_html(index= None, classes="table table-striped table-bordered",escape=False)
            feature2_table = feature2_table.replace('table', 'table id="feature2_table"', 1)
    finally:
        connect.close()

    response = {'feature1_table' : feature1_table, 'feature2_table' : feature2_table}
    return JsonResponse(response)
