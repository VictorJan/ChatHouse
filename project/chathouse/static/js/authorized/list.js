async function search_list_controller(e){

	if ((identification=e.target.value)!=""){
		
		if (!e.target.parentNode.querySelector("#clear_search_button")) clear_search_button();
		
		let query = {'identification':identification}

		let token = await access_token_promise;

		if ((response = await users_call(token.raw,query) ).status == 200 ){
				json_response = await response.json();
			}
		else{
			//The access token has expired/invalid -> refresh it and reasign
			access_token_promise = prepare_access();
			token = await access_token_promise;
			if ((response = await user_call(token.raw,identification.user) ).status == 200 ) json_response = await response.json(); else logout(); 
		}
		list('user',json_response.data,e.target.parentNode.parentNode);
	}
	else{

		await clear_search();
	}
}


async function clear_search () {
	
	if ((clear_button=document.querySelector("#clear_search_button"))) (search_block=clear_button.parentNode).removeChild(clear_button);
	search_block.querySelector("#search_field").value="";
	let token = await access_token_promise;
	prepare_participations(token.raw,token.payload.user_id);

}