# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:34:39 2019

@author: SwayamdiptaBiswas
"""
import pandas as pd
class CricketPreprocess:
    
    list_all_lines, list_over_deliveries, list_action, list_in_btwn_overs, list_action_otherwise = list(), list(), list(), list(), list()
    list_other_combined=list()
    bowler = list()
    batsman = list()
    
    # For opening File
    def openFile(self,filename):
        file = open(filename)
        for line in reversed(file.readlines()):
            self.list_all_lines.append(line.rstrip().lower())
        return self.list_all_lines
    
    # For Data Preprocessing
    def dataPreprocess(self,filename):
        self.list_all_lines=self.openFile(filename)
        string1, string2 = "", ""
        for i in self.list_all_lines:

            if i is not '' and i is not ' ' and ord(i[0]) in list(range(48, 58, 1)) and len(i) <= 4:

                if ('.' in i) and type(float(i)).__name__ == 'float':
                    string1 = string1.replace(string2, "")
                    self.list_action.append(string1)
                    self.list_action_otherwise.append(string2)
                    self.list_over_deliveries.append(i)
                    string1 = ""
                    string2 = ""
                else:
                    if string1 is not ' ':
                        self.list_in_btwn_overs.append(string1)
                        string1 = ""
                        string2 = ""
            else:
                string2 = string1
                string1 = string1 + "" + i

            self.list_other_combined = list(set(self.list_action_otherwise + self.list_in_btwn_overs))
            l = list()
            for i in self.list_other_combined:
                if (i != ''):
                    l.append(i)
            self.list_other_combined = l
            del l
            lsplit = list()
            
            run = list()
            
            wide = list()
            no_ball = list()
            lb = list()
            out = list()
            lout = list()  # b-bowled,c-caught

            dictionary1 = {'1 run': 1, 'bowled': 'b', 'caught': 'c', 'no run': 0, 'six': 6, 'four': 4, '5 runs': 5, 'wide': 1,
                           '2 runs': 2, 'leg byes': 1, '4': 4, '6': 6}

            for i in self.list_action:
                    lsplit = i.split(',')

            self.batsman.append(lsplit[0].split('to')[1])
            self.bowler.append(lsplit[0].split('to')[0])
            if ('wide' in lsplit[1]):
                wide.append(1)
                lout.append('none')
                run.append(1)
                lb.append(0)
                out.append('not out')
                no_ball.append(0)

            elif ('leg byes' in lsplit[1]):
                lb.append(1)
                run.append(dictionary1[lsplit[2].strip()])
                out.append('not out')
                lout.append('none')
                wide.append(0)
                no_ball.append(0)

            elif 'out' in lsplit[1]:

                v = lsplit[1].split('!')[0].split(' ')

                if 'bowled' == v[2]:
                    out.append(dictionary1[v[2]])
                    run.append(0)
                    wide.append(0)
                    lb.append(0)
                    no_ball.append(0)
                    lout.append(lsplit[0].split('to')[0])
            elif 'caught' == v[2]:
                out.append(dictionary1[v[2]])
                run.append(0)
                wide.append(0)
                lb.append(0)

                bowlern = lsplit[0].split(' ')[0:2]
                name = bowlern[0]
                if len(name) is 1:
                    name = name + " " + bowlern[1]

                lout.append("c " + v[4] + " b " + name)
                no_ball.append(0)

        # NO LBWs FOUND!!

            elif 'no ball' in lsplit[1]:
                no_ball.append(1)
                out.append('not out')
                run.append(0)
                wide.append(0)
                lb.append(0)
                out.append('none')

            else:
                wide.append(0)
                lb.append(0)
                out.append('not out')
                lout.append('none')
                run.append(dictionary1[lsplit[1].strip()])
                no_ball.append(0)
            # Preparing the Grand Dataset
            df_columns = ['over','batsman', 'bowler', 'run', 'wide', 'lb', 'nb', 'out', 'out_by']
            df = pd.DataFrame({'1':self.list_over_deliveries,'2': self.batsman, '3': self.bowler, '4': run, '5': wide,'6': lb, '7': no_ball, '8': out, '9': lout})
            df.columns=df_columns
            del lsplit,run,wide ,no_ball ,lb ,out,lout 
            return df
        
    # Generate first structured Data
    def generateStructuredResults(self,filename):
        df=self.dataPreprocess(filename)
        df.to_csv('cricketresults.csv',index=False) 
        
    
    # Return data frame of Bowling score 
    def bowlingScoreGenerator(self,filename):
        bowl,overs,maiden,runs,wickets,NB,wides,eco=list(),list(),list(),list(),list(),list(),list(),list()
        df=self.dataPreprocess(filename)
        df2=pd.DataFrame()

        bowl_er=list(set(self.bowler))
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
            del bowl,overs,maiden,runs,wickets,NB,wides,eco,counter,m,h,r,k
            return DataBowlers
    
    # Generate Score Card Bowling 
    def generateBowlerScoreCard(self,filename):
        DataBowlers=self.bowlingScoreGenerator(filename)
        DataBowlers.to_csv('Bowler_Data.csv',index=False)
        
        
    # Get the first preprocessed Data    
    def getStructuredDataPreprocessed(self,filename):
        return pd.read_csv('cricketresults.csv')
    
    
    #Get The Bowling Score Card
    def getBowlerScoreCard(self,filename):
        return pd.read_csv('Bowler_Data.csv')
    
    
    # Get Bowling Facts
    def highestWicketTaker_bestEconomy(self,filename):
        DataBowlers=self.getBowlerScoreCard(filename)
        d=DataBowlers.loc[DataBowlers['wickets']==max(DataBowlers['wickets'])]
        d=d.loc[d['eco']==min(d['eco'])]
        return d
    
    
    
    #  Get Bowling facts
    def bestEconomy_maxMaiden(self,filename):
        DataBowlers=self.getBowlerScoreCard(filename)
        d2=DataBowlers.loc[DataBowlers['eco']==min(DataBowlers['eco'])]
        d2=d2.loc[d2['maiden']==max(d2['maiden'])]
        return d2
    
    

        
        
        