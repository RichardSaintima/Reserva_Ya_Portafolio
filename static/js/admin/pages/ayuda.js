document.addEventListener('DOMContentLoaded', function() {
    const faqItems = document.querySelectorAll('.faq_item');

    faqItems.forEach(item => {
        item.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    });
    
});
