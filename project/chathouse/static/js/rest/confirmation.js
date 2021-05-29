async function confirmation_call(token,data){
	const url = `${window.location.origin}/api/tokens/confirmation`;
	
	const response = await fetch(url,{
		method:'POST',
		credentials:'omit',
		headers: new Headers({
			'Authorization':`Bearer ${token}`,
			'Content-type':'application/json'
		}),
		body:JSON.stringify(data)
	});

	return response;
}