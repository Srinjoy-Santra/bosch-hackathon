file=open('Data.txt')
list_all_lines,list_over_deliveries,list_action,list_in_btwn_overs,list_action_otherwise=list(),list(),list(),list(),list()
for line in reversed(file.readlines()):
    list_all_lines.append(line.rstrip())
string1=" "
for i in list_all_lines:
    #print(list1[i])
    #print(string1)
    if i is not '' and i is not ' ' and ord(i[0]) in list(range(48,58,1)) and len(i)<=4:

        if ('.' in i) and type(float(i)).__name__=='float':
            list_action.append(string1)
            list_over_deliveries.append(i)
            string1=" "
        else:
            if string1 is not ' ':
                list_in_btwn_overs.append(string1)
            string1=" "
    else:
        if string1 is not ' ':
            list_action_otherwise.append(string1)
        string1 = string1 + "" +i

'''for i in list_in_btwn_overs:
    v=i in list_action_otherwise
    print(v)
    print('[',i,']')
for i in list_action_otherwise:
    print('[',i,']')'''
list_other_combined=list(set(list_action_otherwise+list_in_btwn_overs))
for i in list_action:
    for j in list_other_combined:
        if j in i:
            i=i.replace(j,"")
l=list()
for i in range(len(list_action)):
    for j in range(len(list_other_combined)):
        if(list_other_combined[j]==list_action[i]):
            list_action[i]=list_action[i].replace(list_other_combined[j],"")
    l.append(list_action[i])
print(",,,,, 2nd over" in list_other_combined)
for i in list_other_combined:
    print('[',i,']')


'''for i in range(0,len(list),2):
    a,b=list[i],list[i+1]
    l.append(tuple([b,a]))
dictionary=dict(tuple(l))
print(dictionary.keys(),'[........]',dictionary.values())
        if string1 is not ' ':
            list3.append(string1)'''

