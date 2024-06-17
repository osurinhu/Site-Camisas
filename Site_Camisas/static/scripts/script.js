function qtdcart(id) {

    formas = document.getElementById(id)

    console.log("jesus")

    const formData = new FormData(formas)

    fetch("/cartadd", {

        method: 'post',
        body: formData

    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
        .then(data => {
            // Código para lidar com a resposta de sucesso
            const msgHeader = document.getElementById('msg-cart');
            msgHeader.innerHTML += '<p class="msg"> Carrinho atualizado! </p>';

            setTimeout(
                function () {
                    msgHeader.innerHTML = '';
                }, 2000)
        })
        .catch(error => {
            // Código para lidar com o erro na requisição
            window.location.replace("/entrar");
        });
}






function favadd(id) {

    formas = document.getElementById(id)

    console.log("jesus")

    const formData = new FormData(formas)

    fetch("/favadd", {

        method: 'post',
        body: formData

    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
        .then(data => {
            // Código para lidar com a resposta de sucesso
            const msgHeader = document.getElementById('msg-cart');
            msgHeader.innerHTML += '<p class="msg"> Favoritos atualizado! </p>';

            setTimeout(
                function () {
                    msgHeader.innerHTML = '';
                }, 2000)


        })
        .catch(error => {
            // Código para lidar com o erro na requisição
            window.location.replace("/entrar");
        });
}
