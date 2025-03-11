document.addEventListener("DOMContentLoaded", function() {
    let title = document.getElementById("header-title");
    title.style.opacity = "0"

    window.addEventListener("scroll", function (){
        if (document.documentElement.scrollTop <= 0) {
            title.style.opacity = "0";
        }

        else {
            title.style.opacity = "1";
        }
    });
});