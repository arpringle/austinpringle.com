/*
 *
 *  Filename: script.js
 *
 *  Description: JavaScript for austinpringle.com
 *
 *  Author: Copyright 2024 Austin Pringle
 *
 *  This program is free software: you can redistribute it and/or modify it under the terms of the
 *  GNU General Public License as published by the Free Software Foundation, either version 3 of
 *  the License, or (at your option) any later version.
 *
 */


/*
 * The JavaScript and CSS files that make up this site are designed such that everything should
 * still work on a machine with JavaScript disabled. One major hurdle to this goal, however, is
 * handling user color scheme preferences.
 * 
 * The latest CSS standard supports media queries for color schemes. These queries can either be
 * written as event listeners from the JavaScript side, or embedded directly into the stylesheet.
 * Embedding them into the stylesheet is the best option if you want your site to support color
 * schemes even in non-JavaScript environments.
 * 
 * However, if you embed the media queries into the CSS, then you have to solve some interesting
 * problems on the JavaScript side if you want to allow for manual theme switching. You essentially
 * have to manually override a lot of CSS properties.
 * 
 * While reading this code, remember that the default state is set directly by the stylesheet.
 */

// Create the color scheme media query, checking for a dark preference
let color_scheme_query = window.matchMedia("(prefers-color-scheme: dark)");

// Depending on whether the query matches, we set the "mode" variable.
// false = light mode
// true = dark mode
let mode = color_scheme_query.matches;

// If the user just so happens to change their system's color preference whilst on the web page,
// we want to account for that. This is actually somewhat common, because many modern devices
// provide the ability to automatically change color preference based on the time of day.
// The default behavior of the media query in the stylesheet does actually handle this.
// However, we have to redundantly handle it here because, if we don't, the icon on the button
// to toggle the color scheme will get out of sync from the actual color scheme. Along with all of
// these considerations, we also explicitly do NOT want to follow a change in the user's
// preferences if they have already changed the color scheme via the toggle button, as this would
// be quite annoying. Therefore, we declare a flag to see if the site's mode has been set by the
// user. If it has not been set, then we will follow the system's changing color schemes by setting
// up the following event listener.
let site_mode_set = false;
color_scheme_query.addEventListener("change", function (){
    if (!site_mode_set) { 
        toggleColorScheme();
    }
});

document.addEventListener("DOMContentLoaded", function() {
    let header_right_span = document.getElementById("header-right-span");

    // The reason we create this element from JavaScript is because it allows the toggle button to
    // essentially not exist if the user is not using JavaScript, which is better than a button
    // which does not work.
    let color_scheme_button = document.createElement("button");
    color_scheme_button.id = "color-scheme-button";
    color_scheme_button.title = "Toggle Dark Mode";
    color_scheme_button.addEventListener("click", function(){
        site_mode_set = true;
        toggleColorScheme();
    });

    let color_scheme_button_image = document.createElement("img");
    color_scheme_button_image.src = mode ? "icons/sun-bright.svg" : "icons/moon.svg";
    color_scheme_button_image.id = "color-scheme-button-image";
    color_scheme_button_image.className = "social-icon";

    // The "toggleColorScheme" function adds a nice spin animation style class to the button icon.
    // This event listener allows us to more easily time the transition of the toggle button icon
    // to the animation.
    //
    // `await new Promise(r => setTimeout(r, 250));` is just a way to sleep for 0.25s, however, to
    // use it, the closure must be marked as `async`.
    // TODO: perhaps find a better way to achieve this.
    // There's a bug in
    color_scheme_button_image.addEventListener("animationstart", async function() {
        await new Promise(r => setTimeout(r, 250));
        color_scheme_button_image.src = mode ? "icons/sun-bright.svg" : "icons/moon.svg";
    });

    // When the animation is over, we want to ensure that the style class responsible for animating
    // it is removed.
    color_scheme_button_image.addEventListener("animationend", function() {
        color_scheme_button_image.classList.remove("animate");
    });

    color_scheme_button.append(color_scheme_button_image);
    header_right_span.prepend(color_scheme_button);
});


function toggleColorScheme () {
    mode = !mode;
    updateColors();

    // A listener on the image is responsible for transitioning the icon
    let color_scheme_button_image = document.getElementById("color-scheme-button-image");
    color_scheme_button_image.classList.add("animate");
}

// This code replicates exactly the changes of the media queries in the stylesheet.
function updateColors () {

    const bg = mode ? "black" : "white";
    const txt = mode ? "white" : "black";
    const border = mode ? "rgb(23, 23, 23)" : "rgb(225, 225, 225)";
    const filter = mode ? "invert()" : "inherit";

    document.documentElement.style.setProperty('--bg', bg);
    document.documentElement.style.setProperty('--txt', txt);
    document.documentElement.style.setProperty('--border', border);

    const icons = document.getElementsByClassName("social-icon");
    for (let i = 0; i < icons.length; i++) {
        icons[i].style.setProperty("filter", filter);
    }
}