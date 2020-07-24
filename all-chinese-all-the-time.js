// ==UserScript==
// @name         All Chinese All the time
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Removes any YouTube videos from the feed that do not contain Chinese characters, for maximum learning immersion.
// @author       You
// @match        https://www.youtube.com/
// @exclude      https://www.youtube.com/feed/subscriptions
// @exclude      https://www.youtube.com/results
// @grant        none
// ==/UserScript==

// Regex that matchs strings Chinese characters.
let removeFilterRegex = /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]/;
let pollIntervalMs = 1000;
let disablePlaylists = false;

(function() {
    setInterval(() => {
        if (window.location.href.length <= 0) {
            return;
        }

        if (window.location.href.indexOf("watch") > 0) {
            WatchPageFilter();
        }
        else {
            MainPageFilter();
        }

    }, pollIntervalMs);
})();

function ElementsWithChinese() {
    return Array.from(document.querySelectorAll('#video-title'))
        .filter(item =>
                item.innerHTML.trim().match(removeFilterRegex) == null
                || (disablePlaylists && item.innerHTML.trim().indexOf('合辑') > -1));
}

function MainPageFilter() {
    ElementsWithChinese()
        .forEach(item => { item.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.style.display = "None" });
}

function WatchPageFilter() {
    ElementsWithChinese()
        .forEach(item => { item.parentNode.parentNode.parentNode.parentNode.parentNode.style.display = "None" });
}