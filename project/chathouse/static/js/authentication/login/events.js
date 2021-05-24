function addGlobalEventListener(type,match,callback){
	document.addEventListener(type,e =>{
		if (e.target.matches(match)) callback(e);
	})
}

addGlobalEventListener('click','#identify',identify_controller)