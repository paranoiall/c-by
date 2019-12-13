import yufafenxi

'''
语义分析开始
'''
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

'''
语义分析结束
'''
def create_siyuanshi():
    r = yufafenxi.create_tree()
    yffx(r[1])
    return emit_result

if __name__ == "__main__":
    r = yufafenxi.create_tree()

    # 语义分析
    yffx(r[1])
    
    for i in range(len(emit_result)):
        print(i,':',emit_result[i])
