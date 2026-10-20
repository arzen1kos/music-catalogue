class ScrollPicker {

    constructor({ el, input }) {

        this.el = el;
        this.input = input;

        this.currentYear = new Date().getFullYear();

        this.selectedYear = this.currentYear;

        this.minYear = 1950;
        this.maxYear = this.currentYear;

        this.yearEl = this.el.querySelector('.year');

        this.render();
        this.attachEvents();
    }

    attachEvents() {

        let locked = false;
    
        this.yearEl.addEventListener('wheel', (e) => {
    
            e.preventDefault();
    
            if (locked) return;
    
            locked = true;
    
            if (e.deltaY > 0) {
                this.selectedYear--;
            } else {
                this.selectedYear++;
            }
    
            if (this.selectedYear < this.minYear) {
                this.selectedYear = this.minYear;
            }
    
            if (this.selectedYear > this.maxYear) {
                this.selectedYear = this.maxYear;
            }
    
            this.render();
    
            setTimeout(() => {
                locked = false;
            }, 390);
        });
    }

    render() {

        this.yearEl.innerHTML = '';

        const years = [
            this.selectedYear + 2,
            this.selectedYear + 1,
            this.selectedYear,
            this.selectedYear - 1,
            this.selectedYear - 2
        ];

        years.forEach((year, index) => {

            const button = document.createElement('button');

            button.textContent = year;

            if (index === 2) {
                button.classList.add('selected');

                if (this.input) {
                    this.input.value = year;
                }

            } else {
                button.classList.add('faded');
            }

            this.yearEl.appendChild(button);
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {

    const el = document.querySelector('#scroll-picker');
    const input = document.querySelector('#id_release_year');

    if (el && input) {
        new ScrollPicker({ el, input });
    }
});