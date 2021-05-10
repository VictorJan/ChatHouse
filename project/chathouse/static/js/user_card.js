function build_a_card(data){
	//data:{information:{username:...,email:...,name:...,about:...},current_user:bool}
	let template=document.querySelector("#user_card_template");
	let clone=template.content.cloneNode(true);
	Object.keys(data.information).forEach(k=>{
		clone.querySelector(`#${k}`).innerHTML=data.information[k];
	})
	document.body.querySelector('#overlay').classList.add('active');
	document.body.appendChild(clone);
}

function close_a_card(element){
	element.parentNode.removeChild(element);
	document.body.querySelector('#overlay').classList.remove('active');
}