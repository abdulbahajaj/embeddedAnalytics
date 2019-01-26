import APPManager from './APPManager.js'
import query from './query.js'

var core = function(){
	this.init = (public_key,onReady=function(){}) => {
		APPManager.connect(public_key);
	}
	this.query = function(){
		return new query();
	}
}



window.companyName = new core();



































