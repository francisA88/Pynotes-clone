const field = document.querySelector('.pass-field');
const submitBtn = document.querySelector('#submit');
const errorLabel = document.querySelector('.pass-error');
const form = document.forms[0];

console.log(errorLabel)
submitBtn.addEventListener('click', function(e){
	let value = field.children[0].value;
	let num = field.children[0].dataset.id;
	if (!value) return false;
	fetch(`/notes/${num}/validate`, {
		method: 'POST',
		headers: {"X-CSRFToken": getCookie('csrftoken')},
		body: value,
	}).then(res=>{
		if (res.status == 401 && errorLabel.classList.contains('hide')) {
			errorLabel.classList.remove('hide');
			setTimeout(()=>errorLabel.classList.add('hide'), 1500);
		}
		else{
			res.text().then(data=>{
				if(data.startsWith('key:')){
					let key = data.slice(4);
					console.log(key, num);
					location.href = `/notes/${key}/${num}`;
				}
			})
		}
	})
})