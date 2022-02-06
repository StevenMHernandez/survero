import Vue from 'vue'
import _ from 'lodash'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import axios from 'axios'
import VueFullScreenFileDrop from 'vue-full-screen-file-drop';
import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';
import { DateTime } from 'luxon';

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

window.Vue = Vue;
window._ = _;
window.axios = axios;
window.VueFullScreenFileDrop = VueFullScreenFileDrop;
window.VueTypeaheadBootstrap = VueTypeaheadBootstrap;
window.DateTime = DateTime;
