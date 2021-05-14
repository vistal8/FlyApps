import Vue from 'vue'
/*
1、导入对象
2.Vue.use()
3.创建store对象
4.挂载

*/
import Vuex from 'vuex'

Vue.use(Vuex);
const store = new Vuex.Store({
    state: {
        userinfo: {},
        currentapp: {},
        appInfoIndex: [],
        userInfoIndex: 0,
        show_domain_msg: false,
    },
    mutations: {
        setuserinfo(state, data) {
            state.userinfo = data;
        },
        setappInfoIndex(state, val) {
            state.appInfoIndex = val
        },
        setuserInfoIndex(state, val) {
            state.userInfoIndex = val
        },
        setcurrentapp(state, val) {
            state.currentapp = val
        },
        setdomainshow(state, val) {
            state.show_domain_msg = val
        }
    },
    actions: {
        dodomainshow(context, data) {
            context.commit('setdomainshow', data);
        },
        doUserinfo(context, data) {
            context.commit('setuserinfo', data);
        },
        doappInfoIndex(context, val) {
            context.commit('setappInfoIndex', val)
        },
        douserInfoIndex(context, val) {
            context.commit('setuserInfoIndex', val)
        },
        doucurrentapp(context, val) {
            context.commit('setcurrentapp', val)
        }
    }
});


export default store;
