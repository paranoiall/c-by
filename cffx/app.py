# -*- coding=utf-8 -*-
from flask import Flask, request, make_response, jsonify
import json
from flask_cors import *

import main as cifa
import yufafenxi as yufa
import yuyifenxi as yuyi
import run 



app = Flask(__name__)
CORS(app, supports_credentials=True)


def write_code(code):
    dir = __file__[0:-11]
    #print(dir)
    f = open(dir+'file.txt', mode='w', encoding='utf-8')
    print(dir)
    f.write(code)
    f.close

@app.route('/runcode',methods = ['POST'])
def runcode():      
    data = request.get_data()
    data = json.loads(data)
    # #print(data)
    code = data['code']     
    write_code(code)        #写文件
    res = run.res()
    if(len(res)):
        return jsonify(res)
    else:
        return jsonify("")
  


@app.route('/cifa',methods = ['POST'])
def get_cifa():   
    print("cifa")
    data = request.get_data()
    data = json.loads(data)
    code = data['code']     
    write_code(code)        #写文件
    res = cifa.main()
    if cifa.err_meg != None:
        return jsonify([0,cifa.err_meg])
    return jsonify(res)     

@app.route('/bianyi',methods = ['POST'])
def bianyi():   
    print("bianyi")

    data = request.get_data()
    data = json.loads(data)
    code = data['code']     
    write_code(code)        #写文件
    res = yuyi.create_siyuanshi()
    print(res)
    if res[0] == False:
        return jsonify([0,res[1]])
    return jsonify(res)
  

@app.route('/print_tree',methods = ['POST'])
def print_tree():      
    print("print tree")
    data = request.get_data()
    data = json.loads(data)
    code = data['code']     
    write_code(code)    
    
    r = yufa.create_tree()
    print(r[1])
    return jsonify(str(r[1]))



if __name__ == '__main__':
    dir = __file__[0:-11]
    print(dir)
    app.run('localhost','8081')