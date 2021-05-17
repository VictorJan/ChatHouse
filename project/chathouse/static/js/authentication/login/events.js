function addGlobalEventListener(type,match,callback){
	document.addEventListener(type,e =>{
		console.log((e.target.matches(match)))
		if (e.target.matches(match)) callback(e);
	})
}

addGlobalEventListener('click','#identify',identify_controller)