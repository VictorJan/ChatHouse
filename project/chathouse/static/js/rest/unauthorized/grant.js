async function grant_call(data,token){
	const url = `${window.location.origin}/api/tokens/grant`;
	const response = await fetch(url,{
		method:'POST',
		credentials:'omit',
		headers: new Headers({
			'Content-type':'application/json',
			'Authorization':`Bearer ${token}`
		}),
		body:JSON.stringify(data)
	});
	return response;
}