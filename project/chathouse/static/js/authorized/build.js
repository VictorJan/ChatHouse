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
	if (data.current_user == false) (utilities=clone.querySelector(".card_utilities")).parentNode.removeChild(utilities);

	//remove other cards
	document.querySelectorAll(".card").forEach(card=>{
		document.body.removeChild(card);
	});
	document.body.querySelector('#overlay').classList.add('active');
	document.body.appendChild(clone);

}

const account_card = () =>{
	let template=document.querySelector(`#account_card_template`);
	let clone = template.content.cloneNode(true);

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
		if ((field=clone.querySelector(`#${k}`)) && k!='creator') clone.querySelector(`#${k}`).innerText=data.information[k];
	});

	clone.querySelector('#creator').appendChild(source_block('user',data.information.creator))

	//append participants , if there is any
	if (data.information.participants.length!=0){
		let participants = clone.querySelector(".list_body");
		data.information.participants.forEach((user)=>{
			participants.appendChild(source_block('user',user));
		});
	}
	else{
		clone.firstElementChild.removeChild(clone.querySelector(".card_links"));
	}

	//Set up the 
	clone.querySelector("#discharge_chat_button").dataset['chat_id']=data.information.id;

	//remove other cards
	document.querySelectorAll(".card").forEach(card=>{
		document.body.removeChild(card);
	});
	document.body.querySelector('#overlay').classList.add('active');
	document.body.appendChild(clone);

}

const new_chat_card = () =>{
	
	//data:{information:{id:...,name:...,participants:[...]}}

	let template=document.querySelector(`#new_chat_card_template`);
	let clone = template.content.cloneNode(true);

	let list = clone.firstElementChild;

	//remove other cards
	document.querySelectorAll(".card").forEach(card=>{
		document.body.removeChild(card);
	});
	document.body.querySelector('#overlay').classList.add('active');
	document.body.appendChild(clone);

}



const close_card = (event) => {
	let element = event.target;
	element.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode);
	document.body.querySelector('#overlay').classList.remove('active');
}

const notification = (data,utilities=false) =>{
	let clone=document.querySelector(`#notification_template`).content.cloneNode(true);
	clone.querySelector(".notification_message").innerText=data;
	let notification_layout=document.querySelector(".notification_layout");
	if (notification_layout){
		//remove the previous notifications
		let previous;
		if (previous=document.querySelector(".notification_block")) notification_layout.removeChild(previous);

		//remove the utlities from the template - based on the argument.
		let clear_button;
		if (!utilities) (clear=clone.querySelector("#clear_invalid_button")).parentNode.removeChild(clear);

		notification_layout.appendChild(clone);
	}
}

const notification_utility = (data) =>{
	let clone=document.querySelector(`#notification_template`).content.cloneNode(true);
	clone.querySelector(".notification_message").innerText=data;
	let notification_layout=document.querySelector(".notification_layout");
	if (notification_layout){
		//remove the previous notifications
		let previous;
		if (previous=document.querySelector(".notification_block")) notification_layout.removeChild(previous);
		notification_layout.appendChild(clone);
	}
}

//list:

const list = (type,data,parent) =>{

	//clone the list template
	let clone=document.querySelector(`#list_template`).content.cloneNode(true);

	let list_identification;

	//Set up the identification for the list = "users|chats|participants_list"
	clone.firstElementChild.setAttribute("id",(list_identification=`${type}s_list`));
	if (type=='participant') clone.firstElementChild.style.gridTemplateRows="none";

	let header=clone.querySelector(".list_header");
	if (type=='participant') header.parentNode.removeChild(header); else header.innerText=`${type}s`.toUpperCase();
	
	let body=clone.querySelector(".list_body");
	data.forEach((item)=>{
		body.append(source_block(type,item));
	});

	//header.parentNode.style.gridTemplateRows = (type=='participant')?"1fr":header.parentNode.style.gridTemplateRows;
	body.style.maxHeight=(type=='participant')?'30vh':'75vh';

	let previous_list;
	
	if (previous_list=parent.querySelector(`.list`)) parent.removeChild(previous_list);

	parent.appendChild(clone);
}

const clear_search_button = (parent) =>{
	let clone=document.querySelector(`#clear_search_template`).content.cloneNode(true);
	parent.appendChild(clone);
}


//source block:
const source_block = (type,data)=>{
	//type=user|chat|participant
	//meant to create a source block, where source is a substitue for a user|chat
	let clone=document.querySelector(`#source_block_template`).content.cloneNode(true);
	
	let block = clone.firstElementChild;
	
	let link = clone.querySelector('#source_link');


	
	//Set up the link according to the type
	link.innerText = (type!='chat') ? data.username : data.name;
	link.dataset[`${type}_id`]=data.id;
	

	let head_to_button = clone.querySelector("#head_to_source");
	
	if (type!='chat'){
		if (type=='user'){
			block.classList.add('single');
			block.setAttribute('id','user_block');
		}
		else{
			block.classList.add('participant');
			block.setAttribute('id','participant_block');
			block.dataset[`participant_id`] = data.id;  
		}

		block.removeChild(head_to_button.parentNode);
	}
	else{
		block.dataset['chat_id']=data.id;
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




const message = (payload,established=true,sent=true) => {
	try{
		//payload : {sender:{id:int,username:str}, data:str, dnt:str}
		let clone = document.querySelector("#message_template").content.cloneNode(true);
		//set up the message id
		clone.firstElementChild.dataset.message_id=payload.id;
		//set up the source-source block
		let sender = clone.querySelector("#source_link");
		//set the dataset for the source card
		sender.dataset.user_id=payload.sender.id;
		//set the inner html to the username of the sender
		sender.innerText=payload.sender.username;
		//set the dnt of the message
		clone.querySelector(".right_source_block").innerText=payload.dnt;
		//inject the decrypted message
		clone.querySelector("#message_content").innerText=payload.content;

		let chat = document.querySelector(".chat_content");
		let sentinel = chat.querySelector("#chat_sentinel");
		let previous_height = chat.scrollHeight;
		//Then, if the message just have been established -> append it to the chat, otherwise prepend it to the top.
		if (established==true) chat.appendChild(clone); else chat.insertBefore(clone,sentinel.nextSibling);
		
		//Scroll to the bottom if the previous height is the same as the static height and the messages start to overflow.
		//Otherwise stay at the same height
		chat.scrollTop = (previous_height==chat.clientHeight) ? chat.scrollHeight : (chat.scrollTop)
	}
	catch{
		notification("Coudn't inject the message.")
	}
	
}