class node:
    truelist=[]
    falselist=[]
    nestlist=[]

#符号表
vartable=[]
def var_lookup(item):
    if item in vartable:
        return vartable.index(item)
    else:
        return null
def var_insert(item):
    vartable.append(item)

#四元式
emit_result=[]
nxp=1
def emit(op,arg1,arg2,result):
    emit_result.append([op,arg1,arg2,result])
    nxp = nxp+1

#临时变量
temp_list={}
temp_now=0
def newtemp():
    global temp_now
    temp_list.update({'L'+str(temp_now): None})
    temp_now = temp_now+1


def makelist(item):
    return [item]

def merge(list1,list2):
    return list1+list2
    
def backpatch(list, item):
    for i in range(len(list)):
        list[i] = item

a=node()
b=node()

a.truelist = makelist(1)
b.truelist = makelist(2)
a.truelist = merge(a.truelist, b.truelist)
print(a.truelist)
