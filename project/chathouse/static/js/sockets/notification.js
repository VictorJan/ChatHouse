class NotificationSocket{
	#socket;
	#token;
	constructor(token){
	this.#token = token;
	this.#socket = io(`${window.origin}/socket/notification`,{ extraHeaders:{Authorization:`Bearer ${token.raw}`}, multiplex:false});
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

		//chat activity - is the event meant to notify about any action such as : a new message has been added\removed or a new chat created\removed.
		this.#socket.on('chat_activity',(data)=>{
			//data:{id:int,name:str}
			//remove the prepend the chat
			let chat_list,list_body;
			//make sure that the chat list and the list body exists.
			if ( (chat_list = document.querySelector('#chats_list')) && (list_body=chat_list.querySelector('.list_body')) ) {
				//update the chat list by removing the "stale" block and prepending the "fresh" one
				let stale_chat = list_body.querySelector(`#source_block,[data-chat_id='${data.id}']`);
				if (stale_chat) list_body.removeChild(stale_chat);

				let fresh_chat = source_block('chat',data);
				list_body.prepend(fresh_chat);

				//Add and remove ,after 250 ms, an activity class to the block - for the visual appeal
				list_body.firstElementChild.classList.add("activity");
				new Promise( resolve=> setTimeout(resolve,250)).then(()=>{ list_body.firstElementChild.classList.remove("activity"); })
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

				//Add and remove ,after 250 ms, an activity class to the block - for the visual appeal
				list_body.firstElementChild.classList.add("activity");
				new Promise( resolve=> setTimeout(resolve,250)).then(()=>{ list_body.firstElementChild.classList.remove("activity"); })
			}
		});

		this.#socket.on('discharged_chat',(data)=>{
			//data:{id:int,name:str}
			//The chat was discharged - is up for the removal
			let chat_list,list_body;
			//make sure that the chat list and the list body exists.
			if ( (chat_list = document.querySelector('#chats_list')) && (list_body=chat_list.querySelector('.list_body')) ) {
				//update the chat list by removing the "stale" block and prepending the "fresh" one
				let discharged_chat = list_body.querySelector(`#source_block,[data-chat_id='${data.id}']`);

				if (discharged_chat) list_body.removeChild(discharged_chat);

				//If the recipeint is currently on the page - refresh the page
				if (chat_id && chat_id==data.id) window.location.replace(window.location.href); 
			}
		});

		this.#socket.on('error',(data)=>{
			notification(data.message);
		})
	}

	establish_a_chat(data){
		//data: {participant_id:<Number>,<name>:<str>}
		let payload = {name:data.name};
		
		let identification;
		
		if (identification=Number(data.participant_id)) payload.participant_id=identification;

		this.#socket.emit('establish_a_chat', payload);
	}

	discharge_a_chat(data){
		//data: {participant_id:<Number>,<name>:<str>}
		let identification;
		if ((identification=Number(data.id))) this.#socket.emit('discharge_a_chat', {id:identification});
	}
}