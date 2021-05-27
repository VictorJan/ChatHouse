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
				//If reconnection hasn't been successful - the access token could be invalid or inappropriate according to a chat - thus refresh the page.
				if (this.#socket.connect().connected != true) window.location = window.location.href;
			});
		});

		//established message notification - is the event meant to notify about the creation of the message, appending it to the chat.
		this.#socket.on('established_message',(data)=>{
			//data:{id:int , sender:{id:int,username:str}, content:{iv:str,data:str}, dnt:{timestamp:int,readable:str} }
			//By receiving the payload - decrypt the incoming content of the message
			(chatInstance.receive(data.content)).then((decrypted)=>{
				if (decrypted){
					//structure a proper payload object.
					let block_payload = {id:data.id,sender:data.sender,content:decrypted,dnt:data.dnt.readable};
					//differ messages based if they were sent or received.
					let sent = data.sender.id == this.#token.payload.user_id;
					//build a message block and append it to the chat.
					message(block_payload,true,sent);
				}
				else{
					//Notify about the invalida payload in the encrypted content.
					notification(`A messsage from ${data.sender.username} coudn't be decrypted, due to invalid payload.`)
				}
			})
		});

		//discharged messages notification - is the event meant to notify about the messages that shall be removed from the chat.
		this.#socket.on('discharged_messages',(data)=>{
			//data:{messages:[<int>,<int>,...]}
			try{
				let chat_content = document.querySelector(".chat_content");
				let selector=[];
				//prepare a query for the selector
				data.messages.forEach((message)=>{
					selector.push(`[data-message_id='${message}']`);
				})

				//remove the discharged messages
				chat_content.querySelectorAll(selector.join()).forEach((message)=>{
					chat_content.removeChild(message);
				});
			}
			catch{
				notification("Coulnd't discharge messages, due to absence of the body of a chat.")
			}
		});

	}

	establish_a_message(data){
		//data: {content:{iv:str,data:str}}
		//emits the provided payload data to the "establish_a_message" event.
		this.#socket.emit('establish_a_message', data);
	}

	discharge_messages(data){
		//data: {messages:[<int>,<int>,...]}
		//emits the provided payload data to the "discharge_a_message" event.
		this.#socket.emit('discharge_messages', data);
	}
}