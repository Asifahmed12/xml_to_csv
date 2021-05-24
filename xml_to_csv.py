import os

import pandas as pd

from fnmatch import fnmatch

import xmltodict, json

import datetime



os.chdir('F:/Asif_Ahmed/Projects/IDM_reponses/xml/')





# For renaming columns with same name



def df_column_uniquify(df):

    df_columns = df.columns

    new_columns = []

    for item in df_columns:

        counter = 0

        newitem = item

        while newitem in new_columns:

            counter += 1

            newitem = "{}_{}".format(item, counter)

        new_columns.append(newitem)

    df.columns = new_columns

    return df





# To read xml files in the directory



path = r'F:/Asif_Ahmed/Projects/IDM_reponses/xml/'



files = os.listdir(path)



#s = pd.Series(files)

#selected_files = [s for s in files if "idm" in s]



pattern = "*.xml"

dfs=[]

df = pd.DataFrame()







start_time = datetime.datetime.today()



# Main Code

for f in files:

    if fnmatch(f, pattern):

        with open(f,encoding="utf8") as datafile:

             doc = xmltodict.parse(datafile.read())

        raw = json.dumps(doc)

        data = json.loads(raw)

        df1 = data['response']

        if df1!= "The operation has timed out":

            if 'ednaScoreCard' in df1.keys():

             b = df1['ednaScoreCard']['etr']

             c = pd.DataFrame.from_dict(b,orient='columns')

             d = c[['test','fired']]

             d = d.set_index('test').T

             d.columns = d.columns.str.replace(":", "_")

             d.columns = map(str.upper, d.columns)

             d1 = d.add_prefix('EDNASCORECARD_ETR_FIRED_')

        

             e = c[['test','details']]

             e = e.set_index('test').T

             e.columns = e.columns.str.replace(":", "_")

             e.columns = map(str.upper, e.columns)

             d2 = e.add_prefix('EDNASCORECARD_ETR_DETAILS_')

        

             df_c = pd.concat([d1.reset_index(drop=True), d2.reset_index(drop=True)], axis=1)

             dfa = df_column_uniquify(df_c)

             dfs.append(dfa)

             del dfa

             

         #else: Print("pass")

             

# Final csv

merged = pd.concat(dfs)

merged.to_csv("result.csv")



end_time = datetime.datetime.today()



print("start_time = ", start_time)

print("Execution end Time: ", end_time)  # can be further used for debugging

print("Total execution time : ", end_time - start_time)

    
