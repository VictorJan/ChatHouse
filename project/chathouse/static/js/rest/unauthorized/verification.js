async function verification_call(data){
	const url = `${window.location.origin}/api/tokens/verification`;
	const response = await fetch(url,{
		method:'POST',
		credentials:'include',
		headers: new Headers({
			'Content-type':'application/json'
		}),
		body:JSON.stringify(data)
	});
	return response;
}