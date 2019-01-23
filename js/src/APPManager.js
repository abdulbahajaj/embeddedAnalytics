import { createStore } from 'redux'


const PARAMETERS = {
	host: "localhost",
	port: 8888,
	path: "client"
}


const ACTIONS = {
	ADD_QUERY: "addQuery",
	CONNECTED: 'connected',
	DISCONNECTED: "disconnected",
	CLEAR_QUERIES: "clearQueries",
	ADD_RESPONSE: "addResponse"
}

const queriesBufferReducer = (state, action) => {
	switch (action.type) {
		case ACTIONS.ADD_QUERY:
			state.queries.push({
				query: action.query,
				callBack: action.callBack,
			});
			break;
		case ACTIONS.CONNECTED:
			state.connected = true;
			break;
		case ACTIONS.CLEAR_QUERIES:
			state.queries = [];
			break;
		case ACTIONS.DISCONNECTED:
			state.connected = false;
			break;
	}
	return state
}

const queriesBuffer = createStore(queriesBufferReducer,{queries: [], connected: false})

// const responseBufferReducer = (state, action) => {
// 	switch (action.type) {
// 		case ACTIONS.ADD_RESPONSE:
// 			state.responses.push(action.response)
// 			break;
// 	}
// 	return state
// }

// const responseBuffer = createStore(responseBufferReducer,{responses: []})

const APPManager = new function(){
	this.subscribe = (func) => {
		return queriesBuffer.subscribe(func)
	}
	this.addQuery = (query, callBack) => {
		var action = {};
		action.type = ACTIONS.ADD_QUERY;
		action.query = query;
		action.callBack = callBack;
		queriesBuffer.dispatch(action);
	}
	this.connected = () => {
		var action = {};
		action.type = ACTIONS.CONNECTED;
		queriesBuffer.dispatch(action);
	}
	this.getState = () => {
		return queriesBuffer.getState();
	}
	this.getQueries = () => {
		var state = APPManager.getState();
		if(state.queries.length == 0){return [];}
		if(!state.connected){return [];}

		var queries = state.queries

		var action = {type: ACTIONS.CLEAR_QUERIES};
		queriesBuffer.dispatch(action)

		return queries;
	}
}

const connect = function(host, port, path){
	var connection = new WebSocket('ws://' + host + ":" + port + "/" + path);

	var allCallBacks = {};

	connection.onopen = () => {
		APPManager.connected();
	};
	connection.onerror = (error) => {
		console.log('WebSocket Error ' + error);
	};
	connection.onmessage = (response) => {
		response = response.data;
		response = JSON.parse(response);
		var data = response.data;
		var messageID = response.id;
		data = JSON.parse(data);
		allCallBacks[messageID](data);
	};

	function makeid() {
		var text = "";
		var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
		for (var i = 0; i < 30; i++)
			text += possible.charAt(Math.floor(Math.random() * possible.length));
		return text;
	}
	this.send = (message, callBack) => {
		const messageID = makeid();
		allCallBacks[messageID] = callBack;
		var message = {data: message, id: messageID};
		message = JSON.stringify(message);

		connection.send(message);		
	}

}

const Connection = new connect(PARAMETERS.host, PARAMETERS.port, PARAMETERS.path);

const startProcessing = function(){
	this.subscription = null;
	this.processQueries = () => {
		this.subscription();
		var queriesDesc = APPManager.getQueries();
		this.subscription = APPManager.subscribe(this.processQueries)

		for(var index in queriesDesc){
			var queryDesc = queriesDesc[index];
			var query = JSON.stringify(queryDesc.query);
			Connection.send(query, queryDesc.callBack);
		}
	}
	this.processQueries = this.processQueries.bind(this);
	this.subscription = APPManager.subscribe(this.processQueries)
}

new startProcessing();

export default APPManager;


























































