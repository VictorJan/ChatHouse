async function user_card_controller(e){
	if ( (typeof access_token !== "undefined") && (typeof e.target.innerHTML !== "undefined") && (e.target.innerHTML!=="") ) {
		//get_user_data(access_token,e.target.innerHTML)
		build_a_card('user',{information:{username:'username1',email:'username@gmail.com',name:'name',about:'about me.'}})
	}
}

async function ko_chat_card_controller(e){
	if ( (typeof access_token !== "undefined") && (e.target.parentNode.parentNode.querySelector('#user') !== null) ) {
		//get_user_data(access_token,e.target.innerHTML)
		build_a_card('chat',{information:{username:e.target.parentNode.parentNode.querySelector('#user').innerHTML}})
	}
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