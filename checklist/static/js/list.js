const getCookie = (name) =>
  document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)")?.pop() || "";

const loadQuarantineDays = () => {
  const username = $("#username").text();
  if (!username) return;

  $.ajax({
    type: "POST",
    url: "quarantine-data",
    headers: { "X-CSRFToken": getCookie("csrftoken") },

    data: { username: username },

    success: (response) => {
      if (response && response.result == "success") {
        $("#loader").hide();
        populatePage(
          response.quarantineData,
          new Date(response.quarantineStart)
        );
      }
    },
  });
};

const populatePage = (data, start) => {
  updateTitle(data, start);
  populateDays(data, start);
};

const updateTitle = (data, start) => {
  const title = $("#title");
  const currentDay = Math.ceil((Date.now() - start) / (1000 * 60 * 60 * 24));

  if (currentDay == data.length) {
    title.html(`
      This is your${" "}
      <span class="text-primary">Last Day</span>
      ${" "}of Quarantine!
    `);
  } else {
    title.html(`
      This is your${" "}
      <span class="text-primary">Day ${currentDay}</span>
      ${" "}of Quarantine!<br/>
      ${data.length - currentDay} days to go
    `);
  }
};

const populateDays = (data, start) => {
  const daysList = $("#days");
  const currentDay = Math.ceil((Date.now() - start) / (1000 * 60 * 60 * 24));

  // Reset days list component.
  daysList.html("");

  data.forEach((day) => {
    console.log(day);
    daysList.append(`
      <div class="col">
        <div 
          class="
            ratio ratio-1x1 m-md-2 rounded-3 
            ${
              day.day == currentDay
                ? "bg-info"
                : day.day < currentDay
                ? "bg-success"
                : "bg-secondary"
            }
          "
        >
          <p class="d-flex d-md-none justify-content-center align-items-center text-white">${
            day.day
          }</p>
          <h2 class="d-none d-md-flex justify-content-center align-items-center text-white">${
            day.day
          }</h2>
        </div>
      </div>
    `);
  });
};

loadQuarantineDays();
setInterval(loadQuarantineDays, 5000);
