let themeAudio = new Audio("./assets/sounds/Mission_Complete.wav");
themeAudio.volume = 1.0;
themeAudio.currentTime = 0;
themeAudio.play();

setTimeout(function () {
    self.location.href = "../index.html";
}, 8000);