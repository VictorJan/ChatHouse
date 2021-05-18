class Chat{
	#id;
	#token;
	#dh;
	constructor(id,token,dh){
		this.#id=id;
		this.#token=(token instanceof Token) ? token : null;
		this.#dh=(token instanceof DH_Key) ? dh : null;	
	}

	send(message){
		//calls the emit call to the socket
	}
}