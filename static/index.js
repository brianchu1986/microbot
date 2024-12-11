function touchStartHandler(event) {
    var direction = event.target.dataset.direction;
    console.log("Touch Start :: " + direction);
    targetUrl = "/?move=" + direction;
    console.log(targetUrl);
    fetch(targetUrl, {
        method: "GET", // default, so we can ignore
    });
}

function touchEndHandler(event) {
    const stop_command = "stop";
    var direction = event.target.dataset.direction;
    console.log("Touch End :: " + direction);
    targetUrl = `/?move=stop`;
    console.log(targetUrl);
    fetch(targetUrl, {
        method: "GET", // default, so we can ignore
    });
}
function speedClickHandler(event) {
    var speed = event.target.dataset.speed;
    console.log("Speed Click :: " + speed);
    targetUrl = "/?speed=" + speed;
    console.log(targetUrl);
    fetch(targetUrl, {
        method: "GET", // default, so we can ignore
    })
        .then((response) => {})
        .catch((error) => {
            console.log(error);
        });
    let span = document.getElementById("speed");
    span.innerHTML = "<strong>" + speed.toUpperCase() + "</strong>";
}
document.querySelectorAll(".move_button").forEach((item) => {
    item.addEventListener("touchstart", touchStartHandler);
});

document.querySelectorAll(".move_button").forEach((item) => {
    item.addEventListener("touchend", touchEndHandler);
});
document.querySelectorAll(".move_button").forEach((item) => {
    item.addEventListener("mousedown", touchStartHandler);
});
document.querySelectorAll(".move_button").forEach((item) => {
    item.addEventListener("mouseup", touchEndHandler);
});
document.querySelectorAll(".speed_button").forEach((item) => {
    item.addEventListener("click", speedClickHandler);
});
