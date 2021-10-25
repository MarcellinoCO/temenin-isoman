window.onload = function () {
  const url = window.location.href;
  const quizBox = document.getElementById("quiz-box");
  const scoreBox = document.getElementById("score-box");
  const resultBox = document.getElementById("result-box");
  const timerBox = document.getElementById("timer");

  let stopTimer = false;
  let isSubmitted = false;

  const activateTimer = (time) => {
    timerBox.innerHTML = `<b>${("00" + time).slice(-2)}:00</b>`;

    let minutes = time - 1;
    let seconds = 60;
    let displaySeconds;
    let displayMinutes;

    const timer = setInterval(() => {
      seconds -= 1;

      if (seconds < 0) {
        seconds = 59;
        minutes -= 1;
      }

      displayMinutes = ("00" + minutes).slice(-2);

      if (minutes < 0) {
        displaySeconds = 0;
        displayMinutes = 0;
      }

      displaySeconds = ("00" + seconds).slice(-2);

      if (minutes <= 0 && seconds <= 0) {
        setTimeout(() => {
          alert("Time Over!!");
          clearInterval(timer);
          timerBox.innerHTML = `<b>00:00</b>`;
          sendData(true);
        }, 400);
      }

      if (stopTimer) {
        setTimeout(() => {
          clearInterval(timer);
          timerBox.innerHTML = `<b>00:00</b>`;
        }, 0);
      }

      timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`;
    }, 1000);
  };

  $.ajax({
    type: "GET",
    url: `${url}data`,
    success: function (response) {
      data = response.data;
      data.forEach((el) => {
        for (const [question, answers] of Object.entries(el)) {
          quizBox.innerHTML += `
						<div class="mb-1 questions">
							<b> ${question} </b>
						</div>
					`;

          answers.forEach((answer) => {
            quizBox.innerHTML += `
							<div class="form-field">
								<input 
                  type="radio" 
                  class="answer" 
                  id="${question}-${answer}" 
                  name="${question}" 
                  value="${answer}" />
								<label for="${question}-${answer}">${answer}</label>
							</div>
						`;
          });
        }
      });

      activateTimer(response.time);
    },
    error: function (error) {
      console.log(error);
    },
  });

  const quizForm = document.getElementById("quiz-form");
  const csrf = document.getElementsByName("csrfmiddlewaretoken");
  const sendData = (truth) => {
    // Restrict user to submit multiple times consecutively.
    if (isSubmitted) {
      alert("Quiz already submitted!")
      return;
    }
    isSubmitted = true;

    const data = {};
    const elements = [...document.getElementsByClassName("answer")];

    data["csrfmiddlewaretoken"] = csrf[0].value;
    elements.forEach((element) => {
      if (element.checked) {
        data[element.name] = element.value;
      } else {
        if (!data[element.name]) {
          data[element.name] = null;
        }
      }
    });

    $.ajax({
      type: "POST",
      url: `${url}save`,
      data: data,
      success: function (response) {
        console.log(response.full);
        if (response.full == "True" || truth) {
          stopTimer = true;
          const results = response.results;

          quizForm.classList.add("disp_none");
          document.getElementById("score-to-pass").classList.remove("d-none");

          scoreBox.innerHTML = `${
            response.passed == "True"
              ? "Congratulations, no symptoms associated with COVID-19"
              : "The symptoms you experience are very similar to the signs of the COVID-19 virus infection. Immediately contact the relevant parties to do a swab test!"
          }. Your score is ${response.score}`;

          results.forEach((res) => {
            const restDiv = document.createElement("div");
            for (const [question, resp] of Object.entries(res)) {
              restDiv.innerHTML += question;
              
              const cls = ["p-3", "h6", "container", "text-white"];
              restDiv.classList.add(...cls);

              const answer = resp["answered"];
              const correct = resp["correct_answer"];

              if (resp == "not-answered") {
                restDiv.innerHTML += " | Not Answered";
                restDiv.classList.add("bg-secondary");
              } else {
                if (answer == correct) {
                  restDiv.classList.add("bg-success");
                  restDiv.innerHTML += ` | ${answer}`;
                } else {
                  restDiv.classList.add("bg-danger");
                  restDiv.innerHTML += ` | ${answer}`;
                }
              }
            }
            resultBox.append(restDiv);
          });
        } else {
          alert("Answer all the Questions!!");
        }
      },
      error: function (error) {
        console.log(error);
      },
    });
  };

  quizForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendData(false);
  });
};
