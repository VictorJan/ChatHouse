async function source_card_controller(e){
	//Verify if there is a access_token_promise and the target contains a dataset
	if ( (typeof userInstance !== "undefined") && ((dataset=e.target.dataset)) ) {
		//Get the identification from dataset: if there is a user_id return an object of {user_id:<value>} otherwise return the {chat_id:<value>}, if in both cases the values are none - following steps will be ignored
		let identification = (dataset.user_id) ? {'user':dataset.user_id} : {'chat':dataset.chat_id};
		
		let token = userInstance.accessTokenInstance;
		let response,json_response;
		//Branch to different api routes
		if (identification.user){
			//call the users/<identification> api
			if ((response = await user_call(token.raw,identification.user) ).status == 200 ){
				json_response = await response.json();
			}
			else{
				//The access token has expired/invalid -> refresh it and reasign
				token = await userInstance.refresh_access();
				if ((response = await user_call(token.raw,identification.user) ).status == 200 ) json_response = await response.json(); else logout(); 
			}
			
			let data = {information:json_response.data,current_user: token.payload.user_id==json_response.data.id}

			user_card(data);

		}
		else if (identification.chat){
			//call the chats/<identification>
			if ((response = await chat_call(token.raw,identification.chat) ).status == 200 ){
				json_response = await response.json();
			}
			else{
				//The access token has expired/invalid -> refresh it and reasign
				token = await userInstance.refresh_access();
				
				//In either way prepare the json response, then depending on the status code perform next steps
				response = await user_call(token.raw,identification.user);
				json_response = await response.json();
				//If the status code isn't 200 - then the access_token is invalid or the access to the resource is not permitted
				//So if the access is denied - refresh the page. Otherwise - perform a logout() ,as the token has expired/simply invalid.
				if (response.status!=200){
					if (json_response.reason=='Access has been denied.') window.location.replace(window.location.href);
					logout(); 
				} 
			}
			
			let data = {information:json_response.data}

			chat_card(data);
		}
	}
}


async function account_card_controller(e){
		account_card();
}

async function new_chat_card_controller(e){
		new_chat_card();
}
