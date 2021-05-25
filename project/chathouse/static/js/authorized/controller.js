async function select_message_controller(e){
	let message = (e.target.dataset.message_id) ? e.target : e.target.parentNode;
	if (message.dataset.message_id)
	{
		if (!document.querySelector("#delete_message_button")) chat_utilities('active');

		let dataset_storage = document.querySelector("#delete_message_button");

		select('message',message,dataset_storage);
	}
}

async function select_participant_controller(e){
	let participant = (e.target.dataset.participant_id) ? e.target : null;
	if ((participant) && (participant.dataset.participant_id))
	{
		let dataset_storage = document.querySelector("#establish_chat_button");

		let username = select('participant',participant,dataset_storage);
		if (username) document.querySelector("#search_field[data-type='participant']").value=username;
	}
}

async function cancel_delete_controller(e){
	let utilities = e.target.parentNode;
	let delete_button;
	if (delete_button=utilities.querySelector('#delete_message_button')){
		//remove from all selected messages - the selected class
		console.log(delete_button.dataset.message_id)
		delete_button.dataset.message_id.split(',').forEach((message_id)=>{
			document.querySelector(`#message[data-message_id='${message_id}']`).classList.remove("selected");
		})
		delete_button.dataset.message_id='';
		//set the utilities to idle
		chat_utilities('idle');
	}
}

//CHAT
//Establish a chat
async function establish_chat_controller(e){
	let input_field = document.querySelector('#chat_name');
	if ((input_field) && (input_field.value!='')){
		let payload = {participant_id:e.target.dataset.participant_id, name: input_field.value}
		notification_socket.establish_a_chat(payload);
	}

}
//Discharge a chat
async function discharge_chat_controller(e){
	let chat_id;
	if ((chat_id=Number(e.target.dataset.chat_id))) notification_socket.discharge_a_chat({id:chat_id});
	//close the card:
	let close_button;
	if (close_button=document.querySelector("#close_button")){
		let close_event = new Event('click');
		close_button.dispatchEvent(close_event);
		close_card(close_event);
	}
}



//close_notification_button
function close_notification_controller(e){
	let block;
	if (block=e.target.parentNode) block.parentNode.removeChild(block);
}




async function head_controller(e){
	let chat;
	if (chat=e.target.dataset.chat_id) window.location.replace(`${window.origin}/chat?id=${chat}`);
}


async function get_logout(){
	const url = `${window.location.origin}/logout`;
	const response = await fetch(url,{
		method:'GET',
		credentials: 'same-origin'
	});
	return response;
}

async function logout(){
	let logout_response = await get_logout();
	window.location.replace(logout_response.url);
}

async function prepare_access() {
	//once the page is loaded - get the access token from the api
	let access_response = await access_call();
	if (access_response.status==200){
		let access_json = await access_response.json();
		return new Token(access_json.access_token);
	}
	else{
		//the has expired -> try to logout
		await logout();
	}
}

async function prepare_participations(token,identification){

	let response = await user_call(token,identification,'participations');
	let json_response;
	if (response.status==200){
		json_response = await response.json();
	}
	else{
		access_token_promise = prepare_access();
		token = await access_token_promise;
		if ((response = await user_call(token,identification,'participations')).status == 200 ) json_response = await response.json(); else logout(); 
	}
	list('chat',json_response.data.participations,document.querySelector('.left_layout'));
}

async function get_promised(promise){
	return await promise.then((promised)=>{
		return promised
	});
}

async function prepare_other_public_key(token_object,identification){
	//if the client has loaded in a page with a chat:
	//send GET to the /chat/<identification>/public-keys => thus getting the participants public key
	let public_keys_response = await chat_call(token_object.raw,identification,'public-keys');
	if (public_keys_response.status==200){
		let public_keys_json = await public_keys_response.json();
		//filter through the poublic keys and store the one , which is not yours;
		return public_keys_json.data.participants.filter(user=>user.id!=token_object.payload.user_id);
	}
	else{
		//reload
		window.location.replace(window.location.href);
	}

}

async function prepare_messages(token_object,identification){
	//Send the GET request to the API to get the last few messages
	let response = await chat_call(token_object.raw,identification,'messages?amount=asdsa');
	if (response.status==200){
		let json_response = await response.json();
		console.log(json_response);
	}
}


async function decrypt(content){
	await cipher.decrypt(content);
}

//have a chat class with decrypt encrypt methods and inner private fields : for the cipher_key and chat id , that's only readable constructor initializes with the 
//have a user class to logout or prepare the tokens?