//const openModalButtons = document.querySelectorAll(".open-modal"); 
//const closeModalButtons = document.querySelectorAll(".close-modal");
//const modals = document.querySelectorAll(".modal");
const fade = document.querySelector(".fade"); 

const toggleModal = (modal) => {
    modal.classList.toggle("hide");
    fade.classList.toggle("hide"); // Usa o mesmo fade para todos os modais

    if( !modal.classList.contains("hide") ) {
        modal.querySelector(".close-modal").addEventListener("click", () => toggleModal(modal));
        fade.addEventListener("click", () => toggleModal(modal));
    }
};
/*
openModalButtons.forEach((button, index) => {
    const modal = modals[index];
    
    button.addEventListener("click", () => toggleModal(modal));
});

closeModalButtons.forEach((button, index) => {
    const modal = modals[index];
    
    button.addEventListener("click", () => toggleModal(modal));
});

// Fecha o modal ao clicar no fade
fade.addEventListener("click", () => {
    // Fecha qualquer modal aberto
    modals.forEach((modal) => {
        if (!modal.classList.contains("hide")) {
            toggleModal(modal);
        }
    });
});
*/