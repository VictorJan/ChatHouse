class NotificationSocket{
	#socket;
	constructor(token){
	this.token = token;
	this.#socket = io(`${window.origin}/socket/notification`,{ extraHeaders:{Authorization:`Bearer ${token.raw}`}, multiplex:false});
	this.#set_up();
	}

	#set_up(){

		this.#socket.on('disconnect',() =>{
			//try to resolve the acess token
			access_token_promise=prepare_access();
			//If the resolution was successful -> reconnect using the new token.
			access_token_promise.then((token)=>{
				this.token=token;
				//Change the Authorization headers, injecting a new access token
				this.#socket.io.opts["extraHeaders"]["Authorization"]=`Bearer ${token.raw}`;
				this.#socket.connect();
			});
		});

		//chat activity - is the event meant to notify about any action such as : a new message has been added\removed or a new chat created\removed.
		this.#socket.on('chat_activity',(data)=>{
			//data:{id:int,name:str}
			//remove the prepend the chat
			let chat_list,list_body;
			//make sure that the chat list and the list body exists.
			if ( (chat_list = document.querySelector('#chats_list')) && (list_body=chat_list.querySelector('.list_body')) ) {
				//update the chat list by removing the "stale" block and prepending the "fresh" one
				let stale_chat = list_body.querySelector(`#source_block,[data-chat_id=${data.id}]`);
				if (stale_chat) list_body.removeChild(stale_chat);

				let fresh_chat = source_block('chat',data);
				list_body.prepend(chat_block);
			}
			
		});

		this.#socket.on('established_chat',(data)=>{
			//data:{id:int,name:str}
			let chat_list,list_body;
			//make sure that the chat list and the list body exists.
			if ( (chat_list = document.querySelector('#chats_list')) && (list_body=chat_list.querySelector('.list_body')) ) {
				//update the chat list by prepending the newly established chat
				let established_block = source_block('chat',data);
				list_body.prepend(established_block);
			}
		});

		this.#socket.on('discharged_chat',(data)=>{
			//data:{id:int,name:str}
			//The chat was discharged - is up for the removal
			let chat_list,list_body;
			//make sure that the chat list and the list body exists.
			if ( (chat_list = document.querySelector('#chats_list')) && (list_body=chat_list.querySelector('.list_body')) ) {
				//update the chat list by removing the "stale" block and prepending the "fresh" one
				let discharged_chat = list_body.querySelector(`#source_block,[data-chat_id=${data.id}]`);

				if (discharged_chat) list_body.removeChild(discharged_chat);
			}
		});

		this.#socket.on('error',(data)=>{
			document.querySelector('.notification_layout').innerHTML=data.message;
		})
	}

	establish_a_chat(data){
		//data: {participant_id:<Number>,<name>:<str>}
		let payload = {name:data.name};
		
		let identification;
		
		if (identification=Number(data.participant_id)) payload.participant_id=identification;

		this.#socket.emit('establish_a_chat', payload);
	}
}