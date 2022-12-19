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



def yeast(request):
    return(render(request,'yeast_browse.html',locals()))
def yeast_associated_base(request):
    return(render(request,'yeast_associated.html',locals()))
def yeast_name_base(request):
    return(render(request, 'yeast_name.html',locals()))

'''----------------------------------------------------------------------------'''

def yeast_browser(request):
    table_name = request.POST.get('first_feature')
    table_column = request.POST.get('other_feature')[:-1]

    sql = """
        SELECT `%s(Queried)`, %s FROM %s_1_to_10;
    """%(table_name, table_column, table_name)
    print(sql)
    try:
        connect = sqlite3.connect('db.sqlite3')
        table = pd.read_sql(sql, connect)
    finally:
        connect.close()

    table = table.fillna('-')
    detail_column = ['-']*len(table)
    table['Detail'] = detail_column
    table = table.to_html(index= None,classes="table table-striped table-bordered")
    table = table.replace('table','table id="result_table"',1)
    # table = table.to_json(orient="records")
    # print(table)
    response = {'table':table}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''

def yeast_associated(request):
    # print(request)
    # print('--------')

    table_name = request.POST.get('table_name')
    row_name = request.POST.get('row_name')
    try:
        connect = sqlite3.connect('db.sqlite3')
        select = """
            SELECT * FROM %s_1_to_10 WHERE `%s(Queried)` IN ('%s');
        """%(table_name, table_name, row_name)
        # print(select)
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
    print(first_feature)
    print(second_feature)
    try:
        connect = sqlite3.connect('db.sqlite3')
        for  i in range(2):
            if i == 1:
                select = """
                    SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ('%s')
                """%(first_feature[0], first_feature[0], first_feature[1])
                first_table = pd.read_sql('%s' %select, connect)
                # print(select)
            else:
                select = """
                    SELECT count,SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ('%s')
                """%(second_feature[0], second_feature[0], second_feature[1])
                second_table = pd.read_sql('%s' %select, connect)
    finally:
        connect.close()

    print(first_table)
    first_names = eval(first_table.iat[0,1])
    second_names = eval(second_table.iat[0,1])
    print(type(len(second_names)))
    first_name_table = pd.DataFrame(list(zip(first_names,['true']*len(first_names))),columns=['all','%s'%first_feature[1]])
    second_name_table = pd.DataFrame(list(zip(second_names,['true']*len(second_names))),columns=['all','%s'%second_feature[1]])
    df_merge = pd.merge(first_name_table,second_name_table,how="outer")
    df_merge = df_merge.fillna('false').to_html(index=None, classes='table table-striped table-bordered')
    df_merge = df_merge.replace('table', 'table id="both_name_table"')
    response = {'df_merge':df_merge}
    return JsonResponse(response)

'''----------------------------------------------------------------------------'''
def yeast_modal(request):
    evidence_table = modal(request)
    response ={'evidence_table':evidence_table}
    # print(evidence_table)
    return JsonResponse(response)