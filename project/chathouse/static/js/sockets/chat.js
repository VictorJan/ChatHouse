class ChatSocket{
	#token;
	#socket;
	#dnt;
	constructor(token,chat_identification){
		this.#token = token;
		this.#socket = io(`${window.origin}/socket/chat`,{ extraHeaders:{Authorization:`Bearer ${token.raw}`}, query:{chat_id:chat_identification}, multiplex:false});
		this.#dnt;
		this.#set_up();
	}

	#set_up(){
		
		this.#socket.on('disconnect',() =>{
			//refresh the token , if successful proceed to reconnect
			userInstance.refresh_access().then((token)=>{
				this.#token=token;
				//Change the Authorization headers, injecting a new access token
				this.#socket.io.opts["extraHeaders"]["Authorization"]=`Bearer ${token.raw}`;
				this.#socket.connect();
			});
		});

		//established message notification - is the event meant to notify about the creation of the message, appending it to the chat.
		this.#socket.on('established_message',(data)=>{
			//data:{id:int , sender:{id:int,username:str}, content:{iv:str,data:str}, dnt:{timestamp:int,readable:str} }
			console.log(data);
			//By receiving the payload - decrypt the incoming content of the message
			(chatInstance.receive(data.content)).then((decrypted)=>{
				console.log(decrypted)
				//structure a proper payload object.
				let block_payload = {id:data.id,sender:data.sender,content:decrypted,dnt:data.dnt.readable};
				//build a message block and append it to the chat.
				message(block_payload);
			})
		});

		//discharged message notification - is the event meant to notify about the "crossing out" of a message, removing it from the chat.
		this.#socket.on('discharged_message',(data)=>{
			//data:{chat:{id:int,name:str},action:'remove|add',subject:'chat|message'}
			console.log(data);
		});

	}

	establish_a_message(data){
		//data: {content:{iv:str,data:str}}
		//emits the provided payload data to the "establish_a_message" event.
		this.#socket.emit('establish_a_message', data);
	}
}