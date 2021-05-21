async function user_call(token,identification){

	const url = `${window.location.origin}/api/users/${identification}`;
	
	let credentials_field = 'omit';

	let headers_field = new Headers({'Authorization':`Bearer ${token}`})
	
	const response = await fetch(url,{
		method:'GET',
		credentials: credentials_field,
		headers: headers_field
	});
	return response;
}

async function users_call(token,query){

	let query_list=[];
	
	Object.keys(query).forEach((key)=>{
		query_list.push(`${key}=${query[key]}`);
	})

	const url = `${window.location.origin}/api/users?${query_list.join('&')}`;
	
	let credentials_field = 'omit';

	let headers_field = new Headers({'Authorization':`Bearer ${token}`})
	
	const response = await fetch(url,{
		method:'GET',
		credentials: credentials_field,
		headers: headers_field
	});
	return response;
}