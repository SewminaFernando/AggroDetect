// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

document.addEventListener('DOMContentLoaded', function () {
  const chatbotButton = document.getElementById('chatbotButton');
  const chatContainer = document.getElementById('chatContainer');

  chatbotButton.addEventListener('click', function () {
      if (chatContainer.style.display === 'none') {
          chatContainer.style.display = 'block';
          chatbotButton.innerHTML = '<i class="bx bx-phone-off"></i>';
      } else {
          chatContainer.style.display = 'none';
          chatbotButton.innerHTML = '<i class="bx bx-phone"></i>';
      }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const recordButton = document.querySelector('.record-button');

  recordButton.addEventListener('mousedown', function () {
      recordButton.classList.add('pressed');
  });

  recordButton.addEventListener('mouseup', function () {
      recordButton.classList.remove('pressed');
  });
});

