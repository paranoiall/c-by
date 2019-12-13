# -*- coding=utf-8 -*-
from flask import Flask, request, make_response, jsonify
import json
from flask_cors import *

import main as cifa
import yufafenxi as yufa
import yuyifenxi as yuyi



app = Flask(__name__)
CORS(app, supports_credentials=True)


def write_code(code):
    dir = __file__[0:-11]
    #print(dir)
    f = open(dir+'file.txt', mode='w', encoding='utf-8')
    f.write(code)
    f.close

@app.route('/runcode',methods = ['POST'])
def runcode():      
    data = request.get_data()
    data = json.loads(data)
    #print(data)
    code = data['code']     
    write_code(code)        #写文件
    
    return jsonify("run")
  


@app.route('/cifa',methods = ['POST'])
def get_cifa():   
    print("cifa")
    data = request.get_data()
    data = json.loads(data)
    code = data['code']     
    write_code(code)        #写文件
    return jsonify(cifa.main())

@app.route('/bianyi',methods = ['POST'])
def bianyi():   
    print("bianyi")

    data = request.get_data()
    data = json.loads(data)
    #print(data)
    code = data['code']     
    write_code(code)        #写文件
    return jsonify(yuyi.create_siyuanshi())
  

@app.route('/print_tree',methods = ['POST'])
def print_tree():      
    print("print tree")

    r = yufa.create_tree()
    print(r[1])
    return jsonify(str(r[1]))




if __name__ == '__main__':
    dir = __file__[0:-11]
    print(dir)
    app.run('localhost','8081')