function getCookie(name){
	var cookieValue;
	if (document.cookie && document.cookie !== ''){
		let cookies = document.cookie.split(';');
		for (let i=0; i<cookies.length; i++){
			cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')){
				cookieValue = decodeURIComponent(cookie.substring(name.length+1));
				break
			}
		}
	}
	return cookieValue;
}