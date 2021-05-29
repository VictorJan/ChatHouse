if (!localStorage.getItem('keyring')) window.location.replace(`${window.origin}/logout`);
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
		notification_socket = new NotificationSocket(userInstance.accessTokenInstance);

		//If the page contains a chat, perform the following steps
		if (chat_id){
			//intialize the chatInstance
			(new Chat(chat_id,userInstance)).then((cInstance)=>{
				chatInstance = cInstance;
				//set up the chat socket
				chat_socket = new ChatSocket(userInstance.accessTokenInstance,chat_id);
				//Set the utilities to the idle state.
				chat_utilities('idle');
				//create an observer
				create_observer();
			});
		}
	});
});