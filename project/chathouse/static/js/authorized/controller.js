async function select_message_controller(e){
	let message = (e.target.dataset.message_id) ? e.target : e.target.parentNode;
	if (message.dataset.message_id)
	{
		if (!document.querySelector("#discharge_message_button")) chat_utilities('active');

		let dataset_storage = document.querySelector("#discharge_message_button");

		select('message',message,dataset_storage);
	}
}

async function select_participant_controller(e){
	let participant = (e.target.dataset.participant_id) ? e.target : null;
	if ((participant) && (participant.dataset.participant_id))
	{
		let dataset_storage = document.querySelector("#establish_chat_button");

		let username = select('participant',participant,dataset_storage);
		if (username) document.querySelector("#search_field[data-type='participant']").value=username;
	}
}


//CHAT
//Establish a chat
async function establish_chat_controller(e){
	let input_field = document.querySelector('#chat_name');
	if ((input_field) && (input_field.value!='')){
		let payload = {participant_id:e.target.dataset.participant_id, name: input_field.value}
		notification_socket.establish_a_chat(payload);
	}

}
//Discharge a chat
async function discharge_chat_controller(e){
	let chat_id;
	if ((chat_id=Number(e.target.dataset.chat_id))) notification_socket.discharge_a_chat({id:chat_id});
	//close the card:
	let close_button;
	if (close_button=document.querySelector("#close_button")){
		let close_event = new Event('click');
		close_button.dispatchEvent(close_event);
		close_card(close_event);
	}
}

async function establish_message_controller(e){
	try{
		let message = document.querySelector('#message_field').value;
		//send the message if it contains at least one character apart from the white spaces.
		if (message.match(/(?=.*(?:[\S].*){1,}).+/)) chatInstance.send(message);
	}
	catch{
		notification("Coulnd't establish a message, due to absence of the message field.")
	}
}

async function discharge_message_controller(e){
	let up_for_discharge = Array.from(new Set(e.target.dataset.message_id.split(',').map((message)=>Number(message))));
	if (up_for_discharge.length>0) chatInstance.remove(up_for_discharge); chat_utilities('idle');
}

async function clear_invalid_controller(e){
	chatInstance.sanitize();
}

async function cancel_discharge_message_controller(e){
	let utilities = e.target.parentNode;
	let delete_button;
	if (delete_button=utilities.querySelector('#discharge_message_button')){
		//remove from all selected messages - the selected class
		delete_button.dataset.message_id.split(',').forEach((message_id)=>{
			document.querySelector(`#message[data-message_id='${message_id}']`).classList.remove("selected");
		})
		delete_button.dataset.message_id='';
		//set the utilities to idle
		chat_utilities('idle');
	}
}






//close_notification_button
function close_notification_controller(e){
	let block;
	if (block=e.target.parentNode) block.parentNode.removeChild(block);
}

function close_card_controller(e){
	let element = e.target;
	element.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode);
	document.body.querySelector('#overlay').classList.remove('active');
}



async function head_controller(e){
	let chat;
	if (chat=e.target.dataset.chat_id) window.location.replace(`${window.origin}/chat?id=${chat}`);
}

async function logout_controller(e){
	await userInstance.logout();
}

async function terminate_controller(e){
	await userInstance.request_confirmation('delete');
}

async function reset_password_controller(e){
	await userInstance.request_confirmation('put');
}