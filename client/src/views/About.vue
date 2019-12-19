<template>
  <codemirror  ref="myCm"  v-model="item.content"  :options="cmOptions"   @changes="changes" class="code" ></codemirror>
<!--
    <codemirror v-model="code" :options="cmOptions"></codemirror> 
    
    <codemirror ref="myCm"
                :value="code" 
                :options="cmOptions"
                @ready="onCmReady"
                @focus="onCmFocus"
                @input="onCmCodeChange">
    </codemirror>  
    <no-ssr placeholder="Codemirror Loading...">
      <codemirror ref="myCm"
                  :value="code" 
                  :options="cmOptions"
                  @ready="onCmReady"
                  @focus="onCmFocus"
                  @input="onCmCodeChange">
      </codemirror>
    </no-ssr>-->
</template>
 

 
<script>
// language js
import 'codemirror/mode/javascript/javascript.js'
// theme css
import 'codemirror/theme/base16-dark.css'

import { codemirror } from 'vue-codemirror'
require("codemirror/mode/python/python.js")
require('codemirror/addon/fold/foldcode.js')
require('codemirror/addon/fold/foldgutter.js')
require('codemirror/addon/fold/brace-fold.js')
require('codemirror/addon/fold/xml-fold.js')
require('codemirror/addon/fold/indent-fold.js')
require('codemirror/addon/fold/markdown-fold.js')
require('codemirror/addon/fold/comment-fold.js')
// more codemirror resources
// import 'codemirror/some-resource...'
export default {
  name: "mycoder",
  components:{
    codemirror
  },
  data () {
    return {
      item:{
        content:""
      },
      code: 'const a = 10',
      cmOptions: {
        // codemirror options
        tabSize: 4,
        mode: 'text/javascript',
        theme: 'base16-dark',
        lineNumbers: true,
        line: true,
        // more codemirror options, 更多 codemirror 的高级配置...
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
      window.console.log('this is new code', newCode)
      this.code = newCode
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