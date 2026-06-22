// login.js
console.log("login.js loaded!");
window.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded and parsed");

  const form = document.getElementById("loginForm");
  if (form) {
    console.log("loginForm found!");
    form.addEventListener("submit", (e) => {
      console.log("Login button clicked!");
      handleFormSubmit(e, "/api/login");
    });
  } else {
    console.error("loginForm not found!");
  }
});
