class Chat{
	//fields: id:<chat identificaiton>, <>
	#id;
	#userInstance;
	#cipherInstance;
	#last_timestamp;
	#invalid;

	constructor(id,userInstance){
		//id - chat identification
		//userInstance - an instance of the User class - meant to store the user data: accessTokenInstance,dhInstance.
		//Goal: establish an inner instance of a AES_CBC Class as a cipherInstance  
		return (async() => {
			//First make sure of the types
			this.#id=id;
			//Set up a variable to store current incorrectly encrypted/stored messages
			this.#invalid=[]
			//set the last dnt/timestamp for the message prep
			this.#last_timestamp=(Date.now()/100).toFixed()

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

	async prepare_messages(sentinel){
		if (this.#last_timestamp!=null){
			//send the GET request to the /api/chats/<id>/messages?&amount=10&dnt=<last_timestamp>
			//set up the query parameters
			let amount = 10;
			let query = `amount=${amount}&dnt=${this.#last_timestamp}`;
			let endpoint = 'messages';
			//intialize the chat call
			let response = await chat_call(this.#userInstance.accessTokenInstance.raw,this.#id,`${endpoint}?${query}`);
			let json_response;
			//If the status is 200, then await the json
			if (response.status == 200){
				json_response = await response.json()
			}
			else{
				//Othewise refresh the access token and try the request again.
				//This would log the user out if the grant token has expired or is invalid.
				await this.#userInstance.refresh_access();
				//Send the request again
				response = await chat_call(this.#userInstance.accessTokenInstance.raw,this.#id,`${endpoint}?${query}`);
				//If the response is still not equal to 200 -> then the accessToken is not valid/denied -> log the user out.
				if (response.status != 200) this.#userInstance.logout();
				//Otherwise store the json_response
				json_response = await response.json();
			}
			//Having received the json data of the response -> extract all of the messages from the "messages" key.
			//Then for each of them "receive" the clear text -> decrypting the content, and build the message.
			//Moreover, make sure to store the last timestamp in the last_timestamp variable.
			//However if the amount of the messages are lesser than the requested amount, set the last_timestamp to a null -> thus the client would call the api only if there are still messages to fetch.
			let messages = json_response.data.messages;
			
			let sentinel_clone = sentinel.cloneNode(true);

			let chat_content = sentinel.parentNode;

			for (const message_object of messages){
				let decrypted;
				if (decrypted = await this.receive(message_object.content)){
					//set the message payload
					let message_payload = {id:message_object.id,sender:message_object.sender,content:decrypted,dnt:message_object.dnt.readable};
					//proceed to build the message block , prepending it.
					message(message_payload,false);
				}
				else{
					//notify the user about the integrity alert.
					//Store the invalid messages.
					this.#invalid.push(message_object.id)
				}
			}
			//If the amount of the messages is less than the requested amount, set the last timestamp to a null , otherwise extract the timestamp of the last message in the list.
			this.#last_timestamp = (messages.length<amount) ? null : messages[messages.length-1].dnt.timestamp;
			if(this.#invalid.length!=0) notification("Some messages couldn't be decrypted, due to invalid payload. These messages won't be displayed - do you wish to clear them?",true)
 		}
	}

	send(message){
		//message:str
		//Encrypts the message with the cipherInstance
		try{
			let payload = {};
			this.#cipherInstance.encrypt(message).then((encrypted)=>{
				payload.content=encrypted;
				chat_socket.establish_a_message(payload);
			});
		}
		catch{
			notification('Please submit proper data.');
		}

		//calls the emit call to the socket
	}

	async receive(message){
		/*message:{iv:str,data:str}*/
		try{
			//Decrypt the message with the common secret CryptoKey, set up in the AES_CBC cipherInstance 
			return await this.#cipherInstance.decrypt(message);
		}
		catch{
			//Otherwise set the notification and return null
			notification("Couldn't decrypt the message, due to the invalid payload.")
			return await null;
		}

	}

	remove(messages){
		if (messages instanceof Array){
			chat_socket.discharge_messages({messages:messages})
		}
	}

	sanitize(){
		//sanitizes/clears the chat from the messages with invalid payloads
		//call remove 
		if (this.#invalid && this.#invalid.length>0) this.remove(this.#invalid);
		this.#invalid=null;
	}

}