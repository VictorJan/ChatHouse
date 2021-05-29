const keyring = localStorage.getItem('keyring');
if (keyring) window.location.href=`${window.origin}/start`;

let running;

const confirmation_token = (running=(window.location.href.match(new RegExp('(?<=confirm/\).+')))) ? new Token(running[0]) : null
if ((!confirmation_token) || (confirmation_token.payload.token_type!="confirmation") ) window.location.href=window.href;