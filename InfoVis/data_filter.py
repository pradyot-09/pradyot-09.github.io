# DATA PREPROCESSING / PREPARATION
# for
# InfoVis

# This is Group  Number #14
# We are Daniele, Pradyot and Purvesh

import pandas as pd
from sklearn.externals import joblib


try:
    data = joblib.load('vis1.pkl')
except:
    #read the database
    data = pd.read_csv('terrorismdb.csv', encoding='UTF-8')
    #rename the weird column names
    data.rename(
        columns={'iyear': 'Year', 'imonth': 'Month', 'iday': 'Day', 'country_txt': 'Country', 'region_txt': 'Region',
                 'attacktype1_txt': 'AttackType', 'target1': 'Target', 'nkill': 'Killed', 'nwound': 'Wounded',
                 'summary': 'Summary', 'gname': 'Group', 'targtype1_txt': 'Target_type', 'weaptype1_txt': 'Weapon_type',
                 'motive': 'Motive'}, inplace=True)
    data = data[['Year', 'Month', 'Day', 'Country', 'Region', 'city', 'latitude', 'longitude', 'AttackType', 'Killed',
                 'Wounded', 'Target', 'Summary', 'Group', 'Target_type', 'Weapon_type', 'Motive']]
    data['Killed'].fillna(0, inplace=True)
    data['Wounded'].fillna(0, inplace=True)
    # Creating a common column for casualities
    data['casualities'] = data['Killed'] + data['Wounded']
    joblib.dump(data,'vis1.pkl')
# print(data)



# 
# Vis 1 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#Get number of attacks per year for bar chart
firstBarChart = data[['Year','Country']].groupby(['Year']).agg(['count'])
print(firstBarChart)
# [["1970",651],["1971",471],["1972",568],["1973",473],["1974",581],["1975",740],["1976",923],["1977",1319],["1978",1526],["1979",2662],["1980",2661],["1981",2586],["1982",2544],["1983",2870],["1984",3495],["1985",2915],["1986",2860],["1987",3183],["1988",3720],["1989",4324],["1990",3887],["1991",4683],["1992",5071],["1994",3456],["1995",3081],["1996",3058],["1997",3199],["1998",934],["1999",1395],["2000",1824],["2001",1913],["2002",1333],["2003",1278],["2004",1166],["2005",2017],["2006",2758],["2007",3242],["2008",4805],["2009",4722],["2010",4826],["2011",5076],["2012",8529],["2013",12041],["2014",16908],["2015",14977],["2016",13626],["2017",10980],["2018",9607]]
# create a 2d array from this for plotting the incidents graph

# Vis 1 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Vis 2 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
weapon_sums = {}
for weapon in data['Weapon_type']:
    if weapon in weapon_sums:
        weapon_sums[weapon] = weapon_sums[weapon]+1
    else:
        weapon_sums[weapon] = 1
print(weapon_sums)
# Use weapon_sums for the weapons bubble chart

# Vis 2 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Vis 3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#Bubble graph for casualties in every continent(Region)
label={}
x=1
temp2=data['Region'].unique()
for l in temp2:
    label[l]=x
    x=x+1
print(temp2)

temp=data[['Country','Region','Year','Killed','Wounded']]
temp['Total']=temp['Killed']+temp['Wounded']
temp=temp.groupby(['Region','Country'], as_index=False).agg({'Year':'count', 'Total': 'sum'}).rename(columns={'Year':'Count'})
cmp=[]
for l in temp['Region']:
    cmp.append(label[l])
temp['class']=cmp

#get the Top 50 Regions with highest number of attacks
temp = temp.sort_values(by='Count', ascending=False)
temp=temp.head(50)
print(temp)
#write to a csv
#temp.to_csv('vis3.csv', sep=',', encoding='utf-8')
# Vis 3 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# CHART 4 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Sequence Sunburst for cities with 200+ attacks
temp=data[['Country','Region','city','Year']]

# for count of attacks in every continent
#temp2=temp.groupby('Region', as_index=False).agg({'Year':'count'})


temp=temp.groupby(['Region','Country','city'], as_index=False).agg({'Year':'count'}).rename(columns={'Year':'Count'})
temp=temp.sort_values(['Region','Count'],ascending=False).groupby('Region').head(100)

#get cities with 200+ attacks
temp=temp[temp['Count'] > 200]

#temp3=temp.groupby('Region', as_index=False).agg({'Count':'sum'})


sd = {'Area':['world-Australasia & Oceania', 'world-Central Asia', 'world-East Asia','world-Central America & Caribbean-others','world-Eastern Europe-others','world-Middle East & North Africa-others','world-North America-others','world-South America-others','world-South Asia-others','world-Southeast Asia-others','world-Sub Saharan Africa-others','world-Western Europe-others'], 'Count':[304, 571, 808,7149,4996,26941,3112,11314,37879,11948,16810,9455]} 
#create a dataframe for csv
vis4=pd.DataFrame(sd)
#start from 3 for neglection 'other'  parts and select only cities with 200+ attacks
i=3
#prepare data for csv
for index,x in temp.iterrows():
    world='world'+'-'+x['Region'].replace('-', ' ')+'-'+x['Country']+'-'+x['city'].replace('-', ' ')
    vis4.loc[i]=[world,x['Count']]
    i=i+1


#vis4.to_csv('out.csv', sep=',', encoding='utf-8')
#print(vis4)
# CHART 4 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>








# CHART 5 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

try:
    xoxo = joblib.load('vis5.pkl')
    f = open('vis5/location_data.js', 'w')
    f.write("var bubble_data_global = " + str(xoxo['solo_data']) + ";")
    f.close()

except:
    # dropping rows that don't have latitude longitude data
    latlongdata = data[data["latitude"]==data["latitude"]]
    latlongdata = data[data["longitude"]==data["longitude"]]
    latlongdata['city'].fillna('unknown', inplace=True) 
    # getting the top 15 terrorist groups based on number of incidents
    x = latlongdata.groupby('Group')['Region'].nunique()
    print(x.head(50))
    top10groups = x.sort_values(axis=0,ascending=False).head(15)
    print(top10groups)
    groupdata= {}
    bubble_data = []
    solo_data = {}

    for index,row in latlongdata[['latitude','longitude','AttackType','Group','Year','casualities','city']].iterrows():
        if row['Group'] in top10groups.keys():
            temp = {}
            temp['latitude'] = row['latitude']
            temp['longitude'] = row['longitude']
            temp['type'] = row['AttackType']
            #set the bubble size
            calc = (float(row['casualities'])/float(500))*12
            temp['radius'] = 8 + calc
            #classify attacks 
            if 'Armed' in row['AttackType']:
                temp['fillKey'] = 'ONE'
            elif 'Bombing' in row['AttackType']:
                temp['fillKey'] = 'TWO'
            elif 'Unarmed' in row['AttackType']:
                temp['fillKey'] = 'SIX'
            elif 'Unknown' in row['AttackType']:
                temp['fillKey'] = 'FIVE'
            elif 'Hostage' in row['AttackType']:
                temp['fillKey'] = 'FOUR'
            else:
                temp['fillKey'] = 'THREE'

            temp['y'] = row['Year']
            temp['city']=row['city']
            bubble_data.append(temp)
            if row['Group'] in solo_data:
                solo_data[row['Group']].append(temp)
            else:
                solo_data[row['Group']] = []
                solo_data[row['Group']].append(temp)
            if row['Group'] in groupdata:
                if row['AttackType'] in groupdata[row['Group']]:
                    groupdata[row['Group']][row['AttackType']] = groupdata[row['Group']][row['AttackType']]+1
                else:
                    groupdata[row['Group']][row['AttackType']] = 1
            else:
                groupdata[row['Group']] = {}
                groupdata[row['Group']][row['AttackType']] = 1
    print(top10groups.keys())
    #print(solo_data)

    vis5 = {'solo_data':solo_data,'groups':top10groups.keys()}
    joblib.dump(vis5,'vis5.pkl');
# CHART 5 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

