if (!localStorage.getItem('keyring')) logout();
const dh_keyring_promise = (async()=>{
	return await new DH_Key( JSON.parse(localStorage.getItem('keyring')) );
})();

let access_token_promise=prepare_access();
let chat_id = new URL(window.location.href).searchParams.get('id');

let notification_socket;
let chat_socket;

access_token_promise.then((token)=>{
	
	notification_socket = new NotificationSocket(token);
	chat_socket = (chat_id) ? new ChatSocket(token,chat_id) : null;
});
