const submitButton = document.querySelector("#submit-button");
const textInput = document.querySelector("#text-input");
const resultP = document.querySelector("#result-p");
const resultSpan = document.querySelector("#result-span");

const backendUrl = "http://localhost:8000";

const onSubmitClick = () => {
  const text = textInput.value;
  const payload = { text };
  fetch(`${backendUrl}/predict_rating`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      resultP.style["display"] = "block";
      resultSpan.innerHTML = data.rating;
    })
    .catch(err => {
      console.log(err)
    });
};

submitButton.addEventListener("click", onSubmitClick);
