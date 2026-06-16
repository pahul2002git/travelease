(function () {
    const toggleBtn  = document.getElementById("chatbotToggle");
    const closeBtn   = document.getElementById("chatbotClose");
    const panel      = document.getElementById("chatbotPanel");
    const form       = document.getElementById("chatbotForm");
    const input      = document.getElementById("chatbotInput");
    const messages   = document.getElementById("chatbotMessages");
    const chipsArea  = document.getElementById("chatbotChips");

    if (!toggleBtn || !panel || !form || !input || !messages) return;

    // ── Suggestion chips shown on open ───────────────────────────
    const SUGGESTIONS = [
        "🏖 Show holiday packages",
        "✈️ Cheapest flights",
        "🚆 Book a train",
        "🚌 Bus options",
        "💰 Packages under ₹15,000",
        "🌟 Top recommended trips",
    ];

    // ── Helpers ───────────────────────────────────────────────────
    function now() {
        return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    }

    function escapeHtml(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
    }

    /**
     * Render simple markdown-ish formatting in bot replies:
     *  **bold**, *italic*, bullet lines starting with - or •
     */
    function formatBotText(text) {
        // Escape first, then apply formatting
        let html = escapeHtml(text);
        // Bold
        html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
        // Italic
        html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");
        // Lines starting with - or • become bullet items
        html = html.replace(/^[-•] (.+)$/gm, '<span class="chat-bullet">• $1</span>');
        return html;
    }

    // ── Add Message Bubble ────────────────────────────────────────
    function addMessage(role, text) {
        if (role === "bot") {
            const row = document.createElement("div");
            row.className = "chatbot-bot-row";

            const icon = document.createElement("div");
            icon.className = "chatbot-bot-icon";
            icon.innerHTML = "✈";

            const bubble = document.createElement("div");
            bubble.className = "chatbot-message bot";
            bubble.innerHTML = formatBotText(text) +
                `<span class="msg-time">${now()}</span>`;

            row.appendChild(icon);
            row.appendChild(bubble);
            messages.appendChild(row);
        } else {
            const bubble = document.createElement("div");
            bubble.className = "chatbot-message user";
            bubble.innerHTML = escapeHtml(text) +
                `<span class="msg-time">${now()}</span>`;
            messages.appendChild(bubble);
        }
        messages.scrollTop = messages.scrollHeight;
    }

    // ── Typing Indicator ──────────────────────────────────────────
    let typingEl = null;

    function showTyping() {
        if (typingEl) return;
        typingEl = document.createElement("div");
        typingEl.className = "chatbot-typing";
        typingEl.innerHTML = `
            <div class="chatbot-bot-icon">✈</div>
            <div class="chatbot-typing-bubble">
                <span></span><span></span><span></span>
            </div>`;
        messages.appendChild(typingEl);
        messages.scrollTop = messages.scrollHeight;
    }

    function hideTyping() {
        if (typingEl) {
            typingEl.remove();
            typingEl = null;
        }
    }

    // ── Suggestion Chips ──────────────────────────────────────────
    function renderChips() {
        if (!chipsArea) return;
        chipsArea.innerHTML = "";
        SUGGESTIONS.forEach(function (label) {
            const chip = document.createElement("button");
            chip.type = "button";
            chip.className = "chatbot-chip";
            chip.textContent = label;
            chip.addEventListener("click", function () {
                // Strip emoji prefix for message
                const clean = label.replace(/^[\p{Emoji}\s]+/u, "").trim();
                sendMessage(clean);
                hideChips();
            });
            chipsArea.appendChild(chip);
        });
    }

    function hideChips() {
        if (chipsArea) chipsArea.innerHTML = "";
    }

    // ── Open / Close ──────────────────────────────────────────────
    toggleBtn.addEventListener("click", function () {
        const isOpen = panel.classList.toggle("is-open");
        if (isOpen) {
            renderChips();
            setTimeout(function () { input.focus(); }, 120);
        } else {
            hideChips();
        }
    });

    if (closeBtn) {
        closeBtn.addEventListener("click", function () {
            panel.classList.remove("is-open");
            hideChips();
        });
    }

    // ── Send Message ──────────────────────────────────────────────
    async function sendMessage(text) {
        if (!text) return;
        hideChips();
        addMessage("user", text);
        showTyping();

        // Simulate realistic min-delay so typing indicator is visible
        const minDelay = new Promise(function (res) { setTimeout(res, 700); });

        try {
            const [response] = await Promise.all([
                fetch("/chatbot/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: text }),
                }),
                minDelay,
            ]);

            const data = await response.json();
            hideTyping();
            addMessage("bot", data.reply || "I'm sorry, I couldn't process that. Please try again.");
        } catch (err) {
            hideTyping();
            addMessage("bot", "Our assistant is temporarily unavailable. Please try again shortly.");
        }
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        input.value = "";
        sendMessage(text);
    });

    // Allow Enter to submit but Shift+Enter for newline (if textarea used in future)
    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            form.dispatchEvent(new Event("submit"));
        }
    });
})();
