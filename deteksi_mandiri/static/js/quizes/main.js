<<<<<<< HEAD
window.onload = function () {
  const modalBtns = [...document.getElementsByClassName("modal-button")];
  const startBtn = document.getElementById("start-button");
  const modalBody = document.getElementById("modal-body-confirm");
  const url = window.location.href;

  modalBtns.forEach((modalBtn) =>
    modalBtn.addEventListener("click", () => {
      const pk = modalBtn.getAttribute("data-pk");
      const name = modalBtn.getAttribute("data-quiz");
      const question = modalBtn.getAttribute("data-question");
      const time = modalBtn.getAttribute("data-time");
      const pass = modalBtn.getAttribute("data-pass");

      modalBody.innerHTML = `
        <div class="header-text-muted h10 mb-3">Are you sure want to begin <b>"${name}"</b>?</div>
        <div class="text-muted">
          <ul>
            <li>Test Name : ${name}</li>
            <li>Number of Question : ${question}</li>
            <li>Duration : ${time} min</li>
          </ul>
        </div>
      `;

      startBtn.addEventListener("click", () => {
        window.location.href = url + pk;
      });
    })
  );
};
=======
//make sure window is loaded
window.onload = function () {

  //initialize variable
  const modalBtns = [...document.getElementsByClassName("modal-button")];
  const editBtns = [...document.getElementsByClassName("edit-btn")];
  const seeBtns = [...document.getElementsByClassName("see-btn")];
  const deleteBtns = [...document.getElementsByClassName("delete-btn")];
  const editQuestionBtns = [...document.getElementsByClassName("edit-question-btn")];
  const deleteQuestionBtns = [...document.getElementsByClassName("delete-question-btn")];
  const startBtn = document.getElementById("start-button");
  const modalBody = document.getElementById("modal-body-confirm");
  const create_quiz = document.getElementById("create-quiz");
  const see_question = document.getElementById("see-question");
  const goback1 = document.getElementById("goback1");
  const goback2 = document.getElementById("goback2");
  const url = window.location.href;
  

  //Listener in Create Quiz Button
  if(create_quiz != null) {
    create_quiz.addEventListener('click', ()=> {

      window.location.href = url + 'create-quiz/';
    })
  }


  //Listener in see Question Button
  if(see_question != null) {

    see_question.addEventListener('click', ()=> {
      
      window.location.href = url + 'see-questions/';
    })
  }


  // Listener in Goback Button
  if(goback1 != null) {
    goback1.addEventListener('click', ()=> {

      window.location.href = '/'
    })
  }


  // Listener for GoBack Button
  if(goback2 != null){
    goback2.addEventListener('click', ()=> {

      window.location.href = '/deteksi-mandiri/'
    })
  }


  // Looping all modalBtn that contain quiz data
  modalBtns.forEach((modalBtn) =>

    // If modal button is clicked
    modalBtn.addEventListener("click", () => {
      const pk = modalBtn.getAttribute("data-pk");
      const name = modalBtn.getAttribute("data-quiz");
      const question = modalBtn.getAttribute("data-question");
      const time = modalBtn.getAttribute("data-time");
      const pass = modalBtn.getAttribute("data-pass");
      const action = modalBtn.getAttribute("data-action");

      // Add this html tag to modalBody
      modalBody.innerHTML = `
			<div class="header-text-muted h10 mb-3">Are you sure want to begin <b>"${name}"</b>?</div>
			<div class=text-muted>
				<ul>
					<li>Test Name : ${name}</li>
					<li>Number of Question : ${question}</li>
					<li>Duration : ${time} min</li>
				</ul>
			</div>`;

      // If start button in modal is clicked, stary quiz
      startBtn.addEventListener("click", () => {
        
        window.location.href = url + pk;
      });
    })
  );

  // Looping all editBtns that contain quiz data
  editBtns.forEach((editBtn) =>

    // If edit button is clicked
    editBtn.addEventListener("click", () => {
      const pk = editBtn.getAttribute("data-pk");

      window.location.href = url + 'edit/' + pk ;
    })
  );

  // Looping all seeBtns that thats contains data-pk for question
  seeBtns.forEach((seeBtn) =>

    // If modal button is clicked
    seeBtn.addEventListener("click", () => {
      const pk = seeBtn.getAttribute("data-pk");

      window.location.href = url + 'see-questions/' + pk ;

    })
  );


  // Looping all modalBtn that contain quiz data
  deleteBtns.forEach((deleteBtn) =>

    // If modal button is clicked
    deleteBtn.addEventListener("click", () => {
      const pk = deleteBtn.getAttribute("data-pk");
      const name = deleteBtn.getAttribute("data-quiz");
      const question = deleteBtn.getAttribute("data-question");
      const time = deleteBtn.getAttribute("data-time");
      const pass = deleteBtn.getAttribute("data-pass");
      const action = deleteBtn.getAttribute("data-action");

      // Add this text to modalBody
      modalBody.innerHTML = `
      <div class="header-text-muted h10 mb-3">Are you sure want to delete <b>"${name}"</b>?</div>
      <div class=text-muted>
        <ul>
          <li>Test Name : ${name}</li>
          <li>Number of Question : ${question}</li>
          <li>Duration : ${time} min</li>
        </ul>
      </div>`;

      // If start button in modal is clicked, delete quiz
      startBtn.addEventListener("click", () => {
        
        window.location.href = url + 'delete/' + pk;
      });
    })
  );

  // Looping all editQuestionsBtns that contain question data
  editQuestionBtns.forEach((editQuestionBtn) =>

    // If modal button is clicked
    editQuestionBtn.addEventListener("click", () => {
      const pk = editQuestionBtn.getAttribute("data-pk");

      window.location.href = url + '/edit/' + pk ;
    })
  );

  // Looping all deleteQuestionBtns that contain question data
  deleteQuestionBtns.forEach((deleteQuestionBtn) =>

    // If modal button is clicked
    deleteQuestionBtn.addEventListener("click", () => {
      const pk = deleteQuestionBtn.getAttribute("data-pk");
      const text = deleteQuestionBtn.getAttribute("data-questions");

      // Add this text to modalBody
      modalBody.innerHTML = `
      <div class="header-text-muted h10 mb-3">Are you sure want to delete <b>"${text}"</b>?</div>`;

      // If start button in modal is clicked, the question will be deleted
      startBtn.addEventListener("click", () => {

        window.location.href = url + '/delete/' + pk;
      
      });
    })
  );

};
>>>>>>> 99d81d9a1038e3c401a758a44d449b85248bed7d
