import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import axios from 'axios'
import VueFullScreenFileDrop from 'vue-full-screen-file-drop';
import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

window.Vue = Vue;
window.axios = axios;
window.VueFullScreenFileDrop = VueFullScreenFileDrop;
window.VueTypeaheadBootstrap = VueTypeaheadBootstrap;
