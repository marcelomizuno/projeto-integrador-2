const toggleButton = document.getElementById('toggle-theme');
const body = document.body;

// Verifica se o modo escuro está armazenado no localStorage
if (localStorage.getItem('white-mode') === 'true') {
  body.classList.add('white-mode');
  toggleButton.textContent = 'Ativar Modo Claro';
}

// Função para alternar entre os modos
toggleButton.addEventListener('click', () => {
  body.classList.toggle('white-mode');
  // Armazena a preferência do usuário no localStorage
  const isDarkMode = body.classList.contains('white-mode');
  localStorage.setItem('white-mode', isDarkMode);

  // Atualiza o texto do botão
  toggleButton.textContent = isDarkMode ? 'Ativar Modo Escuro' : 'Ativar Modo Claro';
});