class Token{
	#payload;
	#raw;

	constructor(raw){
		this.#raw=raw;
		this.#payload=this.#decode(raw)
	}
	#decode(raw_data){
		try{
			return JSON.parse(window.atob(raw_data.split('.')[1].replace(/-/g,'+').replace(/_/g,'/')));
		}
		catch{
			return null;
		}
	}
	get payload(){
		return this.#payload;
	}
	get raw(){
		return this.#raw;
	}
}