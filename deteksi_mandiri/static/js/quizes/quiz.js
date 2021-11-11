<<<<<<< HEAD
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
=======
// Make sure if window is loaded
window.onload = function () {

  // Initialize variables
  const url = window.location.href;
  const quizBox = document.getElementById("quiz-box");
  const scoreBox = document.getElementById("score-box");
  const summaryTitle = document.getElementById("sumarry-title");
  const summary = document.getElementById("summary");
  const timerBox = document.getElementById("timer");
  const display_result = document.getElementById("result");
  let stopTimer = false;


  /**
   * Function for activated timer which executed when quiz started
   * 
   * @param time represent quiz time in minutes
   * */
  const activateTimer = (time) => {

    // Initialize strTime and append display it in html
    strTime = ("00"+time).slice(-2)
    timerBox.innerHTML = `<b>${strTime}:00</b>`

    // Variable for timer 
    let minutes = time - 1;
    let seconds = 60;
    let displaySeconds;
    let displayMinutes;


    // Function for countdown the timer
    const timer = setInterval(() => {
      
      seconds -= 1;

      // When second <0, change it to 59 and subtract minute by 1
      if (seconds < 0) {
        seconds = 59;
        minutes -= 1;
      }

      displayMinutes = ("00"+minutes).slice(-2)

      // When minutes < 0, set displaySecond and displayMinutes to 0
      if (minutes < 0) {
        displaySeconds = 0;
        displayMinutes = 0;
      }

      displaySeconds = ("00"+seconds).slice(-2)

      // When minutesd and second <=0 send data to the server and stop quiz
      if (minutes <= 0 && seconds <= 0) {
        setTimeout(() => {
          alert("Time Over!!");
          clearInterval(timer);
          timerBox.innerHTML = `<b>00:00</b>`;
          sendData(true);
        }, 400);
      }

      // Excecuted when there is an event from submit button. Set timer to 00:00
      if (stopTimer) {
        setTimeout(() => {
          clearInterval(timer);
          timerBox.innerHTML = `<b>00:00</b>`;
        }, 0);
      }

      // Display timer into timerBox
      timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`;
    }, 1000);
  };

  $.ajax({
    type: "GET",
    url: `${url}data`,
    success: function (response) {

      // Response.data contains question as key and qnswer as value
      data = response.data;

      // Looping data
      data.forEach((el) => {

        // Get question and answer from data and then add it into quizBox
        for (const [question, answers] of Object.entries(el)) {
          quizBox.innerHTML += `
						<hr>
						<div class ="mb-1 questions">
							<b> ${question} </b>
						</div>`;

          // Looping all answer for each question and display it into quizBox
          answers.forEach((answer) => {
            quizBox.innerHTML += `
							<div class="form-field">
								<input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}"></input>
								<label for="${question}-${answer}">${answer}</label>
							</div>`;
          });
        }
      });

      // Activated timer when all question and answer is loaded
      activateTimer(response.time);
    },
    error: function (error) {
      
      console.log(error);
    },
  });

  // Get quiz-from and csrfmiddlewaretoken
  const quizForm = document.getElementById("quiz-form");
  const csrf = document.getElementsByName("csrfmiddlewaretoken");
  

  /**
   * SendData funtion for send user answer to the server
   * 
   * @param truth represent true id sendData called from timer event 
   *        and false if sendData called from submit button
   * */
  const sendData = (truth) => {

    // Elements contain all answer from each quiz
    const data = {};
    const elements = [...document.getElementsByClassName("ans")];
    data["csrfmiddlewaretoken"] = csrf[0].value;

    // Looping elements and get checked answer
    elements.forEach((el) => {

      // Append user answer to data
      if (el.checked) {
        data[el.name] = el.value;
      } 

      // Executed when user doesn't check this answer
      else {
        if (!data[el.name]) {
          data[el.name] = null;
        }
      }
    });

    $.ajax({
      type: "POST",
      url: `${url}save`,
      data: data,
      success: function (response) {
       
        // Executed when user answer all questions or user haven;t answer all questions until timeover
        if (response.full == "True" || truth) {

          // Stop timer
          stopTimer = true;
          
          // Get all user answer 
          const results = response.results;
          
          // Hide quiz form and display result 
          quizForm.classList.add("disp_none");
          display_result.style.display='flex';
          summaryTitle.classList.remove('disp_none');

          // Add this text to scoreBox 
          scoreBox.innerHTML = `${
            response.passed == "True"
              ? "Congratulations. You have a low risk of becoming infected with CODIV-19. Stay healthy! :D"
              : "You have a high risk of getting infected with COVID-19. Immediately consider contacting the hospital for a swab test!"}. 
              Your score for ${response.quiz} is ${response.score}%`;

          // Looping all result and display itu
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

            // Append resDiv into summary
            summary.append(restDiv);
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

  // Listeter for quizForm, if button clicked, sendData to the server and display result
  quizForm.addEventListener("submit", (e) => {
   
    e.preventDefault();
    sendData(false);
  });
};
>>>>>>> 99d81d9a1038e3c401a758a44d449b85248bed7d
