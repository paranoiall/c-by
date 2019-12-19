<template>
  <div id="app">
    <!-- <div class="opt">      
      <el-button type="primary">运行</el-button>
      <el-button type="primary">编译</el-button>
      <el-button type="primary">查看语法树</el-button>
      <el-button type="primary" class="info" >说明</el-button>
    </div>
    <div class="code">
      <Home></Home>
    </div> -->
    <Coder></Coder>
  </div>
</template>

<script>
import Coder from './components/Coder'
export default {
  components:{
    Coder
  },
  data(){
    return{

    }
  },
  methods:{

  }
}
</script>


<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  border: 1px solid #eee;
  margin: 30px 15px;
}

.opt{
  padding: 10px 30px;
  background-color: #eaebec;
}


.info{
  float: right;
}
</style>
