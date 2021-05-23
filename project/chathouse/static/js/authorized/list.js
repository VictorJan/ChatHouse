async function search_list_controller(e){
	if ((identification=e.target.value)!="" && (e.target.dataset.type)){
		
		if (!e.target.parentNode.querySelector("#clear_search_button")) clear_search_button(e.target.parentNode);
		
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
		list(e.target.dataset.type,json_response.data,e.target.parentNode.parentNode);
	}
	else{
		clear_search(e.target.parentNode.parentNode);
		if (e.target.dataset.type=='user'){
			let token=await access_token_promise;
			prepare_participations(token.raw,token.payload.user_id);
		}
	}
}

async function clear_search_controller(e){
	let field = e.target.parentNode.querySelector("#search_field");
	clear_search(e.target.parentNode.parentNode);
	if (field.dataset.type=='user'){
		let token=await access_token_promise;
		prepare_participations(token.raw,token.payload.user_id);
	}
}

function clear_search (parent) {
	let current_list,clear_button;
	if (current_list=parent.querySelector(".list")) parent.removeChild(current_list);
	if (clear_button=parent.querySelector("#clear_search_button")) parent.firstElementChild.removeChild(clear_button);
	parent.querySelector("#search_field").value="";
}