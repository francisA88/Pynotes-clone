let sugg = document.querySelector(".suggestions");

const searchElem = document.querySelector(".sugg-input");

function clearChildren(elem){
	for (child of elem.children){
		elem.removeChild(child);
	}
}
async function getSearchResults(s){
	let res = await fetch(`/search/${s}`);
	let data = await res.json();
	return data;
}
let clear = ()=>{
	try{
	  sugg.replaceChildren();
	}
	catch(err){
	  clearChildren(sugg);
	}
}
searchElem.addEventListener("input", function(e){
	
	clear();

  if (this.value){
	  let suggestions = getSearchResults(this.value);
		suggestions.then(
			(d)=>{
			notes = d.notes;
		  for (let note of notes){
		    let option = document.createElement("li");
		    let anchor = document.createElement('a');
		    anchor.innerHTML = note.title;
		    anchor.href = `/notes/${note.note_num}/view`;
		    option.appendChild(anchor);
		    sugg.appendChild(option);
		  }
		})
	}else{
		clear();
	}
})

const pwdToggleBtn = document.getElementById('password-toggle');
const passwordInput = document.querySelector('#pwd');
const attrs = ['password','text']
let t = 1;
pwdToggleBtn.addEventListener('click', function(e){
	passwordInput.setAttribute('type', attrs[t]);
	t ^= 1;
})

const titleInput = document.querySelector('#title-input');
const contentInput = document.querySelector('#content-input');
const clearAllBtn = document.querySelector('#clear-all');

clearAllBtn.addEventListener('click', (e)=>clearAll());
function clearAll(){
	titleInput.value = '';
	contentInput.value = '';
	passwordInput.value = '';
}
document.querySelector('#clearbtn').addEventListener('click', function(e){
	searchElem.value = '';
	clear();
})

const successNotification = document.querySelector('.notification');

document.querySelectorAll(".delete").forEach(elem=>{
	elem.addEventListener('click', function(e){
		elem.parentElement.style.display = 'none';
	})
})
function saveNote(){
	let data = {
		title: titleInput.value,
		content: contentInput.value,
		password: passwordInput.value,
	}
	let response = fetch('/notes/save/',{
		method: 'POST',
		body: JSON.stringify(data),
		headers: {"X-CSRFToken": getCookie('csrftoken')}
	});
	response.then(res=>{
		if (res.status === 201){
			successNotification.style.display = 'flex';
			//Automatically remove the notification after a second.
			setTimeout(f=>{
				if (successNotification.style.display === 'flex') successNotification.style.display = 'none';
			}, 2000);
		}
	})
}

const submitBtn = document.querySelector("#submit-btn");
submitBtn.addEventListener('click', (e)=>saveNote());