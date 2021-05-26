
//Once the user signs up , they create a DH_Key , based on the domain data of the server. Then export their keyring : {public:value, private:{iv:value,content:value},g:value,m:value}, for the server to store.
//Once the user logs in, and authenticates appropriately, respond with a private key , at this point the password is valid - so the user shouldn't have a problem creating a DH_Key based on the raw private key.
class DH_Key{
	#keyring;

	constructor(data){
		return ( async () =>
			{
				/*{
				G,M are believed to be valid domain parameters.
				data: {g:value,m:value,
				payload:{private_key:value} or
				raw:{private_key:Object value,password:value}
				}
				}
				*/
				this.modulus=data.m;
				this.generator=data.g;

				this.#keyring = (data.payload) ? {private:data.payload.private_key} : {private:await this.#parse(data.raw.private_key,data.raw.password)};

				this.#keyring.public=this.#exp(this.generator);
				return this;
			}
		)();
	}

	#exp(base){
		let power=(this.#keyring.private >>> 0).toString(2).split('');
		let z=1;

		power.forEach(bit => z=mod(base**(Number(bit)) *z**2,this.modulus))
		return z;
	}

	establish(other){
		return this.#exp(other);
	}

	get keyring(){
		return this.#keyring;
	}

	async #parse(private_key,password){

		let derived_key = (await new PBKDF(password)).value;
		let key = (await(await new AES_CBC(derived_key)).decrypt(private_key));
		if (key) {
			return Number(key);
		}
		return null;
	}

	async export(password){
		//exports the public key in an open form, the private key is encrypted using the key, derived based on the password
		let derived_key = (await new PBKDF(password)).value;
		return {public_key:this.#keyring.public, private_key:await (await new AES_CBC(derived_key)).encrypt(this.#keyring.private), g:this.generator, m:this.modulus}
	}

	store(){
		if ((this.#keyring.private) && !(sessionStorage.getItem('keyring'))){
			localStorage.setItem('keyring',JSON.stringify({g:this.generator,m:this.modulus,payload:{private_key:this.#keyring.private}}));
			return true;
		}
		return false;
	}

}

//use wrapping and unwrapping

class PBKDF
{
	#value;
	constructor(password){
		return(async()=>{
			this.#value=await this.#derive(password);
			return this;
		})();
	}

	async #derive(password){
		password = await crypto.subtle.importKey('raw', (new TextEncoder()).encode(password), 'PBKDF2',false,['deriveKey','deriveBits'])
		return  await crypto.subtle.deriveKey(
			{
				name:'PBKDF2',
				iterations:1000,
				salt: new Uint8Array(10).buffer,
				hash:'SHA-256'
			},
			password,
			{
				name:'AES-CBC',
				length:256
			},
			true,
			['encrypt','decrypt']
			);
	}

	get value(){
		return this.#value;
	}
}


class AES_CBC
{
	#key;

	constructor(key){
		this.#key=key;
	}

	async encrypt(incoming){
		//content:{iv:...,data:...}
		//return hex representation
		let encoder = new TextEncoder();
		let content = {iv:await crypto.getRandomValues(new Uint8Array(16))};
		content.data = buffer_to_hex( await crypto.subtle.encrypt(
			{
				iv:content.iv,
				name:'AES-CBC'
			},
			this.#key,
			encoder.encode(incoming)
		));
		content.iv=buffer_to_hex(content.iv);
		return content;
	}

	async decrypt(encrypted){
		//encrypted has to be a map consisting of iv and content. Convert hex values to Arrays then into Buffers.
		if (encrypted.iv && encrypted.data){
			try
			{
				let decrypted_buffer = await crypto.subtle.decrypt(
					{
						iv:hex_to_array(encrypted.iv).buffer,
						name:'AES-CBC'	
					},
					this.#key,
					hex_to_array(encrypted.data)
				);
				let array=new Uint8Array(decrypted_buffer);
				return (new TextDecoder()).decode(array);
			}
			catch{
				return null;
			}
		}
	}
}

class CipherKey
{
	#value;

	constructor(secret){
		//prepare a key for ecnryption of the messages , the secret is the real key
		return(async () =>{
			this.#value = await this.#convert(secret);
			return this;
		})();
	}
	
	async #convert(data){
		//hash the value to the 256 bits, to use for the encryption.
		let digested = await new Digest(data); 
		return await crypto.subtle.importKey("raw",digested.value,"AES-CBC",true,['encrypt','decrypt']);
	}

	async export(hex=false){
		let buffer=await crypto.subtle.exportKey("raw",this.value);
		let array=Array.from(new Uint8Array(buffer));
		if (hex) {
			return array.map(b=>b.toString(16).padStart(2,'0')).join('');
		}
		return array;
	}

	get value(){
		return this.#value;
	}
}

class Digest
{
	constructor(data,algorithm='SHA-256'){
		return(async ()=> {
				this.algorithm = algorithm;
				this.value = await this.#hash(data,algorithm);
				return this;
			}
		)();
	}

	async #hash(data,algorithm='SHA-256'){
		//Returns ArrayBuffer
		let encoder = new TextEncoder();
		return await crypto.subtle.digest(algorithm,encoder.encode(String(data)));
	}
	
	get hex(){
		return buffer_to_hex(this.value);
	}

}

buffer_to_hex = (buffer) => {
	let array=Array.from(new Uint8Array(buffer));
	return array.map(b=>b.toString(16).padStart(2,'0')).join('');
}
hex_to_array = (hex) => {
	return new Uint8Array(String(hex).match(/[a-f\d]{2}/gi).map(m=>parseInt(String(m),16)));
}

mod = (a,b)=>{
	return ((a%b)+b)%b;
}

random = (a,b)=>{
	return Math.floor(Math.random() * (b-a)+a);
}