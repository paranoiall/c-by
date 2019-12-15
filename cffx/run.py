import yuyifenxi as yuyi



var_table = {}
res_out = []

def run_code(s):
    i = 0
    while i < len(s):
        #print(i)
        if(s[i][0] == '='):
            var_table[s[i][3]] = (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1])
            #print(var_table)
        elif(s[i][0] == '+'):
            var_table[s[i][3]] = (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) + (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2])
        elif(s[i][0] == '-'):
            var_table[s[i][3]] = (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) - (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2])
        elif(s[i][0] == '*'):
            var_table[s[i][3]] = (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) * (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2])
        elif(s[i][0] == '/'):
            var_table[s[i][3]] = (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) // (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2])
        elif(s[i][0] == '%'):
            var_table[s[i][3]] = (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) % (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2])
        elif(s[i][0] == 'out'):
            out = var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]
            print("out",out)
            res_out.append(out)

        elif s[i][0] == '>' :               #比较运算符
            if (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) > (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2]):
                num = s[i][3][1:]                
                i = int(num)
                continue
        elif s[i][0] == '<':
            if (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) < (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2]):
                num = s[i][3][1:]
                i = int(num)
                continue
        elif s[i][0] == '>=':
            if (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) >= (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2]):
                num = s[i][3][1:]
                i = int(num)
                continue
        elif s[i][0] == '<=':
            if (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) <= (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2]):
                num = s[i][3][1:]
                i = int(num)
                continue
        elif s[i][0] == '!=':
            if (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) != (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2]):
                num = s[i][3][1:]
                i = int(num)
                continue
        elif s[i][0] == '==':
            if (var_table[s[i][1]] if(s[i][1] in var_table) else s[i][1]) == (var_table[s[i][2]] if(s[i][2] in var_table) else s[i][2]):
                num = s[i][3][1:]
                i = int(num)
                continue
        elif s[i][0] == 'jmp':      #跳转
            num = s[i][3][1:]
            i = int(num)
            continue
        elif s[i][0] == 'End':      #执行结束
            break
        i = i+1



def res():
    global res_out
    res_out = []
    s = yuyi.create_siyuanshi()
    if s[0]!=False:
        run_code(s)
    else:
        return [0,s[1]]
    return res_out

if __name__ == '__main__':
    s = yuyi.create_siyuanshi()
    print(yuyi.err_meg)
    
    if s[0]:
        run_code(s)
    else:
        print("s = ",s)
    #print(s)
    print(var_table)