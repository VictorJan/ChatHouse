async function user_call(token,identification,endpoint=null,method='GET',data=null){

	const url = `${window.location.origin}/api/users/${identification}${(endpoint)?"/"+endpoint:""}`;
	
	let credentials_field = 'omit';

	let headers_payload={'Authorization':`Bearer ${token}`};
	if (method!="GET") headers_payload['Content-type']='application/json';
	
	let headers_field = new Headers(headers_payload)
	
	let request_payload = {
		method:method,
		credentials: credentials_field,
		headers: headers_field,
	};
	
	if (data && method!='GET') request_payload.body=JSON.stringify(data);

	const response = await fetch(url,request_payload);
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