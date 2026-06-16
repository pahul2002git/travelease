(function () {
    const section = document.getElementById('spin-wheel-offers');
    if (!section) {
        return;
    }

    const spinEndpoint = section.dataset.spinEndpoint || '/offers/spin';
    const openBtn = document.getElementById('openSpinWheel');
    const modal = document.getElementById('spinWheelModal');
    const closeBackdrop = document.getElementById('closeSpinWheel');
    const closeBtn = document.getElementById('closeSpinWheelBtn');
    const spinBtn = document.getElementById('spinWheelTrigger');
    const resultBox = document.getElementById('spinWheelResult');
    const statusCard = document.getElementById('spinOfferStatus');
    const wheelCanvas = document.getElementById('offerWheelCanvas');
    if (!openBtn || !modal || !closeBackdrop || !closeBtn || !spinBtn || !resultBox || !statusCard || !wheelCanvas) {
        return;
    }

    const segments = [
        { id: 'offer_5', label: '5% OFF', color: '#00D2FF' },
        { id: 'offer_10', label: '10% OFF', color: '#2DE1C2' },
        { id: 'offer_0_a', label: 'Try Again', color: '#7A7D9D' },
        { id: 'offer_12', label: '12% OFF', color: '#FFD166' },
        { id: 'offer_7', label: '7% OFF', color: '#53A3FF' },
        { id: 'offer_20', label: '20% OFF', color: '#FF6B6B' },
        { id: 'offer_0_b', label: 'No Offer', color: '#7A7D9D' },
        { id: 'offer_15', label: '15% OFF', color: '#C18CFF' }
    ];

    const canvasCtx = wheelCanvas.getContext('2d');
    let currentRotation = 0;
    let spinning = false;

    function drawWheel() {
        const size = wheelCanvas.width;
        const center = size / 2;
        const radius = center - 16;
        const arc = (Math.PI * 2) / segments.length;
        canvasCtx.clearRect(0, 0, size, size);

        segments.forEach((segment, index) => {
            const start = -Math.PI / 2 + index * arc;
            const end = start + arc;
            canvasCtx.beginPath();
            canvasCtx.moveTo(center, center);
            canvasCtx.arc(center, center, radius, start, end);
            canvasCtx.closePath();
            canvasCtx.fillStyle = segment.color;
            canvasCtx.fill();

            canvasCtx.save();
            canvasCtx.translate(center, center);
            canvasCtx.rotate(start + arc / 2);
            canvasCtx.textAlign = 'right';
            canvasCtx.fillStyle = '#FFFFFF';
            canvasCtx.font = '700 16px Poppins, sans-serif';
            canvasCtx.fillText(segment.label, radius - 18, 6);
            canvasCtx.restore();
        });

        canvasCtx.beginPath();
        canvasCtx.arc(center, center, radius + 1, 0, Math.PI * 2);
        canvasCtx.lineWidth = 6;
        canvasCtx.strokeStyle = 'rgba(255,255,255,0.45)';
        canvasCtx.stroke();
    }

    function showModal() {
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
    }

    function hideModal() {
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
    }

    function getTargetIndex(offerId) {
        const index = segments.findIndex((item) => item.id === offerId);
        return index >= 0 ? index : 0;
    }

    function updateStatusCard(offer) {
        const discount = Number(offer.discount || 0);
        const used = Boolean(offer.used);
        statusCard.dataset.offerId = offer.offer_id || '';
        statusCard.dataset.offerLabel = offer.label || '';
        statusCard.dataset.offerDiscount = String(discount);
        statusCard.dataset.offerCode = offer.code || '';
        statusCard.dataset.offerUsed = used ? 'true' : 'false';

        if (discount > 0 && !used) {
            statusCard.innerHTML = `
                <span class="spin-offer-badge active">Unlocked</span>
                <h3>${offer.label}</h3>
                <p>Code: <strong>${offer.code}</strong> | Apply on package checkout</p>
            `;
            return;
        }
        if (discount > 0 && used) {
            statusCard.innerHTML = `
                <span class="spin-offer-badge used">Used</span>
                <h3>${offer.label}</h3>
                <p>Code <strong>${offer.code}</strong> was already redeemed today.</p>
            `;
            return;
        }
        statusCard.innerHTML = `
            <span class="spin-offer-badge neutral">Completed</span>
            <h3>${offer.label || 'No Offer'}</h3>
            <p>Come back tomorrow for another spin.</p>
        `;
    }

    function renderResult(offer) {
        const discount = Number(offer.discount || 0);
        if (discount > 0) {
            resultBox.innerHTML = `
                <h4>${offer.label} Unlocked</h4>
                <p>Coupon: <strong>${offer.code}</strong></p>
                <p>Use this offer during package checkout today.</p>
            `;
            return;
        }
        resultBox.innerHTML = `
            <h4>${offer.label || 'No Offer This Time'}</h4>
            <p>No discount this round. Come back tomorrow and spin again.</p>
        `;
    }

    function renderExistingResultFromDataset() {
        const offerId = statusCard.dataset.offerId || '';
        if (!offerId) {
            resultBox.innerHTML = '<p>Press start to reveal your offer.</p>';
            return;
        }
        renderResult({
            offer_id: offerId,
            label: statusCard.dataset.offerLabel || '',
            discount: Number(statusCard.dataset.offerDiscount || 0),
            code: statusCard.dataset.offerCode || '',
            used: statusCard.dataset.offerUsed === 'true'
        });
    }

    function spinToOffer(offerId, alreadySpun) {
        const segmentAngle = 360 / segments.length;
        const index = getTargetIndex(offerId);
        const centerAngle = -90 + (index + 0.5) * segmentAngle;
        let baseStop = (270 - centerAngle) % 360;
        if (baseStop < 0) {
            baseStop += 360;
        }
        const jitter = (Math.random() - 0.5) * segmentAngle * 0.45;
        const turns = alreadySpun ? 2 : 7;
        const spinDistance = turns * 360 + baseStop + jitter;

        currentRotation += spinDistance;
        const duration = alreadySpun ? 1800 : 5600;
        wheelCanvas.style.transition = `transform ${duration}ms cubic-bezier(0.15, 0.9, 0.2, 1)`;
        wheelCanvas.style.transform = `rotate(${currentRotation}deg)`;
        return duration;
    }

    async function triggerSpin() {
        if (spinning) {
            return;
        }
        spinning = true;
        spinBtn.disabled = true;
        spinBtn.textContent = 'Spinning...';
        resultBox.innerHTML = '<p>Calculating your reward...</p>';

        try {
            const response = await fetch(spinEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            if (!response.ok || data.status !== 'ok') {
                throw new Error('Unable to spin right now.');
            }

            const duration = spinToOffer(data.offer_id, Boolean(data.already_spun));
            window.setTimeout(function () {
                updateStatusCard(data);
                renderResult(data);
                spinBtn.textContent = 'View Offer';
                spinBtn.disabled = false;
                spinning = false;
            }, duration + 120);
        } catch (error) {
            resultBox.innerHTML = '<p>Something went wrong. Please try again.</p>';
            spinBtn.textContent = 'Start Spin';
            spinBtn.disabled = false;
            spinning = false;
        }
    }

    openBtn.addEventListener('click', function () {
        showModal();
        renderExistingResultFromDataset();
    });
    closeBackdrop.addEventListener('click', hideModal);
    closeBtn.addEventListener('click', hideModal);
    spinBtn.addEventListener('click', triggerSpin);
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            hideModal();
        }
    });

    drawWheel();
})();
