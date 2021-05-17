async function key_parameters_call(token){
	const url = `${window.location.origin}/api/key-parameters`;
	
	const response = await fetch(url,{
		method:'GET',
		credentials: 'omit',
		headers: new Headers({
			'Authorization':`Bearer ${token}`
		})
	});
	return response;
}