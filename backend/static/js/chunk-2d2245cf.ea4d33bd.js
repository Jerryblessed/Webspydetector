(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d2245cf"],{e08f:function(t,e,s){"use strict";s.r(e);var a=function(){var t=this,e=t._self._c;return e("div",{staticClass:"backend-content",attrs:{id:"content"}},[e("div",{staticClass:"column col-12 col-xs-12"},[e("h3",{staticClass:"s-title"},[t._v("Search whitelisted elements")]),e("div",{staticClass:"form-group"},[e("textarea",{directives:[{name:"model",rawName:"v-model",value:t.elements,expression:"elements"}],staticClass:"form-input",attrs:{id:"input-example-3",placeholder:"Paste the elements here",rows:"3"},domProps:{value:t.elements},on:{input:function(e){e.target.composing||(t.elements=e.target.value)}}})]),e("div",{staticClass:"form-group"},[e("button",{staticClass:"btn btn-primary col-12",on:{click:function(e){return t.search_elements()}}},[t._v("Search")])]),t.results.length>0?e("div",{staticClass:"form-group"},[e("table",{staticClass:"table table-striped table-hover"},[t._m(0),e("tbody",t._l(t.results,(function(s){return e("tr",{key:s.element},[e("td",[t._v(t._s(s.element))]),e("td",[t._v(t._s(s.type))]),e("td",[e("button",{staticClass:"btn btn-sm",on:{click:function(e){return t.remove(s)}}},[t._v("Delete")])])])})),0)])]):0==t.first_search?e("div",[e("div",{staticClass:"empty"},[e("p",{staticClass:"empty-title h5"},[t._v("Element"),this.elements.match(/[^\r\n]+/g).length>1?e("span",[t._v("s")]):t._e(),t._v(" not found.")]),e("p",{staticClass:"empty-subtitle"},[t._v("Try wildcard search to expend your search.")])])]):t._e()])])},n=[function(){var t=this,e=t._self._c;return e("thead",[e("tr",[e("th",[t._v("Element")]),e("th",[t._v("Element type")]),e("th")])])}],l=s("bc3a"),r=s.n(l),i={name:"elements-search",data(){return{results:[],first_search:!0,jwt:""}},props:{},methods:{search_elements:function(){return this.results=[],this.first_search=!1,this.elements.match(/[^\r\n]+/g).forEach(t=>{r.a.get("/api/whitelist/search/"+t.trim(),{timeout:1e4,headers:{"X-Token":this.jwt}}).then(t=>{t.data.results.length>0&&(this.results=[].concat(this.results,t.data.results))}).catch(t=>console.log(t))}),!0},remove:function(t){r.a.get("/api/whitelist/delete/"+t.id,{timeout:1e4,headers:{"X-Token":this.jwt}}).then(e=>{e.data.status&&(this.results=this.results.filter((function(e){return e!=t})))}).catch(t=>console.log(t))},async get_jwt(){await r.a.get("/api/get-token",{timeout:1e4}).then(t=>{t.data.token&&(this.jwt=t.data.token)}).catch(t=>console.log(t))}},created:function(){this.get_jwt()}},c=i,o=s("2877"),h=Object(o["a"])(c,a,n,!1,null,null,null);e["default"]=h.exports}}]);
//# sourceMappingURL=chunk-2d2245cf.ea4d33bd.js.map