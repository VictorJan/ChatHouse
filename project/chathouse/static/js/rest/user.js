async function get_user_data(access_token,identification){
	let url = `${window.location.origin}/api/users/${identification}`;
	const response = await fetch(url,{
		method:'GET',
		credentials:'omit',
		headers:{
			'Authorization':`Bearer ${access_token}`
		}
	})
	return response;
}