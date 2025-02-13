// script.js

// You can add your JavaScript code here

// For example, you can add an event listener to the "Patient Details" link
const patientDetailsLink = document.querySelector('a[href="{% url \'home\' %}"]');

if (patientDetailsLink) {
  patientDetailsLink.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default link behavior
    alert('You clicked on the Patient Details link!');
  });
}

// You can also add a function to change the background color of the navigation bar on hover
const navbar = document.querySelector('.navbar');

if (navbar) {
  navbar.addEventListener('mouseover', () => {
    navbar.style.backgroundColor = '#555';
  });

  navbar.addEventListener('mouseout', () => {
    navbar.style.backgroundColor = '#343a40';
  });
}

// Add any other JavaScript code you want to include in your template