class Token{
	#payload;

	constructor(raw){
		this.#payload=this.#decode(raw)
	}
	#decode(raw_data){
		try{
			return JSON.parse(window.atob(raw_data.split('.')[1]));
		}
		catch{
			return null;
		}
	}
	get payload(){
		return this.#payload;
	}
}