class User{
	//store the dhInstance, the accessTokenInstance
	#dhInstance;
	#accessTokenInstance;
	constructor(dhInstance){
		return (async() => {
			this.#dhInstance=(dhInstance instanceof DH_Key) ? dhInstance : null;
			if (this.#dhInstance){
				//Set up the accessTokenInstance - by preparing the accessToken.
				this.#accessTokenInstance = await this.#prepare_access();
				return this;
			}
			else{
				throw "Invalida dhInstance argument."
			}
		})();
	}
	
	async #prepare_access(){
		//Get the access token from the resource : /api/tokens/access
		let response = await access_call();
		if (response.status==200){
			let response_json = await response.json();
			return new Token(response_json.access_token);
		}
		else{
			//the has expired -> try to logout
			await this.logout();
		}
	}

	async logout(){
		let url = `${window.location.origin}/logout`;
		fetch(url,{
			method:'GET',
			credentials: 'same-origin'
		})
		.then((response)=>{
			//remove the keyring from the localStorage
			localStorage.removeItem('keyring');
			window.location.replace(response.url);
		});
	}


	async prepare_participations(){
		//Await for the response from the initiated GET Request to the REST at /api/users/<identification>/participations
		let response = await user_call(this.#accessTokenInstance.raw,this.#accessTokenInstance.payload.user_id,'participations');
		let json_response;
		
		//If the request has been successful - set the json of the response.
		if (response.status==200){
			json_response = await response.json();
		}
		else{
			//If the request hasn't been successful - the accessToken could have expired, so one shall get the one
			this.#accessTokenInstance = await this.#prepare_access();
			//Resend the request - if the response is still not a 200 , then logout. Otherwise store the json from the response and proceed to build the list.
			if ((response = await user_call(this.#accessTokenInstance.raw,this.#accessTokenInstance.payload.user_id,'participations')).status == 200 ) json_response = await response.json(); else this.logout(); 
		}

		//Build the list of participations
		list('chat',json_response.data.participations,document.querySelector('.left_layout'));
	}

	async refresh_access(){
		this.#accessTokenInstance = await this.#prepare_access();
		return this.#accessTokenInstance;
	}

	async request_confirmation(action){
		//Call the confirmation endpoint and if successful, notify the user about the update of the activity state -> request to logout after 3 seconds.
		let body={'action':action};
		let response = await confirmation_call(this.#accessTokenInstance.raw,body);
		if (response.status == 401) {
			//refresh the access token and try again
			this.#accessTokenInstance = await this.#prepare_access();
			if ((response =  await confirmation_call(this.#accessTokenInstance.raw,body)).status == 401 ) this.logout(); 
		}

		if (response.status == 201){
			notification(`The request to ${ (action=='put')?'reset the password':'terminate the account'} has been sent. Please check your inbox to proceed with the confirmation. You will be logged out in a few seconds.`)
			new Promise( resolve=> setTimeout(resolve,5000)).then(()=>{ this.logout() })
		}
		else if (response.status == 401) this.logout(); else notification('The request contained invalid payload, please try again.');
	}
	
	get accessTokenInstance(){
		return this.#accessTokenInstance;
	}

	get dhInstance(){
		return this.#dhInstance;
	}
	
}
