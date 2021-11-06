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
      console.log(response);
    },
  });
};

loadQuarantineDays();
setInterval(loadQuarantineDays, 10000);
