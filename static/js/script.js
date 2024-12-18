// form.js
const form = document.getElementById("apiForm");
const fileForm = document.getElementById("fileFormId")
const successMessage = document.getElementById("success-message");
const fileSuccessMessage = document.getElementById("file-success-message");

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await fetch("/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams(data),
    });

    if (response.ok) {
      form.reset(); // Formu temizle
      successMessage.style.display = "block"; // Başarı mesajını göster
      setTimeout(() => {
        successMessage.style.display = "none"; // Bir süre sonra mesajı gizle
      }, 3000); // 3 saniye sonra gizle
    } else {
      console.error("Kaydetme işlemi başarısız oldu.");
    }
  } catch (error) {
    console.error("Bir hata oluştu: ", error);
  }
});

fileForm.addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(fileForm);

  try {
    const response = await fetch("/fileSubmit/", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      fileForm.reset();
      fileSuccessMessage.textContent = "Başarı ile dosya yüklendi";
      fileSuccessMessage.style.display = "block"; // Başarı mesajını göster
      setTimeout(() => {
        fileSuccessMessage.style.display = "none"; // Bir süre sonra mesajı gizle
      }, 3000); // 3 saniye sonra gizle
    } else {
      console.error("Kaydetme işlemi başarısız oldu.");
    }
  } catch (error) {
    console.error("Bir hata oluştu: ", error);
  }
});
