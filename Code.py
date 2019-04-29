file = open('C:\\Users\\Swayamdipta Biswas\\Downloads\\Data.txt')
list_all_lines, list_over_deliveries, list_action, list_in_btwn_overs, list_action_otherwise = list(), list(), list(), list(), list()
for line in reversed(file.readlines()):
    list_all_lines.append(line.rstrip())
string1, string2 = "", ""
for i in list_all_lines:

    if i is not '' and i is not ' ' and ord(i[0]) in list(range(48, 58, 1)) and len(i) <= 4:

        if ('.' in i) and type(float(i)).__name__ == 'float':
            string1 = string1.replace(string2, "")
            list_action.append(string1)
            list_action_otherwise.append(string2)
            list_over_deliveries.append(i)
            string1 = ""
            string2 = ""
        else:
            if string1 is not ' ':
                list_in_btwn_overs.append(string1)
            string1 = ""
            string2 = ""
    else:
        string2 = string1
        string1 = string1 + "" + i

list_other_combined = list(set(list_action_otherwise + list_in_btwn_overs))
l=list()
for i in list_other_combined:
    if(i!=''):
        l.append(i)
list_other_combined=l
del l
lsplit=list()
bowler=list()
batsman=list()
run=list()
speed=list()
wide=list()
no_ball=list()
maiden=list()

dictionary1={'1 run':1,'no run':0,'SIX':6,'FOUR':4,'four':4,'six':6,}

for i in list_action:
   lsplit=i.split(',')




