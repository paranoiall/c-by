import os
import sys
sys.setrecursionlimit(1000000)  #设置最大递归深度

import main
word_table = main.main()
# print(word_table)

#文法
grammars = {
    "P":    ["int main ( ) { FUNC }"],
    "FUNC":   [ "STAT FUNC" , "E FUNC" , "null"],
    "STAT":    ["int IDs"],
    "IDs":     ["word IDs_r"],
    "IDs_r":   [";", ", IDs", "= VAL ;"],
    "E":      ["word = VAL ;", "if ( BOOL_E ) { FUNC } E_else", "while ( BOOL_E ) { FUNC }", "printf ( P_VAL ) ;"],
    "E_else":   ["else { FUNC }", "null"],
    "BOOL_E":   ["! BOOL_E", "VAL_E", "( BOOL_E ) LOGIC ( BOOL_E )"],
    #"BOOL_E":      ["! BOOL_E LOGIC _BOOL_E",  "VAL_E LOGIC _BOOL_E", ],
   # "_BOOL_E":       ["LOGIC BOOL_E ", "null"],         #"( BOOL_E ) _BOOL_E",

    "P_VAL":    ["word", "value"],
    "VAL_E":   	["VAL VAL_E2"],
    "VAL_E2":   ["COMP VAL", "null"],
    "VAL":		["T VAL2"],
    "VAL2":      ["SYMB VAL", "null"],               #提公因子
    "T":        ["( VAL )", "word", "number"], 

    "LOGIC":    	["&&", "||"],
    "COMP":    [">", "<", ">=", "<=", "==", "!="],
    "SYMB":      ["+", "-", "*", "/", "%"]
}



'''
语义分析预定义
'''
#符号表
vartable = []
var = []
def var_lookup(item):
    if item in vartable:
        return vartable.index(item)
    else:
        exit('Error：变量'+item+'未声明！')

def var_insert(item):
    if item not in vartable:
        vartable.append(item)
        return 1
    else:
        exit('Error：变量'+item+'重复声明！')

#四元式
emit_result=[]
emit_stack=[]
nxp=0
def emit(op,arg1,arg2,result):
    global nxp
    emit_result.append([op,arg1,arg2,result])
    nxp = nxp+1

def emit_push(op,arg1,arg2,result):
    global nxp
    emit_stack.append([op,arg1,arg2,result])
    nxp = nxp+1

def emit_pop():
    global nxp
    for i in range(len(emit_stack)):
        emit_result.append(emit_stack.pop())

#临时变量
temp_list={}
temp_now=0
def newtemp():
    global temp_now
    temp_list.update({'T'+str(temp_now): None})
    temp_now = temp_now+1
    return 'T'+str(temp_now-1)

#回填地址
def enterlist(list):
    for i in list:
        if emit_result[i][3] == None:
            emit_result[i][3] = 'L'+str(nxp)

'''
语义分析预定义结束
'''




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
    def __init__(self, Type, value=None, text=None):
        self.type = Type
        self.value = value
        self.child = list()
        self.text = text

        self.addr = ''
        self.truelist = []
        self.falselist = []
        self.nextlist = []

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
    global word_all, number_all
    stack = []          #符号栈
    root = Node("P")
    End = Node("#")
    stack.append(End)
    stack.append(root)
    index = 0       #下标

    while len(stack) != 0:
        # 独到    &&  ||   等等
        s_top = stack.pop()   #当前栈顶符号
        if s_top.type == "#" and len(stack) == 0:
            print("分析成功")
            return [True,root]

        elif s_top.type in grammars :   #当前栈顶符号为非终结符
            w = word_table[index][1]        #w 为输入串当前顶部
            if w in predict_table[s_top.type]:             # 读取的词法结果式终结符
                temp = predict_table[s_top.type][w] 
                arr = temp.split()

                if s_top.type == 'VAL':
                    s_top.addr = newtemp()
                    # print(s_top)

                nodelist = []   #暂时存放节点
                for item in arr:
                    if item in grammars:
                        nodelist.append(Node(item))
                    else:
                        if item == "null":
                            continue
                        nodelist.append(Node("notype",item))
                for item in nodelist:   #添加子节点
                    s_top.child.append(item)

                nodelist.reverse() #入栈前逆序
                for item in nodelist:   
                    stack.append(item)
                
                # for i in range(len(arr)-1,-1,-1):
                #     if arr[i] in grammars:    #产生式元素为非终结符
                #         temp_node = Node(arr[i])
                #     else:
                #         if arr[i] == "null":
                #             continue
                #         temp_node = Node("notype",arr[i])
                #     stack.append(temp_node)
                if show:
                    print("符号栈:", stack) 
                    print("输入串:",word_table[index:])
                    print("产生式:",s_top.type,"-->",temp)
                    print("匹配字符:",w,"\n")
                    print(temp.split())              
            else :                # 读取的词法结果  是word  number这类,word是终结符但xxxxxxxx   [word,xxxxxx]                
                w = word_table[index][0]        #    区别在此处

                # if w == 'word':
                #     word_all.append(word_table[index][1])    #标识符插入符号表  语义用
                # if w == 'number':
                #     number_all.append(word_table[index][1])

                #print("----------------",w)
                if w in predict_table[s_top.type]:             # 读取的词法结果式终结符
                    #print("----------------------")
                    temp = predict_table[s_top.type][w] 
                    arr = temp.split()

                    if s_top.type == 'VAL':     #语义分析用
                        s_top.addr = newtemp()
                        # print(s_top)

                    nodelist = []   #暂时存放节点
                    for item in arr:
                        if item in grammars:
                            nodelist.append(Node(item))
                        else:
                            if item == "null":
                                continue
                            nodelist.append(Node("notype",item))
                    for item in nodelist:   #添加子节点
                        s_top.child.append(item)

                    nodelist.reverse() #入栈前逆序
                    for item in nodelist:   
                        stack.append(item)
                    
                    if show:
                        print("符号栈:", stack) 
                        print("输入串:",word_table[index:])
                        print("产生式:",s_top.type,"-->",temp)
                        print("匹配字符:",w,"\n")  
                else:
                    print("error 2") 
                    print(s_top.value, " 与 ", word_table[index][1],"不匹配")
                    return
        elif s_top.type not in grammars:
            if s_top.value != word_table[index][1]:
                if word_table[index][0] == "word" or "number" and s_top.value == word_table[index][0]:  #为了文法里word的坑   
                    if show:                 
                        print("符号栈:", stack) 
                        print("输入串:",word_table[index:])
                        print("匹配并出栈字符:",s_top.value,"\n") 
                    s_top.text = word_table[index][1]
                    #val  addr = newtemp()
                    index += 1
                else:
                    print("error")
                    print(s_top.value, " 与 ", word_table[index][1],"不匹配")
                    return
            elif s_top.value == word_table[index][1]:
                if show:
                    print("符号栈:", stack) 
                    print("输入串:",word_table[index:])
                    print("匹配并出栈字符:",s_top.value,"\n") 
                # if(index == len(word_table)-1):
                #     print("final ",stack)
                index += 1






def create_tree():      #返回语法树
    get_first_table()
    find_follow()
    get_predict_table()
    r = LL1()
    return r

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
    # print("\n预测表如下\n")
    # for k in predict_table:
    #     print(k, predict_table[k])
    show = False
    r = LL1(show)
    print("\n语法树:")
    print(r[1])

    # # 语义分析
    # yffx(r[1])
    # for i in range(len(emit_result)):
    #     print(i,':',emit_result[i])








'''
语义分析开始


def yffx(root):
    if root == None:
        return None
    elif len(root.child) == 0 and root.value != None:
        return root.value
    elif root.type == "STAT":
        math_op(root)
    elif root.type == "E":
        judge(root)
    else:
        for c in root.child:
            yffx(c)
        return None


def val_cl(root):
    if root.child[0].child[0].value == '(':
        emit_push('=', root.child[0].child[1].addr, None, root.addr)
        val_cl(root.child[0].child[1])
        
    # 出错了用下面这个
    # elif root.child[1].child:
    #     if root.child[1].child[0].type == 'SYMB':
    #         if root.child[0].child[0].value == 'word':
    #             var_lookup(root.child[0].child[0].text)
    #         emit_push(root.child[1].child[0].child[0].value, root.child[0].child[0].text, root.child[1].child[1].addr, root.addr)
    #         val_cl(root.child[1].child[1])

    # elif root.child[0].child[0].value == 'word':
    #     var_lookup(root.child[0].child[0].text)
    #     root.addr = root.child[0].child[0].text
    #     # 出错了用下面这个，需要简化四元式
    #     # emit_push('=', root.child[0].child[0].text, None, root.addr)

    elif root.child[0].child[0].value == 'word':
        var_lookup(root.child[0].child[0].text)
        if root.child[1].child and root.child[1].child[0].type == 'SYMB':
                emit_push(root.child[1].child[0].child[0].value, root.child[0].child[0].text, root.child[1].child[1].addr, root.addr)
                val_cl(root.child[1].child[1])
        else:
            if root.addr:
                emit_push('=', root.child[0].child[0].text, None, root.addr)
            else:
                root.addr = root.child[0].child[0].text
            # 出错了用下面这个，需要简化四元式
            # emit_push('=', root.child[0].child[0].text, None, root.addr)
    
    elif root.child[0].child[0].value == 'number':
        emit_push('=', root.child[0].child[0].text, None, root.addr)
        
    else:
        exit('Error：赋值错误！')


word_now = ''
def math_op(root):
    global word_now
    ids = root.child[1]
    if ids.child[0].value == 'word':
        word_now = ids.child[0].text
        math_op(root.child[1])

    elif ids.child[0].value == ';':
        var_insert(word_now)
        emit('=', None, None, word_now)
        word_now = ''

    elif ids.child[0].value == ',':
        var_insert(word_now)
        emit('=', None, None, word_now)
        word_now = ''
        math_op(root.child[1])

    elif ids.child[0].value == '=':
        ids.child[1].addr = word_now
        val_cl(ids.child[1])
        emit_pop()
        var_insert(word_now)
        word_now = ''
    else:
        exit('Error：变量声明错误！')


def bool_cl(root): 
    global nxp
    if root.child[0].value == '!':
        root.truelist = root.child[1].falselist
        root.falselist = root.child[1].truelist
        bool_cl(root.child[1])

    elif root.child[0].value == '(':
        if root.child[3].child[0].value == '&&':
            bool_cl(root.child[1])
            enterlist(root.child[1].truelist)
            root.falselist.extend(root.child[1].falselist)
            bool_cl(root.child[5])
            root.truelist.extend(root.child[5].truelist)
            root.falselist.extend(root.child[5].falselist)

        elif root.child[3].child[0].value == '||':
            bool_cl(root.child[1])
            enterlist(root.child[1].falselist)
            root.truelist.extend(root.child[1].truelist)

            bool_cl(root.child[5])
            root.truelist.extend(root.child[5].truelist)
            root.falselist.extend(root.child[5].falselist)

    elif root.child[0].child[0].type == 'VAL':
        val_cl(root.child[0].child[0])
        emit_pop()
        if root.child[0].child[1].child:
            val_cl(root.child[0].child[1].child[1])
            emit_pop()
            emit(root.child[0].child[1].child[0].child[0].value, root.child[0].child[0].addr, root.child[0].child[1].child[1].addr, None)
            root.truelist.append(nxp-1)
            emit('jmp', None, None, None)
            root.falselist.append(nxp-1)
        else:
            emit('==', root.child[0].child[0].addr, 'true', None)
            root.truelist.append(nxp-1)
            emit('jmp', None, None, None)
            root.falselist.append(nxp-1)
    else:
        exit('Error：BOOL表达式错误！')
        

def judge(root):
    if root.child[0].value == 'if':
        bool_cl(root.child[2])
        enterlist(root.child[2].truelist)
        yffx(root.child[5])
        enterlist(root.child[2].falselist)
        if root.child[7]:
            yffx(root.child[7].child[2])

    elif root.child[0].value == 'while':
        bool_cl(root.child[2])
        enterlist(root.child[2].truelist)
        yffx(root.child[5])
        enterlist(root.child[2].falselist)

    elif root.child[0].value == 'word':
        var_lookup(root.child[0].text)
        root.child[2].addr = root.child[0].text
        val_cl(root.child[2])
        emit_pop()

    elif root.child[0].value == 'printf':
        emit('out', root.child[2].child[0].text, None, None)

    else:
        exit('Error：函数'+root.child[0].value+'未定义！')

语义分析结束
'''