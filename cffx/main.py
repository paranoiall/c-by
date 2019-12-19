import os

_key = ['int','long','short','float','double','if','else','while','continue','break','return','printf']
_num = ['0','1','2','3','4','5','6','7','8','9']
_jiefu = ['(',')','{','}',';',',']
_symbol1 = ['+','-','*','%']
_symbol2 = ['=','>','<','!','&','|']

def openfile():
    with open('../file.txt') as f:
        lines = f.readlines()
        f.close()
    return lines

err_meg = None

def main():
    global err_meg
    err_meg = None
    def err():
        global err_meg
        # print(word_now)
        err_meg = 'Error：'+i+'（Line'+str(line_num)+'）'
        # exit(err_meg)
    
        
    words = []
    word_now = ''
    word_space = 0
    word_next = 0
    lines = openfile()
    for line_num in range(len(lines)):
        word_next = 0
        for i in lines[line_num]:
            if word_next == 1:
                continue

            if word_space==0:
                if i=='\n' or i==' ' or i=='\t':
                    pass
                elif i == '/':
                    word_kind = 'SYMB'
                    word_space = 1
                    word_now = i
                elif (i>='a' and i<='z') or (i>='A' and i<='Z') or i=='_':
                    word_space = 1
                    word_kind = 'word'
                    word_now = i
                elif i in _num:
                    word_space = 1
                    word_kind = 'number'
                    word_now = int(i)
                elif i=='"':
                    word_space = 1
                    word_kind = 'value'
                elif i in _jiefu:
                    words.append(['jiefu',i])
                elif i in _symbol1:
                    words.append(['SYMB',i])
                elif i in _symbol2:
                    word_space = 1
                    word_kind = 'symbol'
                    word_now = i
                else:
                    err()
                    
            elif word_space==1:
                if word_kind=='value':
                    if i=='"':
                        words.append([word_kind,word_now])
                        word_kind = ''
                        word_now = ''
                        word_space = 0
                    else:
                        word_now = word_now + i
                        
                elif i=='\n' or i==' ' or i=='\t':
                    words.append([word_kind,word_now])
                    word_kind = ''
                    word_now = ''
                    word_space = 0
                        
                elif i in _jiefu:
                    words.append([word_kind,word_now])
                    words.append(['jiefu',i])
                    word_kind = ''
                    word_now = ''
                    word_space = 0
                    
                elif i in _symbol1:
                    words.append([word_kind,word_now])
                    words.append(['SYMB',i])
                    word_kind = ''
                    word_now = ''
                    word_space = 0

                elif word_kind=='symbol':
                    if word_now=='&' or word_now=='|':
                        if word_now == i:
                            word_now = word_now + i
                            words.append(['LOGIC',word_now])
                            word_kind = ''
                            word_now = ''
                            word_space = 0
                        else:
                            err()
                                         
                    elif i=='=':
                        word_now = word_now + i
                        words.append(['COMP',word_now])
                        word_kind = ''
                        word_now = ''
                        word_space = 0
                        
                    elif word_now=='=' or word_now=='!':
                        if i in _num:
                            words.append(['symbol',word_now])
                            word_kind = 'number'
                            word_now = int(i)
                        elif (i>='a' and i<='z') or (i>='A' and i<='Z') or i=='_':
                            words.append(['symbol',word_now])
                            word_kind = 'word'
                            word_now = i
                        else:
                            err()
                            
                    elif i in _num:
                        words.append(['COMP',word_now])
                        word_kind = 'number'
                        word_now = int(i)
                        
                    elif (i>='a' and i<='z') or (i>='A' and i<='Z') or i=='_':
                        words.append(['COMP',word_now])
                        word_kind = 'word'
                        word_now = i
                        
                    else:
                        err()

                elif i == '/':
                    if word_now == '/':
                        word_next = 1
                        word_space = 0
                        word_now = ''
                        continue
                    else:
                        words.append([word_kind,word_now])
                        words.append(['SYMB',i])
                        word_space = 0
                        word_now = ''
                        
                elif i in _symbol2:
                    words.append([word_kind,word_now])
                    word_kind = 'symbol'
                    word_now = i
                        
                elif word_kind=='number':
                    if i in _num:
                        word_now = int(word_now)*10 + int(i)
                    else:
                        err()
                        
                elif word_kind=='word':
                    if (i>='a' and i<='z') or (i>='A' and i<='Z') or i=='_' or (i in _num):
                        word_now = word_now + i
                    else:
                        err()
                else:
                    err()
                
        for i in range(len(words)):
            if len(words[i]) < 3:
                words[i].append(line_num)
            if words[i][0]=='word':
                if words[i][1] in _key:
                    words[i][0] = 'key'
    return words
    


if __name__ == "__main__":
    out = main()
    for i in range(len(out)):
        print(i,':',out[i])