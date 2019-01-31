import APPManager from './APPManager.js'
import query from './query.js'

var core = function(){
	this.init = (args = {} ) => {
		APPManager.connect(args.publicKey);
	}
	this.query = function(){
		return new query();
	}
}



window.companyName = new core();



































