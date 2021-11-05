const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

const loadQuarantineDays = () => {
  const username = $("#username").text();
  if (!username) return;

  $.ajax({
    type: "POST",
    url: "quarantine-days",
    headers: { "X-CSRFToken": getCookie("csrftoken") },

    data: { "username": username },

    success: (response) => {
      console.log(response);
    },
  });
};

loadQuarantineDays()
setInterval(loadQuarantineDays, 5000);
