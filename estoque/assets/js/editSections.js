document.addEventListener('DOMContentLoaded', function() {
    editSections('dashboard'); 
});


function editSections(section) {
    
    const sections = document.querySelectorAll('.section');
    sections.forEach(function(sec) {
        sec.classList.remove('active-section');
    });
    
    const menuLinks = document.querySelectorAll('.menu-link');
    menuLinks.forEach(function(link) {
        link.classList.remove('active');
    });

    document.getElementById('section-' + section).classList.add('active-section');
    document.getElementById(section).classList.add('active');
   
}