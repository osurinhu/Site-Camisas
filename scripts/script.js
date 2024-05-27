function toggleFavorite(button) {
    button.classList.toggle('active');
    const icon = button.querySelector('.favorite-icon');
    if (button.classList.contains('active')) {
        icon.innerHTML = '&#9829;'; // Código do coração preenchido
    } else {
        icon.innerHTML = '&#9825;'; // Código do coração vazio
    }
}

function addToCart(button) {
    button.classList.toggle('active');
    const icon = button.querySelector('.cart-icon');
    if (button.classList.contains('active')) {
        icon.innerHTML = '&#128722;'; // Código do carrinho preenchido
        // Adicionar lógica para adicionar ao carrinho
    } else {
        icon.innerHTML = '&#128722;'; // Código do carrinho padrão
        // Adicionar lógica para remover do carrinho
    }
}