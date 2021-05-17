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
				//Exports the keyring bundle, encrypting the private key with the password , if the initial route is signup
				data['keyring'] = await dh_key.export(clear_password);
			}


			let verification_response = await grant_call(data,verification_token.raw);
			if (verification_response.status == 201){
				let verification_json = await verification_response.json();
				
				const grant_token = new Token(verification_json.grant_token);

				//If the initial route is login -> based on the retreived keyring - create an instance of a new DH_key. Declare a dh_key
				if (preaccess_token.payload.route == "login"){

					let login_keyring=verification_json.keyring;
					login_keyring['raw']['password']=clear_password;

					dh_key = await new DH_Key(login_keyring);
				}
				//stores current key ring in the session storate
				dh_key.store();

				//call the authorized route to set the grant token as the cookie.

				let view_call_response = await authorized_view_call(grant_token.raw);
				if (view_call_response.status==200){
					window.location.replace(`${window.location.origin}/chat`);
				}

			}
			else{
				document.querySelector(".feedback").innerHTML="Please enter valid data."
			}
		}
	}

async function generate_a_keyring(){

	let response = await key_parameters_call(verification_token.raw);
	if (response.status==200){
		let data = await response.json();
		delete data.success;
		data['payload']={private:random(2,data.m)};
		const keyring = await new DH_Key(data);
		return keyring;
	}
	return null;
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