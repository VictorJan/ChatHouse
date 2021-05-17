async function identify_controller(e){
		let data={};
		e.target.parentNode.querySelectorAll('#email,#username,#name,#about').forEach(el=>{
			if (el.value!="") data[el.id]=el.value;
		});
		if (Object.keys(data).length == 4){
			let result = await verification_call(data);
			console.log(result)
			if (result){
				document.querySelector(".feedback").innerHTML="The email has been sent."
			}
			else{
				document.querySelector(".feedback").innerHTML="Something has gone wrong."
			}
		}
	}