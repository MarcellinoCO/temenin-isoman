// Make sure window status is onload
window.onload = function () {

	// Initialize variable
	var counter = 1;
	const titles = [...document.getElementsByClassName('title-p')];
	
	// Check if title is not null
	if(titles != null){

		// Loopin title and add Answer text 
		titles.forEach((title) => {
			title.innerHTML = `Answer ${counter}`;
			counter++
		})
	}
}