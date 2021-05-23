class NotificationSocket{
	constructor(token){
	this.token = token;
	this.socket = io(`${window.origin}/socket/notification`,{ extraHeaders:{Authorization:`Bearer ${token.raw}`}, multiplex:false});
	this.#set_up();
	}

	#set_up(){
		//chat notification - is the event meant to notify about any action such as : a new message has been added\removed or a new chat created\removed.
		this.socket.on('chat_notification',(data)=>{
			//data:{chat:{id:int,name:str},action:'remove|add',subject:'chat|message'}
			console.log('new_chat')
		});

		this.socket.on('disconnect',() =>{
			//try to resolve the acess token
			access_token_promise=prepare_access();
			//If the resolution was successful -> reconnect using the new token.
			access_token_promise.then((token)=>{
				this.token=token;
				//Change the Authorization headers, injecting a new access token
				this.socket.io.opts["extraHeaders"]["Authorization"]=`Bearer ${token.raw}`;
				this.socket.connect();
			});
		})
	}

	start_chat(data){
		//data: {participant_id:<Number>,<name>:<str>}
		this.socket.emit('start_a_chat',{'a':2})
	}
}