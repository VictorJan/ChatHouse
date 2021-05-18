async function prepare_access() {
	//once the page is loaded - get the access token from the api
	let access_response = await access_call();
	if (access_response.status==200){
		let access_json = await access_response.json();
		return new Token(access_json.access_token);
	}
	else{
		//the has expired -> try to logout
		await logout();
	}
}