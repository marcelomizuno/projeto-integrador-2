document.getElementById("dropdownButton").onclick = showMenu;

function showMenu(){
   document.getElementById("dropdown-content").classList.toggle("show");
}

window.onclick = function(event) {
    // Verifica se o clique foi fora do botão
    if (!event.target.matches('#dropdownButton')) {
        var dropdown = document.getElementById("dropdown-content");
        if (dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
}

