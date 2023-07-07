from django.shortcuts import render
from django.http import JsonResponse
import sqlite3
import pandas as pd

def search_base(request):
    return(render(request, 'search.html',locals()))

def search_mode(request):
    fature_name_dict = {"GO_MF(Queried)":"Queried Term", "GO_BP(Queried)":"Queried Term", "GO_CC(Queried)":"Queried Term", "Protein_Domain(Queried)":"Queried Term", "Mutant_Phenotype(Queried)":"Queried Term", "Pathway(Queried)":"Queried Term", "Disease(Queried)":"Queried Term", "Transcriptional_Regulation(Queried)":"Queried Term", "Physical_Interaction(Queried)":"Queried Term", "Genetic_Interaction(Queried)":"Queried Term",
                        "GO_MF":"GO_MF", "GO_BP":"GO_BP", "GO_CC":"GO_CC", "Disease":"Disease", "Pathway":"Pathway", "Protein_Domain":"Protein Domain", "Mutant_Phenotype":"Mutant Phenotype", "Transcriptional_Regulation":"Transcriptional Regulation", "Physical_Interaction":"Physical Interaction", "Genetic_Interaction":"Genetic Interaction"}
    # feature = request.POST.get('input_feature')  #GO_MF
    name = request.POST.get('search_name')  #Y-form DNA binding
    # print(name)
    conn = sqlite3.connect('db.sqlite3')
    feature_list=["GO_MF", "GO_BP", "GO_CC", "Protein_Domain", "Mutant_Phenotype", "Pathway", "Disease", "Transcriptional_Regulation", "Physical_Interaction", "Genetic_Interaction"]
    find_feature = []
    all_table = []
    response = {}
    try:
        for feature in feature_list:

            #Protein Domain 表中 name與輸入的字並多取出這個欄位來顯示
            if feature == 'Protein_Domain':
                select = """
                    SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, Protein_Domain_name FROM %s_10_length WHERE %s_name LIKE '%s';
                """%(feature, feature, feature, '%{}%'.format(name))
            elif feature == 'Transcriptional_Regulation':
                select = """
                    SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction, Transcriptional_Regulation_id FROM %s_10_length WHERE `%s(Queried)` LIKE '%s';
                """%(feature, feature, feature, '%{}%'.format(name))
            else:
                select = """
                    SELECT `%s(Queried)`, GO_MF, GO_BP, GO_CC, Protein_Domain, Mutant_Phenotype, Pathway, Disease, Transcriptional_Regulation, Physical_Interaction, Genetic_Interaction FROM %s_10_length WHERE `%s(Queried)` LIKE '%s';
                """%(feature, feature, feature, '%{}%'.format(name))


            locals()[feature+"_table"] = pd.read_sql(select, conn)


            if locals()[feature+"_table"].empty == False:
                print(feature)
                if feature == 'Protein_Domain':
                    locals()[feature+"_table"]['Detail'] = locals()[feature+"_table"]['Protein_Domain(Queried)']
                    locals()[feature+"_table"]["Protein_Domain(Queried)"] = locals()[feature+"_table"].apply(lambda x: x["Protein_Domain_name"]+'%'+x["Protein_Domain(Queried)"], axis=1)
                    locals()[feature+"_table"] = locals()[feature+"_table"].drop(columns=['Protein_Domain_name'])
                    print(locals()[feature+"_table"])

                elif feature == 'Transcriptional_Regulation':
                    locals()[feature+"_table"]["Transcriptional_Regulation(Queried)"] = locals()[feature+"_table"].apply(lambda x: x["Transcriptional_Regulation(Queried)"]+'%'+x["Transcriptional_Regulation_id"], axis=1)
                    locals()[feature+"_table"] = locals()[feature+"_table"].drop(columns=['Transcriptional_Regulation_id'])
                    print(locals()[feature+"_table"])

                else:
                    locals()[feature+"_table"]['Detail'] = locals()[feature+"_table"]['%s(Queried)'%feature]
                    locals()[feature+"_table"]['%s(Queried)'%feature] = locals()[feature+"_table"].apply(lambda x: x['%s(Queried)'%feature]+'%'+x['%s(Queried)'%feature], axis=1)


                find_feature.append(feature)
                locals()[feature+"_table"]["Detail"] = locals()[feature+"_table"].iloc[:,1:-1].sum(axis=1)
                print(locals()[feature+"_table"])

                locals()[feature+"_table"] = locals()[feature+"_table"].rename(columns=fature_name_dict)
                locals()[feature+"_table"] = locals()[feature+"_table"].to_html(index= None,classes="table table-striped table-bordered")
                locals()[feature+"_table"] = locals()[feature+"_table"].replace('table', 'table id="%s_table"'%feature, 1)
                all_table.append(locals()[feature+"_table"])

    finally:
        conn.close()
    response["find_feature"] = find_feature
    response["all_table"] = all_table
    print(find_feature)
    # table = table.fillna('-')
    # table = table.to_html(index= None,classes="table table-striped table-bordered")
    # table = table.replace('table', 'table id="result_table"',1)
    # response = {'table':table, 'feature':feature, 'count_name_table':count_name_table}
    # response = {'table':table, 'feature':feature}
    # print(response)
    return JsonResponse(response)