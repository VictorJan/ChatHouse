function addGlobalEventListener(type,match,callback){
	document.addEventListener(type,e =>{
		if (e.target.matches(match)) callback(e);
	})
}


addGlobalEventListener('click','#source_link',source_card_controller);
addGlobalEventListener('click','#close_button',close_parent);

addGlobalEventListener('keyup','#search_field',search_list_controller);
addGlobalEventListener('click','#clear_search_button',clear_search);

addGlobalEventListener('click','#head_to_source',head_controller);

addGlobalEventListener('click','#logout_button',logout);


addGlobalEventListener('click','.source_block, .message_content_block,.message_block',select_message_controller)