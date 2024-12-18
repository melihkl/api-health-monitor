const fileForm = document.getElementById("fileFormId")
const fileSuccessMessage = document.getElementById("file-success-message");

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
