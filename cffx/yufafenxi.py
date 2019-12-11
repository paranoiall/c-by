import os
import sys
sys.setrecursionlimit(1000000)  #设置最大递归深度

import main
word_res = main.cifafenxi()
print(word_res)

#文法
grammars = {
    "P":    ["int main ( ) { FUNC }"],
    "FUNC":   [ "STAT FUNC" , "E FUNC" , "null"],
    "STAT":    ["int IDs"],
    "IDs":     ["word IDs_r"],
    "IDs_r":   [";", ", IDs", "= VAL ;"],
    "E":      ["word = VAL ;", "if ( BOOL_E ) { FUNC } E_else", "while ( BOOL_E ) { FUNC }", "printf ( P_VAL ) ;"],
    "E_else":   ["else { FUNC }", "null"],
    "BOOL_E":      ["! BOOL_E _BOOL_E", "( BOOL_E ) _BOOL_E", "VAL_E _BOOL_E"],
    "_BOOL_E":       ["LOGIC VAL_E BOOL_E", "null"],

    "P_VAL":    ["word", "value"],
    "VAL_E":   	["VAL VAL_E2"],
    "VAL_E2":   ["COMP VAL", "null"],
    "VAL":		["T VAL2"],
    "VAL2":      ["SYMB VAL", "null"],               #提公因子
    "T":        ["( VAL )", "word", "number"], 

    "LOGIC":    	["&&", "||"],				            #symbol_luoji
    "COMP":    [">", "<", ">=", "<=", "==", "!="], 	    #symbol_bijiao
    "SYMB":      ["+", "-", "*", "/", "%"]		    #symbol_yunsuan 
}


'''
#语义时用   
'''
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






#查找指定非终结符的first集合
def find_first(key):
    if key not in grammars: 
        return [key]
    l = []
    for next_grammar in grammars[key]: 
        next_k = next_grammar.split()[0]
        l.extend(find_first(next_k))
    return l



first_table = {}
follow_table = {}
predict_table = {}
observer = {}

def get_first_table():
    for k in grammars:      #遍历每个非终结符        
        predict_table[k] = {}
        first_table[k] = []
        for next_grammar in grammars[k]:        #遍历产生式右部 获取FIRST元素
            next_k = next_grammar.split()[0]
            kl = find_first(next_k)
            first_table[k].extend(kl)
            for kk in kl:
                if kk != "null":
                    predict_table[k][kk] = next_grammar



#查找所有非终结符follow

def init_observer():    #将产生式右部最后符号为不等于左边非终截符的产生式添加至observer中
    for k in grammars:
        follow_table[k] = []
        observer[k] = []
        for next_grammar in grammars[k]:
            last_k = next_grammar.split()[-1]
            if last_k in grammars and last_k != k:
                observer[k].append(last_k) 

"""
刷新订阅
检测到某个follow集合更新时，对其订阅的所有产生式左部的follow集合进行更新
简而言之：follow（A）发生了更新，那么曾经将follow（A）加入自身的B，C也更新其follow
并且，这是一个递归过程
"""
def refresh(k):
    for lk in observer[k]:
        newlk = U(follow_table[k], follow_table[lk])
        if newlk != follow_table[lk]:
            follow_table[lk] = newlk
            refresh(lk)


#合并两个list并且去重
def U(A,B):
    return list(set(A+B))

#   #为结束符
def find_follow():
    init_observer()
    follow_table["P"] = ["#"]
    for k in grammars:
        for next_grammar in grammars[k]:
            next_k = next_grammar.split()
            
            for i in range(0,len(next_k)-1):
                if next_k[i] in grammars:
                    if next_k[i+1] not in grammars:                
                        #如果后继字符是终结符，加入                        
                        new_follow = U([next_k[i+1]], follow_table[next_k[i]])

                        if new_follow != follow_table[next_k[i]]:
                            follow_table[next_k[i]] = new_follow
                            refresh(next_k[i])
                    else:
                        new_follow = U(first_table[next_k[i+1]], follow_table[next_k[i]])
                        
                        #如果后继字符的first集合中含有null，通知所有订阅者更新follow集合                        
                        if "null" in first_table[next_k[i+1]]:
                            new_follow = U(follow_table[k], new_follow)
                            observer[k].append(next_k[i])
                        if new_follow != follow_table[next_k[i]]:
                            follow_table[next_k[i]] = new_follow
                            refresh(next_k[i])
            
            #产生式左部的follow集合加入最后一个非终结符的follow集合            
            if next_k[-1] in grammars:
                if next_k[-1] not in follow_table:
                    follow_table[next_k[-1]] = []
                if next_k[-1] != k:
                    follow_table[next_k[-1]] = U(follow_table[next_k[-1]], follow_table[k])

    for k in follow_table:
        if "null" in follow_table[k]:
            follow_table[k].remove("null")


"""
将follow集合中的部分内容加入predict表中
"""
def get_predict_table():
    for k in grammars:
        for next_grammar in grammars[k]:
            next_k = next_grammar.split()[0]
            if next_k in grammars and "null" in first_table[next_k] or next_k == "null":
                for fk in follow_table[k]:
                    predict_table[k][fk] = next_grammar     #等价于将产生式左边非终结符的follow集加入产生式的select集




# 语法树节点
class Node:
    def __init__(self, Type, value=None):
        self.type = Type
        self.value = value
        self.child = list()

    # 将语法树对象字符化输出
    def __str__(self):
        childs = list()
        for child in self.child:
            childs.append(child.__str__())
        out = "<{type}, {text}>".format(type=self.type, text=self.value)
        for child in childs:
            if child:
                for line in child.split("\n"):
                    out = out + "\n     " + line
        return out

    def __repr__(self):
        return self.__str__()





def LL1(show=False):
    stack = []          #符号栈
    root = Node("P")
    End = Node("#")
    stack.append(End)
    stack.append(root)
    index = 0       #下标

    word_table = word_res

    while len(stack) != 0:
        s_top = stack.pop()   #当前栈顶符号
        if s_top.type == "#" and len(stack) == 0:
            print("成功")
            return True
        elif s_top.type in grammars :   #当前栈顶符号为非终结符
            w = word_table[index][1]        #w 为输入串当前顶部
            if w in predict_table[s_top.type]:             # 读取的词法结果式终结符
                temp = predict_table[s_top.type][w] 
                arr = temp.split()
                for i in range(len(arr)-1,-1,-1):
                    if arr[i] in grammars:    #产生式元素为非终结符
                        temp_node = Node(arr[i])
                    else:
                        if arr[i] == "null":
                            continue
                        temp_node = Node("notype",arr[i])
                    stack.append(temp_node)
                    
                print(temp.split())  
                print("stack", stack)  
            else :                # 读取的词法结果  是word  number这类,word是终结符但xxxxxxxx   [word,xxxxxx]                
                w = word_table[index][0]        #    区别在此处
                print("----------------",w)
                if w in predict_table[s_top.type]:             # 读取的词法结果式终结符
                    #print("----------------------")
                    temp = predict_table[s_top.type][w] 
                    arr = temp.split()
                    for i in range(len(arr)-1,-1,-1):
                        if arr[i] in grammars:    #产生式元素为非终结符
                            temp_node = Node(arr[i])
                        else:
                            if arr[i] == "null":
                                continue
                            temp_node = Node("notype",arr[i])
                        stack.append(temp_node)
                    print(temp.split())  
                    print("stack", stack)
                else:
                    print("error 2") 
                    print(s_top, "---", word_table[index])
                    return
        elif s_top.type not in grammars:
            if s_top.value != word_table[index][1]:
                if word_table[index][0] == "word" or "number" and s_top.value == word_table[index][0]:  #为了文法里word的坑
                    print("not in ",s_top.value)
                    index += 1
                else:
                    print("error")
                    print(s_top.value, "---", word_table[index][1])
                    return
            elif s_top.value == word_table[index][1]:
                print("not in ",s_top.value)
                # if(index == len(word_table)-1):
                #     print("final ",stack)
                index += 1
            
        







if __name__ == "__main__":
    get_first_table()
    find_follow()
    get_predict_table()
    # get_first_table()
    # for k in first_table:
    #     print(k, first_table[k])
    # find_follow()
    # print("\nfollow \n")
    # for k in follow_table:
    #     print(k, follow_table[k])
    print("\n预测表如下\n")
    for k in predict_table:
        print(k, predict_table[k])

    
    LL1()