// form.js
const form = document.getElementById('apiForm');
const successMessage = document.getElementById('success-message');

form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams(data)
        });

        if (response.ok) {
            form.reset(); // Formu temizle
            successMessage.style.display = 'block'; // Başarı mesajını göster
            setTimeout(() => {
                successMessage.style.display = 'none'; // Bir süre sonra mesajı gizle
            }, 3000); // 3 saniye sonra gizle
        } else {
            console.error("Kaydetme işlemi başarısız oldu.");
        }
    } catch (error) {
        console.error("Bir hata oluştu: ", error);
    }
});
