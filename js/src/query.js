import APPManager from './APPManager.js'
const allQueryTypes = [];

const addQueryType = (operation, args) => {
	allQueryTypes.push({
		operation: operation,
		args: args,
	})
}

addQueryType("select", {collectionID: "string"})
addQueryType("filter", {collectionID: "string"})

const query = function(){
	var queryDesc = [];

	for(var key in allQueryTypes){
		var queryType = allQueryTypes[key];
		this[queryType.operation] = ((queryType) => {	
			return (kwargs) => {
				var query = {};
				query['type'] = queryType.operation;
				for(var key in queryType.args){
					var argType = queryType.args[key];
					var val = kwargs[key];

					if(typeof val != argType){
						// raise exception;
						console.log("raise exception")
						return;
					}
					query[key] = val;

				}

				queryDesc.push(query);
				return this;
			}
		})(queryType);

	}

	this.debug = () => {
		console.log(queryDesc);
	}

	this.execute = function(callBack){
		APPManager.addQuery(queryDesc,callBack);
	}
}



export default query;

// this.select = (function(collectionID){
// 	queryDesc.push({operation: 'select', collectionID: collectionID});
// 	return new this.query(queryDesc);
// }).bind(this);
