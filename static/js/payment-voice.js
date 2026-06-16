(function () {
    const paymentForms = Array.from(document.querySelectorAll("form[action]")).filter((form) => {
        const action = (form.getAttribute("action") || "").toLowerCase();
        return action.endsWith("/pay") || action.includes("/pay?");
    });

    if (!paymentForms.length || !("speechSynthesis" in window)) {
        return;
    }

    let availableVoices = [];
    const loadVoices = function () {
        availableVoices = window.speechSynthesis.getVoices() || [];
    };

    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;

    function pickCoolVoice() {
        if (!availableVoices.length) return null;
        const preferred = availableVoices.find((v) =>
            /en/i.test(v.lang) && /zira|aria|samantha|female|google us english/i.test(v.name)
        );
        if (preferred) return preferred;
        return availableVoices.find((v) => /en/i.test(v.lang)) || availableVoices[0];
    }

    function speakPaymentLine() {
        try {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(
                "Payment received. Please wait while we secure your booking."
            );
            const voice = pickCoolVoice();
            if (voice) utterance.voice = voice;
            utterance.rate = 1;
            utterance.pitch = 1.05;
            utterance.volume = 1;
            window.speechSynthesis.speak(utterance);
        } catch (e) {
            // Silent fallback to normal submit.
        }
    }

    paymentForms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            if (form.dataset.voiceSubmitted === "1") {
                return;
            }

            event.preventDefault();
            form.dataset.voiceSubmitted = "1";

            const submitButton = form.querySelector("button[type='submit'], input[type='submit']");
            if (submitButton) {
                submitButton.disabled = true;
                if (submitButton.tagName === "BUTTON") {
                    submitButton.dataset.originalText = submitButton.textContent;
                    submitButton.textContent = "Processing...";
                }
            }

            speakPaymentLine();

            window.setTimeout(function () {
                form.submit();
            }, 900);
        });
    });
})();
