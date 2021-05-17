function build_a_card(type,data={}){
	//data:{information:{username:...,email:...,name:...,about:...},current_user:bool}
	//type:user|chat
	let template=document.querySelector(`#${type}_card_template`);
	if (template!=null){
		let clone=template.content.cloneNode(true);
		if (data.information) {
			Object.keys(data.information).forEach(k=>{
					clone.querySelector(`#${k}`).innerText=data.information[k];
			});
		}
		
		document.querySelectorAll(".card").forEach(card=>{
			document.body.removeChild(card);
		});

		document.body.querySelector('#overlay').classList.add('active');
		document.body.appendChild(clone);
	}
}

function close_a_card(element){
	element.parentNode.removeChild(element);
	document.body.querySelector('#overlay').classList.remove('active');
}