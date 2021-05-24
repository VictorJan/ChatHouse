async function source_card_controller(e){
	//Verify if there is a access_token_promise and the target contains a dataset
	if ( (typeof access_token_promise !== "undefined") && ((dataset=e.target.dataset)) ) {
		//Get the identification from dataset: if there is a user_id return an object of {user_id:<value>} otherwise return the {chat_id:<value>}, if in both cases the values are none - following steps will be ignored
		let identification = (dataset.user_id) ? {'user':dataset.user_id} : {'chat':dataset.chat_id};
		
		let token = await access_token_promise;
		//Branch to different api routes
		if (identification.user){
			//call the users/<identification> api
			let json_response;
			if ((response = await user_call(token.raw,identification.user) ).status == 200 ){
				json_response = await response.json();
			}
			else{
				//The access token has expired/invalid -> refresh it and reasign
				access_token_promise = prepare_access();
				token = await access_token_promise;
				if ((response = await user_call(token.raw,identification.user) ).status == 200 ) json_response = await response.json(); else logout(); 
			}
			
			let data = {information:json_response.data,current_user: token.payload.user_id==json_response.data.id}

			user_card(data);

		}
		else if (identification.chat){
			//call the chats/<identification>
			let json_response;
			if ((response = await chat_call(token.raw,identification.chat) ).status == 200 ){
				json_response = await response.json();
			}
			else{
				//The access token has expired/invalid -> refresh it and reasign
				access_token_promise = prepare_access();
				token = await access_token_promise;
				if ((response = await chat_call(token.raw,identification.chat) ).status == 200 ) json_response = await response.json(); else logout(); 
			}
			
			let data = {information:json_response.data}

			chat_card(data);
		}
	}
}


async function account_card_controller(e){
	//Verify if there is a access_token_promise
	if (typeof access_token_promise !== "undefined") {
		
		let token = await access_token_promise;
		account_card();
	}
}

async function new_chat_card_controller(e){
	//Verify if there is a access_token_promise
	if (typeof access_token_promise !== "undefined") {
		
		let token = await access_token_promise;
		new_chat_card();
	}
}
