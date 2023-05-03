from django.shortcuts import render
from django.http import JsonResponse
import sqlite3
import pandas as pd

def search_base(request):
    return(render(request, 'search.html',locals()))

def search_mode(request):
    feature = request.POST.get('input_feature')
    name = request.POST.get('input_name')
    conn = sqlite3.connect('/home/chunlin/Django/chunlin_project/db.sqlite3')

    #Protein Domain 表中 name與輸入的字並多取出這個欄位來顯示
    if feature == 'Protein_Domain':
        select = """
            SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, Protein_Domain_name FROM %s_10_length WHERE %s_name LIKE '%s';
        """%(feature, feature, feature, '%{}%'.format(name))

    else:
        select = """
            SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction FROM %s_10_length WHERE `%s(Queried)` LIKE '%s';
        """%(feature, feature, feature, '%{}%'.format(name))

    try:
        table = pd.read_sql(select, conn)
    finally:
        conn.close()

    if feature == 'Protein_Domain':
        table['Detail'] = table['Protein_Domain(Queried)']
        table['Protein_Domain(Queried)'] = table['Protein_Domain_name']
        table = table.drop(columns=['Protein_Domain_name'])
    else:
        table['Detail'] = table['%s(Queried)'%feature]

    '''------tooltips------'''
    # count_name_table =  table[['count','SystematicName']]
    # count_name_table = count_name_table.values.tolist()
    '''------tooltips------'''

    table = table.fillna('-')
    table = table.to_html(index= None,classes="table table-striped table-bordered")
    table = table.replace('table', 'table id="result_table"',1)
    # response = {'table':table, 'feature':feature, 'count_name_table':count_name_table}
    response = {'table':table, 'feature':feature}

    return JsonResponse(response)