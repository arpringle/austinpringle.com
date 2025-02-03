document.addEventListener("DOMContentLoaded", function() {
    let header = document.getElementById("sticky-header");
    header.classList.remove("border");

    window.addEventListener("scroll", function (){
        if (document.documentElement.scrollTop <= 0) {
            header.className = "";
        }

        else {
            header.className = "border";
        }
    });
});