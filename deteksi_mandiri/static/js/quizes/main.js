//make sure window is loaded
window.onload = function () {

  //initialize variable
  const modalBtns = [...document.getElementsByClassName("modal-button")];
  const startBtn = document.getElementById("start-button");
  const modalBody = document.getElementById("modal-body-confirm");
  const url = window.location.href;

  //looping all modalBtn that contain quiz data
  modalBtns.forEach((modalBtn) =>

    //if modal button is clicked
    modalBtn.addEventListener("click", () => {
      const pk = modalBtn.getAttribute("data-pk");
      const name = modalBtn.getAttribute("data-quiz");
      const question = modalBtn.getAttribute("data-question");
      const time = modalBtn.getAttribute("data-time");
      const pass = modalBtn.getAttribute("data-pass");

      //add this text to modalBody
      modalBody.innerHTML = `
			<div class="header-text-muted h10 mb-3">Are you sure want to begin <b>"${name}"</b>?</div>
			<div class=text-muted>
				<ul>
					<li>Test Name : ${name}</li>
					<li>Number of Question : ${question}</li>
					<li>Duration : ${time} min</li>
				</ul>
			</div>`;

      //if start button in modal is clicked, stary quiz
      startBtn.addEventListener("click", () => {
        
        window.location.href = url + pk;
      });
    })
  );
};
