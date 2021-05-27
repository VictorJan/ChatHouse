function addGlobalEventListener(type,match,callback){
	document.addEventListener(type,e =>{
		if (e.target.matches(match)) callback(e);
	})
}

addGlobalEventListener('click','#account_button',account_card_controller);
addGlobalEventListener('click','#new_chat_button',new_chat_card_controller);
addGlobalEventListener('click','#source_link',source_card_controller);

addGlobalEventListener('click','#close_button',close_card_controller);

addGlobalEventListener('click','#close_notification_button',close_notification_controller);

addGlobalEventListener('keyup','#search_field',search_list_controller);
addGlobalEventListener('click','#clear_search_button',clear_search_controller);

addGlobalEventListener('click','#head_to_source',head_controller);

addGlobalEventListener('click','#logout_button',logout_controller);

//Establish a chat
//Selecet a participant event
addGlobalEventListener('click','#participant_block',select_participant_controller)
//Establish a chat button event
addGlobalEventListener('click','#establish_chat_button',establish_chat_controller)


//Chat utilities
//Discharge/remove a chat button event
addGlobalEventListener('click','#discharge_chat_button',discharge_chat_controller)


//Messages
addGlobalEventListener('click','.source_block, .message_content_block,.message_block',select_message_controller)
addGlobalEventListener('click','#establish_message_button',establish_message_controller )
addGlobalEventListener('click','#discharge_message_button',discharge_message_controller )
addGlobalEventListener('click','#clear_invalid_button',clear_invalid_controller )
addGlobalEventListener('click','#cancel_discharge_message_button',cancel_discharge_message_controller )