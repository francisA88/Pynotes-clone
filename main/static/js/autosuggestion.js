const suggestions = document.querySelectorAll('.suggestions');


function adjustSuggestionsSize(){
	suggestions.forEach(el=>{
		let parent = el.parentElement;
		let input = parent.querySelector('.sugg-input');
		console.log(el)
		console.log(input)
		el.style.left = `${input.clientLeft/2+input.offsetLeft}px`;
		el.style.top = `${input.offsetHeight + input.offsetTop}px`;
		el.style.width = `${input.clientWidth}px`;
	})
}
adjustSuggestionsSize();
window.onresize = (e)=> adjustSuggestionsSize();