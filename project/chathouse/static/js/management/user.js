class User{
	#id;
	#token;
	#dh;
	constructor(id,token,dh){
		this.#id=id;
		this.#token=(token instanceof Token) ? token : null;
		this.#dh=(token instanceof DH_Key) ? dh : null;	
	}

	send(message){
		//calls the emit call to the socket
	}

	#connect
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
