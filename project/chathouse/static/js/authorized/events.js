function addGlobalEventListener(type,match,callback){
	document.addEventListener(type,e =>{
		if (e.target.matches(match)) callback(e);
	})
}

addGlobalEventListener('click','#account_button',account_card_controller);
addGlobalEventListener('click','#new_chat_button',new_chat_card_controller);
addGlobalEventListener('click','#source_link',source_card_controller);

addGlobalEventListener('click','#close_button',close_card);

addGlobalEventListener('keyup','#search_field',search_list_controller);
addGlobalEventListener('click','#clear_search_button',clear_search_controller);

addGlobalEventListener('click','#head_to_source',head_controller);

addGlobalEventListener('click','#logout_button',logout);

//New chat
addGlobalEventListener('click','#participant_block',select_participant_controller)
addGlobalEventListener('click','#establish_chat_button',establish_chat_controller)


//Messages
addGlobalEventListener('click','.source_block, .message_content_block,.message_block',select_message_controller)
addGlobalEventListener('click','#cancel_delete_button',cancel_delete_controller )