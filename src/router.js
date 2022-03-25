import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Api from './views/Api.vue'
import Evaluate from './views/Evaluate.vue'
import Result from './views/Result.vue'
import Video from './views/Video.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/api',
      name: 'api',
      component: Api
    },
    {
      path: '/evaluate',
      name: 'evaluate',
      component: Evaluate
    },
    {
      path: '/result',
      name: 'result',
      component: Result
    },
    {
      path: '/video',
      name: 'video',
      component: Video
    }
  ]
})
