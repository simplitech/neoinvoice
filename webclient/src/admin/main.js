import Vue from 'vue';
import VueMask from 'v-mask';
import VueMoment from 'vue-moment';
import App from './controller/App.vue';

// plugins
import AppBus from './service/AppBus';
import AppFilter from './service/AppFilter';
import AppResource from './service/AppResource';
import AppFragments from './controller/fragment';

// builders
import AppTranslator from './service/AppTranslator';
import AppRouter from './service/AppRouter';

Vue.lang = 'en';

Vue.use(VueMask);
Vue.use(VueMoment);
Vue.use(AppBus);
Vue.use(AppFilter);
Vue.use(AppResource);
Vue.use(AppFragments);

new Vue({
  el: '#app',
  i18n: AppTranslator(Vue),
  router: AppRouter(Vue),
  render: h => h(App),
});
