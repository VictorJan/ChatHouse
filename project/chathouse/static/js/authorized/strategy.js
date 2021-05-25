if (!localStorage.getItem('keyring')) logout();
const dh_keyring_promise = (async()=>{
	return await new DH_Key( JSON.parse(localStorage.getItem('keyring')) );
})();

//set up an instance of the Chat class - to perform the preparation of the messages,
//userInstance 

const chat_id = Number(new URL(window.location.href).searchParams.get('id'));

let chatInstance;
let userInstance;

let notification_socket;
let chat_socket;

dh_keyring_promise.then((dhInstance)=>{

	//intialize the userInstance
	(new User(dhInstance)).then((uInstance)=>{
		userInstance=uInstance;
		//At this point the UserInstance contains the accessTokenInstance;
		userInstance.prepare_participations();
		//Set up the notification socket
		//notification_socket = new NotificationSocket(tokenInstance);

		//If the page contains a chat, perform next steps
		if (chat_id){
			//intialize the chatInstance
			(new Chat(chat_id,userInstance)).then((cInstance)=>{
				chatInstance=cInstance;
				chat_socket = new ChatSocket(userInstance.accessTokenInstance,chat_id);
				chat_utilities('idle');
			});
		}
	});
});

/*

let cipher_key;
let cipher;

//Set up:
access_token_promise.then((tokenInstance)=>{
	
	//Set up the notification socket
	notification_socket = new NotificationSocket(tokenInstance);

	//Prepare current chats - participations on the left side
	userInstance.prepare_participantions();
	
	//If the page consists of a chat, perform next steps
	if (chat_id){
		//Build idle chat utilities
		chat_utilities('idle');
		//Set up the chat socket, which would perfrom the logout/dis
		chat_socket = new ChatSocket(token_object,chat_id);
		//Await to get the promised Diffie Hellman keyring - start the initialization of the Chat instance
		dh_keyring_promise.then((promised_dh)=>{
			chatInstance = new Chat(chat_id,token_object,)
		})
		//Get the messages and decrypt them:
		prepare_messages(token_object,chat_id);
	}
});


/*
get_promised(dh_keyring_promise).then((promised_dh)=>{
			//Then await to retreive keyrings of others/other participants
			prepare_other_public_key(token_object,chat_id).then((others)=>{
				//Having received a list of other participants with their keyrings -> set a common secret if there is another pariticipant, otherwise set the secret to yours private key.
				let secret = (others.length!=0) ? promised_dh.establish(others[0].keyring.public_key) : promised_dh.keyring.private;
				//Having established the common secret - await the promised Cipher Key to get the CryptoKey for the encryption and decryption.
				get_promised(new CipherKey(secret)).then((promised_cipher_key)=>{
					cipher_key=promised_cipher_key.value;
					cipher = new AES_CBC(cipher_key);
				})
			})
		});

*/