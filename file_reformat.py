
import pdb
import pandas as pd
import numpy as np

dirName = 'files'

def charIndex(string):
    underIndex = [i for i,ltr in enumerate(string) if ltr=='_']
    if len(underIndex)==7:
        spaceIndex = string.index('_')
    else:
        spaceIndex = string.index(' ')    
    
    equalIndex = [i for i,ltr in enumerate(string) if ltr=='=']
    return spaceIndex, equalIndex


fileNames = ['LVHS_LOD.xlsx','LVVSN_LOD.xlsx','LVVSP_LOD.xlsx']
totalDataFrame = pd.DataFrame()


for fileIndex in range(0,len(fileNames)):
    df = pd.read_excel(dirName+'/'+fileNames[fileIndex],header=0)
    #names = df.columns.values.tolist()
    rows_num = len(df.index)*(len(df.columns)-4)  
    #rows_num = len(df.index)*(50-4) 
    new_df = pd.DataFrame(index=np.arange(0,rows_num),columns=('component','L','W','type','SA','SB','SX','dieX','dieY','wafer','value'))

    count = 0   
    for col in range(4,len(df.columns)):
    #for col in range(4,50):
        print fileIndex,' ',col
        spaceIndex,equalIndex = charIndex(df.columns[col]) 
        for row in range(0,len(df.index)):
            new_df.loc[count]['value']=df.loc[row][col]
            new_df.loc[count]['wafer']=df.loc[row][1]  
            new_df.loc[count]['dieX']=df.loc[row][2]
            new_df.loc[count]['dieY']=df.loc[row][3]
            #pdb.set_trace()
            new_df.loc[count]['type']=str(df.columns[col][:spaceIndex]).lower()
            new_df.loc[count]['L']=df.columns[col][equalIndex[0]+1:equalIndex[1]-2]
            new_df.loc[count]['W']=df.columns[col][equalIndex[1]+1:equalIndex[2]-3]  
            new_df.loc[count]['SA']=df.columns[col][equalIndex[2]+1:equalIndex[3]-3]
            new_df.loc[count]['SB']=df.columns[col][equalIndex[3]+1:equalIndex[4]-3]
            new_df.loc[count]['SX']=df.columns[col][equalIndex[4]+1:]
            new_df.loc[count]['component']=str(df.columns[col][spaceIndex+1:equalIndex[0]-2]).lower()
            count+=1 
    
    totalDataFrame = pd.concat([totalDataFrame,new_df],ignore_index=True)    

writer = pd.ExcelWriter('output.xlsx')
totalDataFrame.to_excel(writer,'sheet1')
writer.save()
print "Excel is written!"

for key in new_df:
    pdb.set_trace()
    arr = np.array(new_df[key])
    np.save(open(dirName+'/'+key+'.npy','w'),arr)

print 'npy is written'



