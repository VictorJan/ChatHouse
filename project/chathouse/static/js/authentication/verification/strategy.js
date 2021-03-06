const keyring = localStorage.getItem('keyring');
if (keyring) window.location.href=`${window.origin}/start`;

let running;

const verification_token = (running=(window.location.href.match(new RegExp('(?<=verify/\).+')))) ? new Token(running[0]) : null
if ((!verification_token) || (verification_token.payload.token_type!="verification") ) window.location.href=window.href;

const preaccess_token = new Token(verification_token.payload.preaccess);
if (preaccess_token.payload.token_type!='preaccess') window.location.href=window.href;