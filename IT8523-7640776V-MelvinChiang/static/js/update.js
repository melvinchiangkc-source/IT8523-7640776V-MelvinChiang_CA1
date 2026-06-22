// update.js
console.log("update.js loaded!");

document.getElementById("updateForm")?.addEventListener("submit", (e) => {
  console.log("Update form submit event triggered");
  console.log("Event object:", e);

  const userId = document.getElementById("userId")?.value.trim();
  console.log("User ID from input:", userId);

  if (!userId) {
    console.log("Validation failed: User ID is empty");
    alert("User ID is required.");
    return;
  }

  console.log("Validation passed, calling handleFormSubmit");

  handleFormSubmit(e, `/api/update/${userId}`, {}, "PUT");

  console.log("handleFormSubmit called");
});

console.log("Update form event listener attached");
