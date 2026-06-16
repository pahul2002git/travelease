(function () {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduceMotion) return;

    const clickableSelector = ".btn, .apply-btn, button, input[type='submit'], input[type='button'], .chatbot-toggle";
    document.addEventListener("pointerdown", function (event) {
        const target = event.target.closest(clickableSelector);
        if (!target) return;

        const rect = target.getBoundingClientRect();
        const ripple = document.createElement("span");
        const size = Math.max(rect.width, rect.height);

        ripple.className = "click-ripple";
        ripple.style.width = size + "px";
        ripple.style.height = size + "px";
        ripple.style.left = event.clientX - rect.left - size / 2 + "px";
        ripple.style.top = event.clientY - rect.top - size / 2 + "px";

        target.appendChild(ripple);
        window.setTimeout(function () {
            ripple.remove();
        }, 600);
    });
})();
