const loadQuarantineDays = () => {
  $.ajax({
    type: "POST",
    url: "/quarantine-days",
    success: (response) => {
      console.log(response);
    },
  });
};

setInterval(loadQuarantineDays, 5000);
