let carrinho = [];
let total = 0;

function adicionarAoCarrinho(item, preco) {
    carrinho.push({ item, preco });
    total += preco;
    atualizarCarrinho();
}

function atualizarCarrinho() {
    const listaCarrinho = document.getElementById('lista-carrinho');
    listaCarrinho.innerHTML = '';
    carrinho.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.item} - R$ ${item.preco.toFixed(2)}`;
        listaCarrinho.appendChild(li);
    });
    document.getElementById('total-carrinho').textContent = total.toFixed(2);
}

function mostrarCarrinho() {
    atualizarCarrinho();
    document.getElementById('modal-carrinho').style.display = 'flex';
}

function fecharModal() {
    document.getElementById('modal-carrinho').style.display = 'none';
    document.getElementById('modal-pagamento').style.display = 'none';
}

function mostrarPagamento() {
    document.getElementById('modal-pagamento').style.display = 'flex';
}

function efetuarPagamento() {
    const formaPagamento = document.getElementById('forma-pagamento').value;

    // Aqui você pode adicionar a lógica de pagamento, como enviar os dados para um servidor
    alert(`Pagamento realizado com sucesso!\nForma de Pagamento: ${formaPagamento}`);

    carrinho = [];
    total = 0;
    atualizarCarrinho();
    fecharModal();
}
