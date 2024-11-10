document.addEventListener('DOMContentLoaded', function() {
  
  const menuLinks = document.querySelectorAll('.menu-link');

  menuLinks.forEach(link => {
      link.addEventListener('click', function(event) {
         
          event.preventDefault(); 
          menuLinks.forEach(link => link.classList.remove('active'));         
          this.classList.add('active');
      });
  });
});