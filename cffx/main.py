import os

_key = ['int','long','short','float','double','if','else','while','continue','break','return','printf']
_num = ['0','1','2','3','4','5','6','7','8','9']
_jiefu = ['(',')','{','}',';',',']
_symbol1 = ['+','-','*','/','%']
_symbol2 = ['=','>','<','!','&','|']

def openfile():
    with open('file.txt') as f:
        lines = f.read()
    return lines

def main():
    def err():
        print('error:')
        print(i)
        exit()
        
    words = []
    word_now = ''
    word_space = 0
    lines = openfile()
    for i in lines:
        if word_space==0:
            if i=='\n' or i==' ' or i=='\t':
                pass
            
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
                words.append(['symbol_yunsuan',i])
            elif i in _symbol2:
                word_space = 1
                word_kind = 'symbol'
                word_now = i
            else:
                err()
                
        elif word_space==1:
            if i=='\n' or i==' ' or i=='\t':
                words.append([word_kind,word_now])
                word_kind = ''
                word_now = ''
                word_space = 0

            elif word_kind=='value':
                if i=='"':
                    words.append([word_kind,word_now])
                    word_kind = ''
                    word_now = ''
                    word_space = 0
                else:
                    word_now = word_now + i
                    
            elif i in _jiefu:
                words.append([word_kind,word_now])
                words.append(['jiefu',i])
                word_kind = ''
                word_now = ''
                word_space = 0
                
            elif i in _symbol1:
                words.append([word_kind,word_now])
                words.append(['symbol_yunsuan',i])
                word_kind = ''
                word_now = ''
                word_space = 0
                
            elif word_kind=='symbol':
                if word_now=='&' or word_now=='|':
                    if word_now == i:
                        word_now = word_now + i
                        words.append(['symbol_luoji',word_now])
                        word_kind = ''
                        word_now = ''
                        word_space = 0
                    else:
                        err()
                        
                elif i=='=':
                    word_now = word_now + i
                    words.append(['symbol_bijiao',word_now])
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
                    words.append(['symbol_bijiao',word_now])
                    word_kind = 'number'
                    word_now = int(i)
                    
                elif (i>='a' and i<='z') or (i>='A' and i<='Z') or i=='_':
                    words.append(['symbol_bijiao',word_now])
                    word_kind = 'word'
                    word_now = i
                    
                else:
                    err()
                    
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
                
    for i in words:
        if i[0]=='header':
            if i[1]=='define':
                i[0] = 'define'
            elif i[1][0:7]=='include':
                i[0] = 'include'
            else:
                err()
                
        elif i[0]=='word':
            if i[1] in _key:
                i[0] = 'key'
    return words

print(main())
print("finish!")
