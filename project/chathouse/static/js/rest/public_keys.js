async function get_key_parameters(){
	let url = `${window.location.origin}/api/key-parameters`;
	const response = await fetch(url,{
		method:'GET',
		credentials:'omit',
		headers:{
			'Authorization':'Bearer'
		}
	});
	return await response.json();
}