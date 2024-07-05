function send_message() {
    let inputBox = document.getElementById("input_box");
    let messageBox = document.getElementById("message_box");
    let message = inputBox.value;
    let currentContents = messageBox.value;
    console.log(message);
    inputBox.value = "";
    messageBox.value = currentContents + message + "\n"
    let formData = new FormData;
    formData.set("message", message)
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/chat.html", true);
    xhr.send(formData);
}