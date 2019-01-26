import APPManager from './APPManager.js'

var core = function(){
	this.init = (public_key,onReady=function(){}) => {
		APPManager.connect(public_key);
	}
	this.query = new function(queryDesc=[]){
		this.select = (function(collectionID){
			queryDesc.push({operation: 'select', collectionID: collectionID});
			return new this.query(queryDesc);
		}).bind(this);
		this.execute = function(callBack){
			APPManager.addQuery(queryDesc,callBack);
		}
	}
}



window.companyName = new core();



































