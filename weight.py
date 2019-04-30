import pandas as pd
file=pd.read_csv('Bowler_Data.csv')
weight=list()
for i in list(file['bowler'].index):
    if file.iloc[i,4] != 0:
        if file.iloc[i,4]==4:
            d=4
        elif file.iloc[i,4]==5:
            d=8
        else:
            d=0
        weight.append((file.iloc[i,4]*10)+(file.iloc[i,2]*4)+d)
    else:
         weight.append(0+(file.iloc[i,2]*4))
file['weight']=weight 
file.to_csv('WeightedBowlingScoreBoard.csv')
bestBowler=file.loc[file['weight']==max(file['weight'])]['bowler'].reshape(-1)[0]
print(bestBowler)     