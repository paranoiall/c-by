

'''
语义分析预定义
'''

#符号表
err_meg = None
vartable = []
var = []
def var_lookup(item):
    global err_meg
    if item in vartable:
        return vartable.index(item)
    else:
        err_meg = 'Error：变量'+item+'未声明！'
        # exit(err_meg)

def var_insert(item):
    global err_meg
    if item not in vartable:
        vartable.append(item)
        return 1
    else:
        err_meg = 'Error：变量'+item+'重复声明！'
        # exit(err_meg)

#四元式
emit_result=[[]]
nxp=0
def emit(op,arg1,arg2,result):
    global nxp,emit_result
    emit_result[0].append([op,arg1,arg2,result])
    nxp = nxp+1

class emit_stack:
    def __init__(self):
        self.stack = [[]]

    def emit_push(self,op,arg1,arg2,result):
        global nxp
        self.stack[0].append([op,arg1,arg2,result])
        nxp = nxp+1

    def emit_pop(self, stack_out = 1):
        global emit_result
        if stack_out == 1:
            stack_out = emit_result
        global nxp
        for i in range(len(self.stack[0])):
            stack_out[0].append(self.stack[0].pop())

    def enterstack(self, addr, text):
        for i in range(len(self.stack[0])):
            for j in range(len(self.stack[0][i])):
                if self.stack[0][i][j] == addr and (j==1 or j==2):
                    self.stack[0][i][j] = text
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
    global emit_result,nxp
    for i in list:
        if emit_result[0][i][3] == None:
            emit_result[0][i][3] = 'L'+str(nxp)

def clear():
    global vartable,var,emit_stack,emit_result,nxp,temp_list,temp_now,word_now,err_meg
    err_meg = None
    vartable = []
    var = []
    emit_result=[[]]
    nxp=0
    temp_list={}
    temp_now=0
    word_now = ''
'''
语义分析预定义结束
'''
'''
语义分析开始
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


def val_cl(root, stack, num=0):

    if root.child[0].child[0].value == 'word':
        var_lookup(root.child[0].child[0].text)

    if root.child[1].child and root.child[1].child[0].type == 'SYMB':
        if root.child[0].child[0].value == '(':
            stack.emit_push(root.child[1].child[0].child[0].value, root.child[0].child[1].addr, root.child[1].child[1].addr, root.addr)
            val_cl(root.child[0].child[1], stack)
        else:
            stack.emit_push(root.child[1].child[0].child[0].value, root.child[0].child[0].text, root.child[1].child[1].addr, root.addr)
        val_cl(root.child[1].child[1], stack)
    else:
        if root.child[0].child[0].value == '(':
            stack.emit_push('=', root.child[0].child[1].addr, None, root.addr)
            val_cl(root.child[0].child[1], stack)
        elif root.child[0].child[0].value == 'number' or root.child[0].child[0].value == 'word':
            stack.emit_push('=', root.child[0].child[0].text, None, root.addr)
            # stack.enterstack(root.addr, root.child[0].child[0].text)


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
        stack = emit_stack()
        stack.emit_push('=', ids.child[1].addr, None, word_now)
        val_cl(ids.child[1], stack)
        stack.emit_pop()
        var_insert(word_now)
        word_now = ''
    # else:
        # exit('Error：变量声明错误！')


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
        if root.child[0].child[1].child:
            stack = emit_stack()
            stack.emit_push(root.child[0].child[1].child[0].child[0].value, root.child[0].child[0].addr, root.child[0].child[1].child[1].addr, None)
            val_cl(root.child[0].child[0],stack)
            # stack.emit_pop()
            val_cl(root.child[0].child[1].child[1], stack)
            stack.emit_pop()
            root.truelist.append(nxp-1)
            emit('jmp', None, None, None)
            root.falselist.append(nxp-1)
        else:
            stack = emit_stack()
            stack.emit_push('==', root.child[0].child[0].addr, 'true', None)
            val_cl(root.child[0].child[0], stack)
            stack.emit_pop()
            root.truelist.append(nxp-1)
            emit('jmp', None, None, None)
            root.falselist.append(nxp-1)
    # else:
        # exit('Error：BOOL表达式错误！')
        

def judge(root):
    global nxp
    if root.child[0].value == 'if':
        bool_cl(root.child[2])
        enterlist(root.child[2].truelist)
        yffx(root.child[5])
        emit('jmp', None, None, None)
        if_else = [nxp-1]
        enterlist(root.child[2].falselist)
        if root.child[7].child:
            yffx(root.child[7].child[2])
        enterlist(if_else)


    elif root.child[0].value == 'while':
        _while = 'L'+str(nxp)
        bool_cl(root.child[2])
        enterlist(root.child[2].truelist)
        yffx(root.child[5])
        emit('jmp', None, None, _while)
        enterlist(root.child[2].falselist)

    elif root.child[0].value == 'word':
        var_lookup(root.child[0].text)
        stack = emit_stack()
        stack.emit_push('=', root.child[2].addr, None, root.child[0].text)
        val_cl(root.child[2], stack)
        stack.emit_pop()

    elif root.child[0].value == 'printf':
        if root.child[2].child[0].value == 'word':
            var_lookup(root.child[2].child[0].text)
        emit('out', root.child[2].child[0].text, None, None)

    # else:
        # exit('Error：函数'+root.child[0].value+'未定义！')




def youhua():
    emit_d = []
    emit_replace = {}
    for i in range(len(emit_result[0])):
        if emit_result[0][i][1] != None and emit_result[0][i][3] != None:
            if emit_result[0][i][0] == '=' and str(emit_result[0][i][1])[0] !='T' and emit_result[0][i][2] == None and str(emit_result[0][i][3])[0] == 'T':
                # if isinstance(variate,int)
                emit_replace.update({emit_result[0][i][3]: emit_result[0][i][1]})
                emit_d.append(i)
    j=0
    for i in emit_d:
        del emit_result[0][i-j]
        
        for k in range(len(emit_result[0])):
            if emit_result[0][k][3] != None and emit_result[0][k][3][0] == 'L':
                if int(emit_result[0][k][3][1:]) > i-j:
                    emit_result[0][k][3] = 'L'+str(int(emit_result[0][k][3][1:])-1)
        j += 1

    for i in range(len(emit_result[0])):
        for key in emit_replace:
            if emit_result[0][i][1] != None:
                if emit_result[0][i][1] == key:
                    emit_result[0][i][1] = emit_replace[key]
            if emit_result[0][i][2] != None:
                if emit_result[0][i][2] == key:
                    emit_result[0][i][2] = emit_replace[key]
     


'''
语义分析结束
'''


import yufafenxi as yufa


def create_siyuanshi():
    clear()
    r = yufa.create_tree()
    if r[0]:
        yffx(r[1])
    else:
        return r
    youhua()
    emit('End', None, None, None)
    return emit_result[0]


if __name__ == "__main__":
    r = yufa.create_tree()
    yffx(r[1])
    youhua()
    emit('End', None, None, None)
    for i in range(len(emit_result[0])):
        print(i,':',emit_result[0][i])





