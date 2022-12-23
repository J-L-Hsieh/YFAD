from django.shortcuts import render
from django.http import JsonResponse
import sqlite3
import pandas as pd

def search_base(request):
    return(render(request, 'search.html',locals()))

def search_mode(request):
    feature = request.POST.get('input_feature')
    name = request.POST.get('input_name')

    conn = sqlite3.connect('db.sqlite3')
    try:
        sql = """
            SELECT * FROM %s_1_to_10 WHERE `%s(Queried)` LIKE '%s';
        """%(feature, feature, '%{}%'.format(name))
        table = pd.read_sql(sql, conn)
    finally:
        conn.close()
    table = table.fillna('-').drop(['count','SystematicName'],axis=1)
    table = table.to_html(index= None,classes="table table-striped table-bordered")
    table = table.replace('table', 'table id="result_table"',1)
    response = {'table':table, 'feature':feature}
    return JsonResponse(response)