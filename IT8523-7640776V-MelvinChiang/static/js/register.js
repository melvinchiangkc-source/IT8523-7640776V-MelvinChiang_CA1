// register.js
console.log("register.js loaded!");

window.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded and parsed");

  const form = document.getElementById("registerForm");
  if (form) {
    console.log("registerForm found!");
    form.addEventListener("submit", (e) => {
      console.log("Register button clicked!");
      handleFormSubmit(e, "/api/register");
    });
  } else {
    console.error("registerForm not found!");
  }
});
