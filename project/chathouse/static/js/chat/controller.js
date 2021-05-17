async function user_card_controller(e){
	if ( (typeof access_token !== "undefined") && (typeof e.target.innerHTML !== "undefined") && (e.target.innerHTML!=="") ) {
		//get_user_data(access_token,e.target.innerHTML)
		build_a_card('user',{information:{username:'username1',email:'username@gmail.com',name:'name',about:'about me.'}})
	}
}

async function ko_chat_card_controller(e){
	if ( (typeof access_token !== "undefined") && (e.target.parentNode.parentNode.querySelector('#user') !== null) ) {
		//get_user_data(access_token,e.target.innerHTML)
		build_a_card('chat',{information:{username:e.target.parentNode.parentNode.querySelector('#user').innerHTML}})
	}
}