//header
document
  .getElementById("home-link")
  .addEventListener("click", function (event) {
    event.preventDefault();
    window.location.href = "/home";
  });

document
  .getElementById("person-link")
  .addEventListener("click", function (event) {
    event.preventDefault();
    window.location.href = "/perfuser";
  });

document
  .getElementById("logout-link")
  .addEventListener("click", function (event) {
    event.preventDefault();

    fetch("/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action: "logout" }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          window.location.href = "/login";
        }
      })
      .catch((error) => {
        console.error("Erro ao fazer logout:", error);
      });
  });

//index
const slides = document.querySelectorAll(".swiper-slide");
let currentIndex = 0;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle("active", i === index);
  });
}

//home
document.addEventListener("DOMContentLoaded", function () {
  const openPostFormButton = document.getElementById("open-post-form");
  const postFormContainer = document.getElementById("post-form");
  const closePostFormButton = document.getElementById("close-post-form");

  openPostFormButton.addEventListener("click", function () {
    postFormContainer.style.display = "block";
  });

  closePostFormButton.addEventListener("click", function () {
    postFormContainer.style.display = "none";
  });
});

//register
document
  .getElementById("formregister")
  .addEventListener("submit", function (event) {
    var senha = document.getElementById("rsenha").value;
    var confirmarSenha = document.getElementById("rconfirmarsenha").value;

    if (senha !== confirmarSenha) {
      event.preventDefault();
      alert("As senhas não coincidem. Por favor, verifique.");
    }
  });

//login
document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    var email = document.getElementById("lemail").value;
    var senha = document.getElementById("lsenha").value;

    if (!email || !senha) {
      event.preventDefault();
      alert("Por favor, preencha todos os campos.");
    }
  });

document.getElementById("prevBtn").addEventListener("click", () => {
  currentIndex = currentIndex > 0 ? currentIndex - 1 : slides.length - 1;
  showSlide(currentIndex);
});

document.getElementById("nextBtn").addEventListener("click", () => {
  currentIndex = currentIndex < slides.length - 1 ? currentIndex + 1 : 0;
  showSlide(currentIndex);
});

showSlide(currentIndex);
