function select(identification,element,storage){
	//identification:message|participant + id ? source
	//element - the clicked element
	//storage - a button , where the data is accordingly set up

	let value;

	if (value=element.dataset[`${identification}_id`])
	{
		if (identification=='participant'){
			
			if (storage.dataset[`${identification}_id`]==value){
				storage.dataset[`${identification}_id`]='';
				element.classList.remove("selected");
				storage.disabled=true;
			}
			else{
				
				let previous={};
				if ( (previous['value']=storage.dataset[`${identification}_id`]) && (previous['element'] = element.parentNode.querySelector(`[data-${identification}_id='${previous['value']}']`)) ) previous['element'].classList.remove("selected");
				
				storage.dataset[`${identification}_id`]=value;
				element.classList.add("selected");
				storage.disabled=false;
			}
		}
		else{
			//set running message set : extract current dataset from the button -> if there is any ,then convert them into a list and map each to a Number, otherwise set an empty list .
			let message_set = new Set((storage.dataset[`${identification}_id`]!='')?
				storage.dataset[`${identification}_id`].split(',').map((item)=>Number(item))
				:[]);

			value=Number(value);
			
			if (message_set.has(value)){
				message_set.delete(value);
				element.classList.remove("selected");
			}
			else{
				message_set.add(value);
				element.classList.add("selected");
			}

			//set idle state for the utilities
			if (message_set.size==0) chat_utilities('idle');

			storage.dataset[`${identification}_id`]=Array.from(message_set);

		}

	}
}