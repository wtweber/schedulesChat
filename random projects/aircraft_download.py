import json, requests, io, os
import pandas as pd
#from pandas.io.json import json_normalize

parameters = {  'api_key' : '41665130-d5a7-11e9-9e95-755433902422',
                'format' : 'JSON',
                'manufacturer' : ''
}


manufactur = pd.read_json('data.json', orient='records')
manufactur = manufactur.sort_values(by=['types'], ascending = False).reset_index(drop=True)
path = os.getcwd()
#print(manufactur)


aircraft= pd.DataFrame()

for index, row in manufactur.iterrows():
    parameters['manufacturer'] = row['manufacturer_code']
    #print(parameters)
    response = requests.get("https://v4p4sz5ijk.execute-api.us-east-1.amazonaws.com/anbdata/aircraft/designators/type-list", params=parameters)
    data = response.json()
    #rawData = pd.read_json(io.StringIO(data))
    #print(json.dumps(data, indent=4))

    aircraft = aircraft.append(pd.json_normalize(data), sort = False)
    #if index > 90:
    #    break

# Make a get request with the parameters.
aircraft = aircraft.reset_index(drop=True)
print(aircraft)
writer = pd.ExcelWriter(os.path.join(path, 'aircraft.xlsx'), engine = 'xlsxwriter')
aircraft.to_excel(writer, index=False)
writer.save()
