async function confirmation_controller(e){
		/*call requires either:
		PUT:{password:{current:str,new:str},private_key:{iv:str,data:str}}
		DELETE:{password:str}
		*/
		let data={};
		e.target.parentNode.querySelectorAll('#password,#current_password,#new_password').forEach(el=>{
			if (el.value!="") data[el.id]=el.value;
		});
		
		let action;
		if (Object.keys(data).length == (( (action=confirmation_token.payload.action) =='put')?2:1)){

			//store the clear password
			let clear = {'current':data['current_password']};
			if (action=='put') clear.new = data['new_password'];

			//sha256 hash the password|s
			for (const key of Object.keys(data)){
				data[key] = (await new Digest(data[key])).hex;
			}

			if (action == "put"){
				//Retreive the private key and establish a dH
				//Call the users/<id> endpoint -> retreive the keyring information, if the token has expired , thus the clien shall receive a 401 -> refresh the page.
				let keyring_response;
				let keyring_json;
				//If the request has been usuccessful -> then the confirmation token is invalid/no longer valid due to activity state.
				if ((keyring_response = await user_call(confirmation_token.raw,confirmation_token.payload.user_id,endpoint='keyring')).status==200) keyring_json=await keyring_response.json(); else window.location.replace(window.location.href);
				//Establish dh payload with a raw private encrypted key, which is going to be injected with a current password -> to then encrypt the revealed private key with a new password. Then the reencrypted private key shall be exported.
				//Set up the g and m
				let dh_payload = keyring_json.data.parameters;
				//Set up the raw payload , including the encrypted private key and the current password -> to resolve the clear private key
				dh_payload.raw = {
					private_key:keyring_json.data.keyring.private_key,
					password:clear['current']
				};
				//Await for an instance of the DH_Key
				let dh_key = await new DH_Key(dh_payload);
				//if a private key couldn't be resolved ~ the password was invalid , thus the Number value of the private key, couldn't be established.
				if (!dh_key.keyring.private) {
					document.querySelector(".feedback").innerHTML='Password seems to be invalid.'; 
					data=null;
				}
				else{
					//Exports the private key, encrypting the private key with the new password. Also reset the payload
					data={'reset':{
							'password':{
								'current':data['current_password'],
								'new':data['new_password']
							}
						}
					}
					data['reset']['private_key'] = (await dh_key.export(clear['new'])).private_key;
				}

			}
			//If there is still data
			if (data){
				//At this point for both routes , user rest call could be executed , based on the action and having provided confirmation token, the user identification - requester's id and the soon-to be JSON data.
				let confirmation_response = await user_call(confirmation_token.raw,confirmation_token.payload.user_id,null,action.toUpperCase(),data);
				let confirmation_json = await confirmation_response.json();

				if (confirmation_response.status==200 || confirmation_json.reason!="Invalid confirmation token."){
					//If the requets has been successful or the provided payload was invalid\authentication data was not valid - gives a chance to enter again, untill the confirmation token is invalid. 
					document.querySelector(".feedback").innerHTML=confirmation_json.message;
				}
				else{
					//Otherwise - the status code is 401 - invalid confirmation token ~> refresh the page.
					window.location.replace(window.location.href);
				}
			}
		}
	}