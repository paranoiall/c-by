<template>
    <div>
      <div class="opt">      
        <el-button type="primary" @click="run_code">运行</el-button>
        <el-button type="primary" @click="comp_code">编译</el-button>
        <el-button type="primary" @click="get_cifa">查看词法</el-button>
        <el-button type="primary" @click="print_gram">查看语法树</el-button>
        <el-button type="primary" class="info" @click="dialog_show = true">说明</el-button>
        <el-dialog
          title="说明"
          :visible.sync="dialog_show"
          width="30%"
          center>
          <span>具体语法说明</span>
          <div>
            <p>1.函数应为int main(){...}，只能定义一个函数</p>
            <p>2.变量声明应该在一个函数体的开始</p>
            <p>3.逻辑符号(&& ||)左右的布尔判断应在一个小括号内，例如：(...)&&(...)</p>
            <p>4.printf可以输出一个字符串或者一个已定义的变量</p>            
          </div>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialog_show = false">取 消</el-button>
            <el-button type="primary" @click="dialog_show = false">确 定</el-button>
          </span>
        </el-dialog>
      </div>

      <div class="home">
        <div id="code" class="input">
          <codemirror  ref="myCm"  v-model="item.content"  :options="cmOptions"   @changes="onCmCodeChange" class="code" ></codemirror>
        </div>
        <div class="output">
          <div v-show="out_type == 1">
            <p v-bind:key="index" v-for="(item,index) in out_val" v-show="out_val[0] != 0">
              {{item != null?item:"null"}}  
            </p>
            <p v-show="out_val[0] == 0">
              {{out_val[1]}}
            </p>
          </div>
          <div v-show="out_type == 2||out_type == 3">
            <p v-bind:key="index" v-for="(item,index) in out_val" v-show="out_val[0] != 0">
              {{item}}
            </p>
            <p v-show="out_val[0] == 0">
              {{out_val[1]}}
            </p>
          </div><!--
          <div v-show="out_type == 3">
            <p v-bind:key="index" v-for="(item,index) in out_val" v-show="out_val[0] != 0">
              {{item?item:"null"}}
            </p>
            <p v-show="out_val[0] == 0">
              {{out_val[1]}}
            </p>
          </div>-->
          <div v-show="out_type == 4" class="tree">
            {{out_val}}
          </div>
        </div>
      </div>
    </div>
</template>
 

 
<script>
// language js
import 'codemirror/mode/javascript/javascript.js'
// theme css
import 'codemirror/theme/base16-dark.css'
//导入使用的语言语法定义文件
require("codemirror/mode/python/python.js");
require("codemirror/mode/javascript/javascript.js");
require("codemirror/mode/clike/clike.js"); //导入选中的theme文件

require("codemirror/theme/blackboard.css");
//导入自动提示核心文件及样式
require("codemirror/addon/hint/show-hint.css");

require("codemirror/addon/hint/show-hint.js");
//导入指定语言的提示文件
require("codemirror/addon/hint/javascript-hint.js");
require('codemirror/addon/edit/matchbrackets');
require('codemirror/addon/selection/active-line');


import axios from 'axios'
export default {
  name: "Mycoder",
  components:{
  },
  data () {
    return {
      out_val:'',
      out_type: 1,
      dialog_show:false,


      item:{
        content:""
      },
      cmOptions: {
        indentUnit: 4,
        tabSize: 4,
        mode: 'text/x-csrc',
        theme: 'default',
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        matchBrackets: true,
        autofocus:true,
        extraKeys: {
            "Shift-Tab": (cm) => {              // 反向缩进   
                if (cm.somethingSelected()) {
                    cm.indentSelection('subtract');  // 反向缩进
                } else {
                    // cm.indentLine(cm.getCursor().line, "subtract");  // 直接缩进整行
                    const cursor = cm.getCursor();
                    cm.setCursor({line: cursor.line, ch: cursor.ch - 4});  // 光标回退 indexUnit 字符
                }   
                return ;
            },  
            "Ctrl-B": (cm)=>{   //编译
                let val = cm.getValue();
                //校验表单数据
                
                window.console.log("hhh",val)   
                
            },
            "Ctrl-R":()=>{  //运行
                window.console.log("run")
                return;
            }
        }
      }
    }
  },
  methods: {
    onCmReady(cm) {
      window.console.log('the editor is readied!', cm)
    },
    onCmFocus(cm) {
      window.console.log('the editor is focus!', cm)
    },
    onCmCodeChange(newCode) {
    //   window.console.log('this is new code', newCode)
       this.code = newCode
    },



    run_code(){
      //window.console.log("run");
      var that = this;
      this.out_type = 1;
      axios({
        method:"POST",
        url:"http://localhost:8081/runcode",
        data:{
          code: that.item.content
        },
        headers:{
        'Content-type': 'application/x-www-form-urlencoded'
        },
      })
      .then((res)=> {
        window.console.log(res.data);
        that.out_val = res.data;
      })
      .catch((err)=> {
        window.console.log(err);
      });
    },
    comp_code(){
      window.console.log("编译");
      var that = this;
      this.out_type = 2;
      axios({
        method:"POST",
        url:"http://localhost:8081/bianyi",
        data:{
          code: that.item.content
        },
        headers:{
        'Content-type': 'application/x-www-form-urlencoded'
        },
      })
      .then((res)=> {
        window.console.log(res.data);
        that.out_val = res.data;
      })
      .catch((err)=> {
        window.console.log(err);
      });
    },
    get_cifa(){
      window.console.log("编译");
      var that = this;
      this.out_type = 3;
      axios({
        method:"POST",
        url:"http://localhost:8081/cifa",
        data:{
          code: that.item.content
        },
        headers:{
        'Content-type': 'application/x-www-form-urlencoded'
        },
      })
      .then((res)=> {
        window.console.log(res.data);
        that.out_val = res.data;
      })
      .catch((err)=> {
        window.console.log(err);
      });
    },
    print_gram(){
      window.console.log("语法树")

      var that = this;
      this.out_type = 4;
      axios({
        method:"POST",
        url:"http://localhost:8081/print_tree",
        data:{
          code: that.item.content
        },
        headers:{
        'Content-type': 'application/x-www-form-urlencoded'
        },
      })
      .then((res)=> {
        window.console.log(res.data);
        that.out_val = res.data;
      })
      .catch((err)=> {
        window.console.log(err);
      });
    }
  },
  computed: {
    codemirror() {
      return this.$refs.myCm.codemirror
    }
  },
  mounted() {
    window.console.log('this is current codemirror object', this.codemirror)
    // you can use this.codemirror to do something...
  }
}
</script>


<style>
#code{
  overflow-y: scroll;
}
.CodeMirror{
    /* border: 1px solid #eee; */
    height: 500px !important;
    font-size: 20px !important;
}
div{
    text-align: left;
}






/**/
.home{
  display: flex;
}
.input,.output{
  margin: 10px;
  border:1px solid #ddd;
}
.input{
  width: 60%;
  
}
.output{
  width: 40%;
  overflow-y: scroll;
  overflow-x: scroll;
  height: 500px;
}
.tree{
  white-space: pre;
}
</style>