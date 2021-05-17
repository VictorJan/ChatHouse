async function access_call(token=null){
	const url = `${window.location.origin}/api/tokens/access`;
	
	let credentials_field = (token) ? 'omit' : 'include';
	let headers_field = (token) ? new Headers({'Authorization':`Bearer ${token}`}) : new Headers()
	
	const response = await fetch(url,{
		method:'GET',
		credentials: credentials_field,
		headers: headers_field
	});
	return response;
}