import Vue from 'vue'
import App from './App.vue'
import router from './router'

import VueCodemirror from 'vue-codemirror' 
// require styles
import 'codemirror/lib/codemirror.css'  
// you can set default global options and events when use
Vue.use(VueCodemirror)

import { Button,Dialog} from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(Button)
Vue.use(Dialog)
 

import VueResource from 'vue-resource'
Vue.use(VueResource);

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
