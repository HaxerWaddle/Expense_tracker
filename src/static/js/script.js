const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry);
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        } else {
            entry.target.classList.remove('show');
        }
    });
});

const hidden_items = document.querySelectorAll('.hidden');
hidden_items.forEach((el) => observer.observe(el));

document.addEventListener("DOMContentLoaded", function () {
    const msg = document.getElementById("msg");
    if (msg) {
        setTimeout(() => {
            msg.remove();
        }, 3000);
    }
});
