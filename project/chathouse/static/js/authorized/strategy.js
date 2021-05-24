if (!localStorage.getItem('keyring')) logout();
const dh_keyring_promise = (async()=>{
	return await new DH_Key( JSON.parse(localStorage.getItem('keyring')) );
})();

let access_token_promise=prepare_access();
const chat_id = Number(new URL(window.location.href).searchParams.get('id'));

let notification_socket;
let chat_socket;

let cipher_key;
let cipher;

//Set up:
access_token_promise.then((token_object)=>{
	
	//Set up the notification socket
	notification_socket = new NotificationSocket(token_object);

	//Prepare current chats - particioations on the left side
	prepare_participations(token_object.raw,token_object.payload.user_id)
	
	//If the page consists of a chat, perform next steps
	if (chat_id){
		//Build idle chat utilities
		chat_utilities('idle');
		//Set up the chat socket, which would perfrom the logout/dis
		chat_socket = new ChatSocket(token_object,chat_id);
		//Await to get the promised Diffie Hellman keyring
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
		//Get the messages and decrypt them:
		prepare_messages(token_object,chat_id);
	}
});
