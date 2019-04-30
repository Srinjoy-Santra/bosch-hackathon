# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 18:03:48 2019

@author: SwayamdiptaBiswas
"""
from codexyzClasses import CricketPreprocess

import matplotlib.pyplot as plt
import pandas as pd
class BowlingAnalysis:
    global file
    bowler = list()
    batsman = list()
    def __init__(self,filename):
        self.file=CricketPreprocess().dataPreprocess(filename)
        #self.file=pd.read_csv('dataset.txt')
    
    def bowlingScoreGenerator(self):
        bowl,overs,maiden,runs,wickets,NB,wides,eco=list(),list(),list(),list(),list(),list(),list(),list()
        df=self.file
        df2=pd.DataFrame()

        bowl_er=list(set(self.bowler))
        
       
        i,lis=0,list()
        lis.appendt(df.loc[df['over']==float(i+0.1)]['bowler'])
        
        while(i <= int(df[-1,0])):
            i=i+1
            if(df.loc[df['over']==float(i+0.1)]['bowler'] not in lis):
                lis.append(df.loc[df['over']==float(i+0.1)]['bowler'])
        for i in bowl_er:
            counter=0
            m=0
            df2=df.loc[df['bowler'] == i]
            bowl.append(i)
            overs.append(len(df2['bowler'])//6)
            wides.append(sum(df2['wide']))
            NB.append(sum(df2['nb']))
            wickets.append(len(df2.loc[df2['out']!='not out']['out']))
            runs.append(sum(df2['run']))
            eco.append((sum(df2['run']))/(len(df2['bowler'])//6))
            h=int(df['over'].reshape(-1)[0].split('.')[0])
            r=0
            for j in df2['over']:
                k=float(j)
                if int(k)!=0 and (k<=float(int(k)+0.6)) and (h%int(k)==0):
                    r=r+df2['run'].reshape(-1)[m]
                    m=m+1
                    h=int(j.split('.')[0])
                elif int(k)==0:
                    if (k<=float(int(k)+0.6)):
                        r=r+df2['run'].reshape(-1)[m]
                        m=m+1
                        h=int(j.split('.')[0])
                    else:
                        if r==0:
                            counter=counter+1
                else:
                    counter=0
                    r=0
                    r=r+df2['run'].reshape(-1)[m]
                    m=m+1
                    h=int(j.split('.')[0])
                maiden.append(counter)
            DataBowlers=pd.DataFrame({ '1':bowl,'2':overs,'3':maiden,'4':runs,'5':wickets,'6':NB,'7':wides,'8':eco}) 
            Bowler_columns=['bowler','overs','maiden','runs','wickets','NB','wide','eco']
            DataBowlers.columns=Bowler_columns
            DataBowlers.to_csv('Bowler_Data2.csv',index=False)
            del bowl,overs,maiden,runs,wickets,NB,wides,eco,counter,m,h,r,k
            return DataBowlers
    
           
                
    #Get The Bowling Score Card
    def getBowlerScoreCard(self):
        return pd.read_csv('Bowler_Data2.csv')
    
    
    # Get Bowling Facts
    def highestWicketTaker_bestEconomy(self):
        DataBowlers=self.getBowlerScoreCard()
        d=DataBowlers.loc[DataBowlers['wickets']==max(DataBowlers['wickets'])]
        d=d.loc[d['eco']==min(d['eco'])]
        return d
    
    
    
    #  Get Bowling facts
    def bestEconomy_maxMaiden(self):
        DataBowlers=self.getBowlerScoreCard()
        d2=DataBowlers.loc[DataBowlers['eco']==min(DataBowlers['eco'])]
        d2=d2.loc[d2['maiden']==max(d2['maiden'])]
        return d2    
    def plotNetRunrate(self):
        runrate=list()
        count,m,r=1,0,0
        for i in self.file['over']:
            k=float(i)
            if(k<float(int(k)+0.6)):
                r=r+self.file['run'].reshape(-1)[m]
                m=m+1
        
            elif k==float(int(k)+0.6):
                r=r+self.file['run'].reshape(-1)[m]
                m=m+1
                runrate.append(r/count)
                count=count+1
       
        o=list(range(1,21,1))
        plt.scatter(x=o,y=runrate,c='r')
        plt.plot(o,runrate,c='b')
        plt.show()
        
p=BowlingAnalysis('C:\\Users\\Swayamdipta Biswas\\Downloads\\Data.txt') 
p.plotNetRunrate()   
