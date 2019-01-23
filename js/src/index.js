import APPManager from './APPManager.js'

var core = function(){
	this.init = (username,apikey,onReady=function(){}) => {

	}
	this.query = (queryDescription, callBack) => {
		APPManager.addQuery(queryDescription,callBack)
	}
}



window.companyName = new core();



































