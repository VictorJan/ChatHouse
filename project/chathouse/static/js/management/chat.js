class Chat{
	//fields: id:<chat identificaiton>, <>
	#id;
	#userInstance;
	#cipherInstance;

	constructor(id,userInstance){
		//id - chat identification
		//userInstance - an instance of the User class - meant to store the user data: accessTokenInstance,dhInstance.
		//Goal: establish an inner instance of a AES_CBC Class as a cipherInstance  
		return (async() => {
			//First make sure of the types
			this.#id=id;
			this.#userInstance=(userInstance instanceof User) ? userInstance : null;
			if (this.#userInstance){
				//Get the public key of the other participant
				let other = await this.#prepare_other_public_key();
				//If the filtered result has provided another key - establish a common secret , otherwise set one's own private key as the secret
				let secret = (other.length==1) ? this.#userInstance.dhInstance.establish(other[0].keyring.public_key) : this.#userInstance.dhInstance.keyring.private;
				//Having established the common secret - await the promised Cipher Key to get the CryptoKey to establish the cipherInstance.
				(new CipherKey(secret)).then((cipherkeyInstance)=>{
					this.#cipherInstance = new AES_CBC(cipherkeyInstance.value);
				});
			}
			return this;
		})();
	}
	async #prepare_other_public_key(){
		//if the client has loaded in a page with a chat:
		//send GET to the /chat/<identification>/public-keys => thus getting the participants public key
		let public_keys_response = await chat_call(this.#userInstance.accessTokenInstance.raw,this.#id,'public-keys');
		if (public_keys_response.status==200){
			let public_keys_json = await public_keys_response.json();
			//filter through the poublic keys and store the one , which is not yours;
			return public_keys_json.data.participants.filter(user=>user.id!=this.#userInstance.accessTokenInstance.payload.user_id);
		}
		else{
			//reload
			window.location.replace(window.location.href);
		}
	}

	send(message){
		//message:str
		//Encrypts the message with the cipher
		//calls the emit call to the socket
	}

	receive(message){

	}

}