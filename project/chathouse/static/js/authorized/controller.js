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

		select('participant',participant,dataset_storage);
	}
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
	//send GET to the /chat/<identification>/public-keys => thus getting the
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