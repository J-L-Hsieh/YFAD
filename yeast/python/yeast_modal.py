import pandas as pd
import sqlite3
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

def modal(request):
    feature_name = request.POST.get('feature_name').split('%')

    feature1 = feature_name[0]
    name1 = feature_name[1]

    feature2 = feature_name[2]
    name2 = feature_name[3]
    print(name1)
    print(name2)
    try:
        connect = sqlite3.connect('db.sqlite3')
        db_cursor = connect.cursor()

        select = """
            SELECT SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
        """%(feature1, feature1, name1)
        db_cursor.execute(select)
        sys_name1 = db_cursor.fetchall()
        sys_name1_set = set(eval(sys_name1[0][0]))


        select = """
            SELECT SystematicName FROM %s_1_to_10 WHERE `%s(Queried)` IN ("%s");
        """%(feature2, feature2, name2)
        db_cursor.execute(select)
        sys_name2 = db_cursor.fetchall()
        print(select)
        print(sys_name2)
        sys_name2_set = set(eval(sys_name2[0][0]))
        intersection = str(tuple(sys_name1_set.intersection(sys_name2_set)))
        '''-------------------------依照主要的feature取出證據檔------------------'''
        if feature2 == 'Physical_Interaction':
            select = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN %s  AND `StandardName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN %s AND `StandardName(Bait)` IN ("%s"));
            """%(feature2, intersection, name2, intersection, name2)
            print(select)
            evidence_table = pd.read_sql(select , connect)


        elif feature2 == 'Genetic_Interaction':
            select = """
                SELECT * FROM %s_evidence WHERE `SystematicName(Bait)` IN %s  AND `StandardName(Hit)` IN ("%s") OR (`SystematicName(Hit)` IN %s AND `StandardName(Bait)` IN ("%s"));
            """%(feature2, intersection, name2, intersection, name2)
            print(select)
            evidence_table = pd.read_sql(select , connect)

        else:
            select = """
                SELECT * FROM %s_evidence WHERE SystematicName IN %s AND %s IN ("%s");
            """%(feature2, intersection, feature2, name2)
            print(select)
            evidence_table = pd.read_sql(select , connect)
    finally:
        connect.close()
    if feature2 == 'Physical_Interaction':
        evidence_table['SystematicName(Bait)']=evidence_table['Bait_link']
        evidence_table['SystematicName(Hit)']=evidence_table['Hit_link']
        evidence_table['StandardName(Bait)']=evidence_table['term_link']
        evidence_table = evidence_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

    elif feature2 == 'Genetic_Interaction':
        evidence_table['SystematicName(Bait)']=evidence_table['Bait_link']
        evidence_table['SystematicName(Hit)']=evidence_table['Hit_link']
        evidence_table['StandardName(Bait)']=evidence_table['term_link']
        evidence_table = evidence_table.drop(columns=['Bait_link', 'Hit_link', 'term_link'])

    else:
        evidence_table['SystematicName']=evidence_table['gene_link']
        evidence_table['%s'%feature2]=evidence_table['term_link']
        evidence_table = evidence_table.drop(columns=['gene_link', 'term_link'])
    # print(evidence_table)
    evidence_table = evidence_table.to_html(index= None, classes="table table-bordered table-hover dataTable no-footer", escape=False)
    # evidence_table = evidence_table.to_html(index= None, classes = "table", escape=False)

    evidence_table = evidence_table.replace('table', 'table id="evidence_table"', 1)

    return evidence_table