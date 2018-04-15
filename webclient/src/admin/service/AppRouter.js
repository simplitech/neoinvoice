/* eslint global-require: 0 */
import VueRouter from 'vue-router';

export default function buildRouter(Vue) {
  Vue.use(VueRouter);

  const router = new VueRouter({
    routes: [
      { path: '/login', component: require('../controller/Login.vue') },
      {
        path: '/home',
        component: require('../controller/fragment/Default.vue'),
        children: [
          { path: '/home', component: require('../controller/Wallet.vue') },
          { path: '/persistDomain', component: require('../controller/PersistDomain.vue') },
          { path: '/requestSubdomain', component: require('../controller/RequestSubdomain.vue') },

          { path: '/wallet/:wallet', component: require('../controller/Wallet.vue') },

          { path: '/domain/:domain', component: require('../controller/Domain.vue') },
          { path: '/transferDomain/:domain', component: require('../controller/TransferDomain.vue') },
          { path: '/persistSubdomain/:domain', component: require('../controller/PersistSubdomain.vue') },
          { path: '/persistMeta/:domain', component: require('../controller/PersistMeta.vue') },
          { path: '/persistPendingTransaction/:domain', component: require('../controller/PersistPendingTransaction.vue') },

          { path: '/payment/:domain/:idPendingTransaction', component: require('../controller/PendingTransaction.vue') },
        ],
      },
      { path: '/', redirect: '/login' },
      { path: '*', redirect: '/home' },
    ],
  });

  router.beforeEach((to, from, next) => {
    window.scrollTo(0, 0);
    next();
  });

  Object.assign(Vue, { $router: router });

  return router;
}
