function displayFileName() {
    var fileInput = document.getElementById("videoFile");
    var fileNameDisplay = document.getElementById("fileName");
    var videoPlayer = document.getElementById("videoPlayer");

    if (fileInput.files.length > 0) {
        fileNameDisplay.innerText = "Selected file: " + fileInput.files[0].name;
        var file = URL.createObjectURL(fileInput.files[0]);
        videoPlayer.src = file;
        videoPlayer.style.display = "block";
    } else {
        fileNameDisplay.innerText = "";
        videoPlayer.style.display = "none";
    }
}

function uploadFile() {
    var fileInput = document.getElementById("videoFile");
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("response").innerText = data;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("response").innerText = "Error uploading file.";
    });
}

function uploadUrl() {
    var urlInput = document.getElementById("videoUrl");
    var url = urlInput.value;

    if (!url) {
        document.getElementById("response").innerText = "Please enter a valid video URL.";
        return;
    }

    var formData = new FormData();
    formData.append("url", url);

    fetch("/upload-url", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("response").innerText = data;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("response").innerText = "Error uploading video URL.";
    });
}
