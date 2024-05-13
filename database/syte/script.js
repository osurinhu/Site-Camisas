let carrinho = [];
let total = 0;

function adicionarAoCarrinho(item, preco, imagemId) {
    carrinho.push({ item, preco });
    total += preco;
    atualizarCarrinho();
    adicionarDestaque(imagemId);
}

function atualizarCarrinho() {
    const listaCarrinho = document.getElementById('lista-carrinho');
    listaCarrinho.innerHTML = '';
    carrinho.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.item} - R$ ${item.preco.toFixed(2)}`;
        listaCarrinho.appendChild(li);
    });
}

function mostrarCarrinho() {
    atualizarCarrinho();
    document.getElementById('modal-carrinho').style.display = 'flex';
    document.getElementById('div-registro').style.display = 'block';
}

function fecharModal() {
    document.getElementById('modal-carrinho').style.display = 'none';
    document.getElementById('div-registro').style.display = 'none';
    document.getElementById('div-pagamento').style.display = 'none';
}

function verificarRegistro() {
    const nome = document.getElementById('nome').value;
    const telefone = document.getElementById('telefone').value;
    const cep = document.getElementById('cep').value;
    const email = document.getElementById('email').value;

    if (nome && telefone && cep && email) {
        document.getElementById('div-registro').style.display = 'none';
        document.getElementById('div-pagamento').style.display = 'block';

        // Verifica se o CEP contém "Patos de Minas" (ignorando diferenças de maiúsculas/minúsculas)
        if (cep.toLowerCase().includes('patos de minas')) {
            calcularTaxaEntrega(0); // Taxa de entrega zero se o CEP for de Patos de Minas
        } else {
            calcularTaxaEntrega(calcularDistanciaKm(cep));
        }
    } else {
        alert('Por favor, preencha todos os campos do registro.');
    }
}

function efetuarPagamento() {
    const formaPagamento = document.getElementById('forma-pagamento').value;

    // Calcular valor total considerando a taxa de entrega
    const valorTotal = total + (total * (taxaEntrega / 100));

    // Exibir mensagem com o valor total a ser pago
    alert(`Valor Total a ser Pago (com Taxa de Entrega): R$ ${valorTotal.toFixed(2)}\nForma de Pagamento: ${formaPagamento}`);

    carrinho = [];
    total = 0;
    atualizarCarrinho();
    fecharModal();
}

function calcularDistanciaKm(cep) {
    // Lógica para calcular a distância em km com base no CEP
    // Por questões de simplicidade, vamos simular um valor aleatório entre 1 e 1000
    return Math.floor(Math.random() * 1000) + 1;
}

function calcularTaxaEntrega(distanciaKm) {
    // Calcular taxa de entrega com base na distância em km
    // A cada 100km de distância, aumenta a taxa em 8%
    const taxaBase = 8; // Taxa base de 8%
    const kmPorTaxa = 100; // Cada 100km acrescenta 8% na taxa
    const taxaPorKm = Math.floor(distanciaKm / kmPorTaxa) * taxaBase;
    taxaEntrega = Math.min(taxaPorKm, 100); // Limitar a taxa a 100%
}

