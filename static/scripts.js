function send_message() {
    let inputBox = document.getElementById("input_box");
    let messageBox = document.getElementById("message_box");
    let message = inputBox.value;
    let currentContents = messageBox.value;
    inputBox.value = "";
    messageBox.value = currentContents + message + "\n";
    fetch ("/chat.html", {
        method: "POST",
        body: new URLSearchParams({ message: message }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message)
    })
    .catch(error => {
        console.log(error);
    });
}

function send_login_request() {
    let form = document.getElementById("login_form");
    let formData = new FormData(form);
    fetch ("/login.html", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message)
        if (data.result == "INVALID_CREDS") {
            alert("Wrong username or password.")
        }
    })
    .catch(error => {
        console.log(error);
    });
}

function send_signup_request() {
    let form = document.getElementById("signup_form");
    let formData = new FormData(form);
    fetch ("/login.html", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message)
        if (data.result == "INVALID_CREDS"){
            alert("Error in your registration. Make sure you follow the guidelines\n1. Password must be between 8 and 20 characters, and contain at least 1 digit\n2. Usernames must be between 3 and 20 characters\n3. Emails must be valid emails")
        }
    })
    .catch(error => {
        console.log(error);
    });
}