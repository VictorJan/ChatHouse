async function search_list_controller(e){
	if ((identification=e.target.value)!=""){

		let token = await access_token_promise;
		let query = {'identification':identification}

		if ((response = await users_call(token.raw,query) ).status == 200 ){
				json_response = await response.json();
			}
		else{
			//The access token has expired/invalid -> refresh it and reasign
			access_token_promise = prepare_access();
			token = await access_token_promise;
			if ((response = await user_call(token.raw,identification.user) ).status == 200 ) json_response = await response.json(); else logout(); 
		}
		list('user',json_response.data);
	}
}