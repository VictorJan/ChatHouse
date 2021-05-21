let selected=[];

async function select_message_controller(e){
	let message = (e.target.dataset.message_id) ? e.target : e.target.parentNode;
	if (message.dataset.message_id)
	{
		if ( (index=selected.indexOf(message_id = Number(message.dataset.message_id))) != -1){
			selected.splice(index,1);
			message.classList.remove("selected");
		}
		else{
			selected.push(message_id);
			message.classList.add("selected");
		}
		
		if (selected.length==0){

		}
		else{
			document.querySelector("")
		}
	}
}

function build_chat_bottom(template){

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

async function prepare_chats(token){

	let response = await chats_call(token);
	if (response.status==200){
		let json_response = await response.json();
	}
	else{
		access_token_promise = prepare_access();
		token = await access_token_promise;
		if ((response = await chats_call(token.raw) ).status == 200 ) json_response = await response.json(); else logout(); 
	}
	list('chat',json_response.data);
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