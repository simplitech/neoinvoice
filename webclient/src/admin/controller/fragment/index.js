import Default from './Default.vue';
import FormGroup from './form-group';
import Modal from './Modal.vue';

export default {
  install(Vue) {
    Vue.component('Default', Default);
    Vue.component('Modal', Modal);
    Vue.use(FormGroup);
  },
};
