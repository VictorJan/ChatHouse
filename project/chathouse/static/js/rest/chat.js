async function chat_call(token,identification,endpoint=null){

	const url = `${window.location.origin}/api/chats/${identification}${ (endpoint) ? ("/"+endpoint) : "" }`;
	
	let credentials_field = 'omit';

	let headers_field = new Headers({'Authorization':`Bearer ${token}`})
	
	const response = await fetch(url,{
		method:'GET',
		credentials: credentials_field,
		headers: headers_field
	});
	return response;
}

async function chats_call(token){

	const url = `${window.location.origin}/api/chats`;
	
	let credentials_field = 'omit';

	let headers_field = new Headers({'Authorization':`Bearer ${token}`})
	
	const response = await fetch(url,{
		method:'GET',
		credentials: credentials_field,
		headers: headers_field
	});
	return response;
}