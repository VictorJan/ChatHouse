function addGlobalEventListener(type,match,callback){
	document.addEventListener(type,e =>{
		if (e.target.matches(match)) callback(e);
	})
}

addGlobalEventListener('click','#confirm',confirmation_controller);