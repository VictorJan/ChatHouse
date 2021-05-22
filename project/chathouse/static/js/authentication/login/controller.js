async function identify_controller(e){
		let data={};
		e.target.parentNode.querySelectorAll('#identification').forEach(el=>{
			if (el.value!="") data[el.id]=el.value;
		});
		if (Object.keys(data).length == 1){
			let result = await verification_call(data);
			if (result.status == 201){
				document.querySelector(".feedback").innerHTML="The verification email has been sent."
			}
			else{
				if (result.status==401) window.location.replace(window.location.href);
				document.querySelector(".feedback").innerHTML="Please enter valid data."
			}
		}
	}