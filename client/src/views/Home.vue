<template>
  <div class="home">
    <div class="input">
      <Mycode />
    </div>
    <div class="output">
      {{val}}
    </div>
  </div>
</template>

<script>

import Mycode from '@/components/Coder.vue'

export default {
  name: 'home',
  components: {
    Mycode
  },
  data(){
    return{
      val:""
    }
  },
  created: function () {
    // `this` points to the vm instance
  }
}
</script>

<style scoped>
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
  height: 500px;
}
/* .output>textarea{
  
} */
</style>
