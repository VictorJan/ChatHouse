//cards:
const user_card = (data)=>{
	
	//data:{information:{id:...,username:...,email:...,name:...,about:...,common:[...]},current_user:bool}

	let template=document.querySelector(`#user_card_template`);
	let clone = template.content.cloneNode(true);

	clone.querySelector("#identification").innerText = data.information.username;

	Object.keys(data.information).forEach(k=>{
		if (field=clone.querySelector(`#${k}`)) clone.querySelector(`#${k}`).innerText=data.information[k];
	});

	//append common chats
	if (data.information.common_chats.length!=0){
		let common_chats_list = clone.querySelector(".list_body");
		data.information.common_chats.forEach((chat)=>{
			common_chats_list.appendChild(source_block('chat',chat));
		});
	}
	else{
		clone.firstElementChild.removeChild(clone.querySelector(".card_links"));
	}

	//Verify the current_user
	if (data.current_user == false) (logout_button=clone.querySelector("#logout_button")).parentNode.removeChild(logout_button);

	//Set up the kick off a chat with the user
	clone.querySelector("#kick_off_button").dataset['user_id']=data.information.id;

	//remove other cards
	document.querySelectorAll(".card").forEach(card=>{
		document.body.removeChild(card);
	});
	document.body.querySelector('#overlay').classList.add('active');
	document.body.appendChild(clone);

}


const chat_card = (data)=>{
	
	//data:{information:{id:...,name:...,participants:[...]}}

	let template=document.querySelector(`#chat_card_template`);
	let clone = template.content.cloneNode(true);

	clone.querySelector("#identification").innerText = data.information.name;

	Object.keys(data.information).forEach(k=>{
		if (field=clone.querySelector(`#${k}`)) clone.querySelector(`#${k}`).innerText=data.information[k];
	});

	//append participants , if there is any
	if (data.information.participants.length!=0){
		let common_chats_list = clone.querySelector(".list_body");
		data.information.participants.forEach((user)=>{
			common_chats_list.appendChild(source_block('user',user));
		});
	}
	else{
		clone.firstElementChild.removeChild(clone.querySelector(".card_links"));
	}

	//Set up the 
	clone.querySelector("#eliminate_button").dataset['card_id']=data.information.id;

	//remove other cards
	document.querySelectorAll(".card").forEach(card=>{
		document.body.removeChild(card);
	});
	document.body.querySelector('#overlay').classList.add('active');
	document.body.appendChild(clone);

}


const close_parent = (event) => {
	let element = event.target;
	element.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode);
	document.body.querySelector('#overlay').classList.remove('active');
}


//list:

const list = (type,data,parent) =>{
	let clone=document.querySelector(`#list_template`).content.cloneNode(true);
	clone.querySelector(".list_header").innerText=`${type}s`.toUpperCase();
	let body=clone.querySelector(".list_body");
	data.forEach((item)=>{
		body.append(source_block(type,item));
	})
	parent.removeChild(parent.querySelector(".list"));
	parent.appendChild(clone);
}

const clear_search_button = () =>{
	let clone=document.querySelector(`#clear_search_template`).content.cloneNode(true);
	let parent = document.querySelector(".search_block");
	parent.appendChild(clone);
}


//source block:
const source_block = (type,data)=>{
	//type=user|chat
	//meant to create a source block, where source is a substitue for a user|chat
	let clone=document.querySelector(`#source_block_template`).content.cloneNode(true);
	let link = clone.querySelector('#source_link');

	
	//Set up the link according to the type
	link.innerText = (type=='user') ? data.username : data.name;
	link.dataset[`${type}_id`]=data.id;
	
	let head_to_button = clone.querySelector("#head_to_source");
	
	if (type=='user'){
		head_to_button.parentNode.parentNode.classList.add('single');
		head_to_button.parentNode.parentNode.removeChild(head_to_button.parentNode);

	}
	else{
		head_to_button.dataset['chat_id']=data.id;
	}

	return clone;
}

const chat_utilities = (type) =>{
	//type:idle - meant to build an idle state of the utilities (send message)
	//type:active - meant to build an active state of the utilities (having selected messages - allow to delete them)
	let current=document.querySelector(".chat_utilities");
	let chat_bottom=document.querySelector(".chat_bottom");
	let clone=document.querySelector(`#chat_utilities_${type}`).content.cloneNode(true);

	if (type=='active') chat_bottom.firstElementChild.setAttribute('disabled',true); else chat_bottom.firstElementChild.removeAttribute('disabled');
	if (current) chat_bottom.removeChild(current); 
	chat_bottom.appendChild(clone);
}