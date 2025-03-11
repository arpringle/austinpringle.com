/*
 *
 *  Filename: scheme-switcher.js
 *
 *  Description: Code for color-scheme handling for austinpringle.com
 *
 *  Author: Copyright 2024 Austin Pringle
 *
 *  This program is free software: you can redistribute it and/or modify it under the terms of the
 *  GNU General Public License as published by the Free Software Foundation, either version 3 of
 *  the License, or (at your option) any later version.
 *
 */

let color_scheme_query = window.matchMedia("(prefers-color-scheme: dark)");
let mode = color_scheme_query.matches;

let site_mode_set = false;

switch (document.cookie) {
    case "":
        site_mode_set = false;
        break;
    default:
        site_mode_set = true;
        let cookies = document.cookie.split("; ");
        cookies.forEach(cookie => {
            let [key, value] = cookie.split("=");
            if (key === "mode") {
                mode = (value === "true");
            }
        });
}

color_scheme_query.addEventListener("change", function() {
    if (!site_mode_set) {
        toggleColorScheme();
    }
});

updateColors();

document.addEventListener("DOMContentLoaded", function() {

    let color_scheme_button = document.getElementById("color-scheme-button");
    color_scheme_button.hidden = false;
    color_scheme_button.addEventListener("click", function() {
        site_mode_set = true;
        toggleColorScheme();
        document.cookie = "mode=" + mode + ";";
    });

    let color_scheme_button_image = document.getElementById("color-scheme-button-image");
    color_scheme_button_image.src = mode ? "/icons/sun-bright.svg" : "/icons/moon.svg";

    // Ensure the animation class is removed after the animation ends
    color_scheme_button_image.addEventListener("animationend", function() {
        color_scheme_button_image.classList.remove("animate");
    });
});

function toggleColorScheme() {
    mode = !mode;
    let color_scheme_button_image = document.getElementById("color-scheme-button-image");
    color_scheme_button_image.classList.add("animate");
    color_scheme_button_image.src = mode ? "/icons/sun-bright.svg" : "/icons/moon.svg";
    updateColors();
    document.cookie = "mode=" + mode + ";"; // Update the cookie after toggling
}

function updateColors() {
    document.documentElement.className = mode ? "dark-mode" : "light-mode";
}