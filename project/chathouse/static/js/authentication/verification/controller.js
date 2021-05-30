async function verification_controller(e){
		let data={};
		e.target.parentNode.querySelectorAll('#password').forEach(el=>{
			if (el.value!="") data[el.id]=el.value;
		});
		if (Object.keys(data).length == 1){

			//store the clear password
			const clear_password = data['password'];

			//sha256 hash the password
			data['password'] = (await new Digest(data['password'])).hex;
			let dh_key;

			if (preaccess_token.payload.route == "signup"){
				//Generate a random dh key
				dh_key = await ( await generate_a_keyring() );
				if (!dh_key.keyring.private) window.location.replace(window.location.href);
				//Exports the keyring bundle, encrypting the private key with the password , if the initial route is signup
				data['keyring'] = await dh_key.export(clear_password);
			}



			let grant_response = await grant_call(data,verification_token.raw);
			let grant_json = await grant_response.json();

			if (grant_response.status == 201){
				
				const grant_token = new Token(grant_json.grant_token);

				//If the initial route is login -> based on the retreived keyring - create an instance of a new DH_key. Declare a dh_key
				if (preaccess_token.payload.route == "login"){

					let login_keyring=grant_json.keyring;
					login_keyring['raw']['password']=clear_password;

					dh_key = await new DH_Key(login_keyring);
				}
				
				//stores current keyring in the local storage
				if(dh_key.store()){
					//call the authorized route to set the grant token as the cookie.
					let view_call_response = await authorized_view_call(grant_token.raw);
					window.location.replace(`${window.location.origin}/chat`);
				}
				else{
					document.querySelector(".feedback").innerHTML="Couldn't set up the keyring in the localStorage, please try again."
				}

			}
			else{
				if (grant_response.status == 401){
					if (grant_json.reason=='Invalid verification/preaccess token.'){
						window.location.replace(`${window.location.origin}/start`);
					}
					else if (grant_json.reason=='Invalid authentication data.'){
						document.querySelector(".feedback").innerHTML="The password is invalid."
					}
				}
				else if  (grant_response.status == 409){
					if (grant_json.reason=='Conflict. Please submit again.'){
						document.querySelector(".feedback").innerHTML="Please submit again."
					}
					else{
						window.location.replace(window.location.href);
					}
				}
			}
		}
	}

async function generate_a_keyring(){

	let response = await key_parameters_call(verification_token.raw);
	if (response.status==200){
		let data = await response.json();
		delete data.success;
		data['payload']={private_key:random(2,data.m)};
		const keyring = await new DH_Key(data);
		return keyring;
	}
	window.location.replace(`${window.location.origin}/chat`)
}

async function authorized_view_call(token){
	const url = `${window.location.origin}/chat`;

	let headers_field = new Headers({'Authorization':`Bearer ${token}`})
	
	const response = await fetch(url,{
		method:'GET',
		credentials: 'same-origin',
		headers: headers_field
	});
	return response;
}