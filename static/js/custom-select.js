(() => {
    const closeAll = () => {
        document.querySelectorAll('.custom-select.open').forEach((el) => el.classList.remove('open'));
    };

    const enhanceSelect = (select) => {
        if (select.dataset.customized === 'true') return;
        select.dataset.customized = 'true';

        const wrapper = document.createElement('div');
        wrapper.className = 'custom-select';

        const trigger = document.createElement('div');
        trigger.className = 'custom-select-trigger';
        trigger.textContent = select.options[select.selectedIndex]?.text || 'Select';

        const options = document.createElement('div');
        options.className = 'custom-select-options';

        Array.from(select.options).forEach((option) => {
            const item = document.createElement('div');
            item.className = 'custom-select-option';
            item.textContent = option.text;
            item.dataset.value = option.value;
            if (option.selected) item.classList.add('is-selected');
            if (option.value === '') item.classList.add('is-placeholder');
            item.addEventListener('click', () => {
                select.value = option.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                trigger.textContent = option.text;
                options.querySelectorAll('.custom-select-option').forEach((opt) => opt.classList.remove('is-selected'));
                item.classList.add('is-selected');
                wrapper.classList.remove('open');
            });
            options.appendChild(item);
        });

        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = wrapper.classList.contains('open');
            closeAll();
            if (!isOpen) wrapper.classList.add('open');
        });

        select.addEventListener('change', () => {
            const selected = select.options[select.selectedIndex]?.text || 'Select';
            trigger.textContent = selected;
        });

        select.parentNode.insertBefore(wrapper, select);
        wrapper.appendChild(select);
        wrapper.appendChild(trigger);
        wrapper.appendChild(options);
    };

    document.addEventListener('click', closeAll);

    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('select.js-custom-select').forEach(enhanceSelect);
    });
})();
