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

// Create the color scheme media query, checking for a dark preference
let color_scheme_query = window.matchMedia("(prefers-color-scheme: dark)");

// Depending on whether the query matches, we set the "mode" variable.
// false = light mode
// true = dark mode
let mode = color_scheme_query.matches;

let site_mode_set = false;
color_scheme_query.addEventListener("change", function (){
    if (!site_mode_set) { 
        toggleColorScheme();
    }
});

document.addEventListener("DOMContentLoaded", function() {
    document.documentElement.className = mode ? "dark-mode" : "light-mode";

    let color_scheme_button = document.getElementById("color-scheme-button");
    color_scheme_button.hidden = false;
    color_scheme_button.addEventListener("click", function(){
        site_mode_set = true;
        toggleColorScheme();
    });

    let color_scheme_button_image = document.getElementById("color-scheme-button-image");
    color_scheme_button_image.src = mode ? "icons/sun-bright.svg" : "icons/moon.svg";

    // When the animation is over, we want to ensure that the style class responsible for animating
    // it is removed.
    color_scheme_button_image.addEventListener("animationend", function() {
        color_scheme_button_image.classList.remove("animate");
    });
});

function toggleColorScheme () {
    mode = !mode;
    updateColors();

    let color_scheme_button_image = document.getElementById("color-scheme-button-image");
    color_scheme_button_image.classList.add("animate");
    color_scheme_button_image.src = mode ? "icons/sun-bright.svg" : "icons/moon.svg";
}

function updateColors () {
    document.documentElement.className = mode ? "dark-mode" : "light-mode";
}