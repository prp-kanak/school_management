/** @odoo-module **/

console.log('Script Loaded'); // Debugging log

setTimeout(() => {
    const studentCards = document.querySelectorAll('.student-card');

    // Add d-none class to all cards
    studentCards.forEach(card => {
        card.classList.add('d-none');
    });

    const container = document.querySelector('.container.my-5');
    if (!container) {
        console.error('Container not found!');
        return;
    }


    // Create and add a toggle button
    const toggleButton = document.createElement('button');
    toggleButton.textContent = 'Show/Hide Students';
    toggleButton.classList.add('btn', 'btn-secondary', 'mt-3');
    container.prepend(toggleButton);

    toggleButton.addEventListener('click', () => {
        studentCards.forEach(card => {
            card.classList.toggle('d-none');
        });
    });
}, 500); // Delay by 500ms
