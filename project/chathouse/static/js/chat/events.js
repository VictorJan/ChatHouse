function addGlobalEventListener(type,match,callback){
	document.addEventListener(type,e =>{
		console.log(e.target.matches(match))
		if (e.target.matches(match)) callback(e);
	})
}


addGlobalEventListener('click','#user',user_card_controller);

addGlobalEventListener('click','#kick_off_chat',ko_chat_card_controller);

addGlobalEventListener('keyup','#search_field',users_list_controller);