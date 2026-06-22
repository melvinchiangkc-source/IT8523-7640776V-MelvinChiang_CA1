// common.js
console.log("common.js loaded!");

async function handleFormSubmit(event, endpoint, customData = null, method = "POST") {
    console.log("handleFormSubmit called!");  // Debugging log
    event.preventDefault();

    const formData = {};
    const inputs = event.target.querySelectorAll("input");
    inputs.forEach(input => formData[input.id] = input.value.trim());

    console.log("Collected form data:", formData);  // Debugging log

    // If customData is provided, override or merge it with formData
    const requestData = customData ? { ...formData, ...customData } : formData;

    try {
        console.log("Sending request to:", endpoint, "with data:", requestData);  // Debugging log
        const response = await fetch(endpoint, {
            method: method,  // Use the specified HTTP method
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();
        console.log("Server response:", result);  // Debugging log
        alert(response.ok ? result.message : `Error: ${result.message}`);
    } catch (error) {
        console.error("Request failed:", error);
        alert("An error occurred. Please try again.");
    }
}