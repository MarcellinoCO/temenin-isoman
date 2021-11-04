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
