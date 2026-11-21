
/* LISTA DE PRODUTOS */

const produtos = [

    {
        id: 1,
        nome: "Pomada Modeladora",
        categoria: "Pomadas",
        descricao: "Fixação forte com efeito matte.",
        preco: 49.90,
        icone: "🧴"
    },

    {
        id: 2,
        nome: "Cera Capilar",
        categoria: "Ceras",
        descricao: "Modelagem e definição dos fios.",
        preco: 39.90,
        icone: "💈"
    },

    {
        id: 3,
        nome: "Shampoo Masculino",
        categoria: "Shampoos",
        descricao: "Limpeza e hidratação capilar.",
        preco: 44.90,
        icone: "🧴"
    },

    {
        id: 4,
        nome: "Tônico Capilar",
        categoria: "Tratamentos",
        descricao: "Cuidado com o couro cabeludo.",
        preco: 59.90,
        icone: "🧪"
    },

    {
        id: 5,
        nome: "Pasta Modeladora",
        categoria: "Pomadas",
        descricao: "Controle e acabamento natural.",
        preco: 45.90,
        icone: "🧴"
    },

    {
        id: 6,
        nome: "Óleo para Barba",
        categoria: "Barba",
        descricao: "Hidratação e cuidado para barba.",
        preco: 34.90,
        icone: "🧔"
    },

    {
        id: 7,
        nome: "Shampoo Antiqueda",
        categoria: "Shampoos",
        descricao: "Limpeza para os cuidados capilares.",
        preco: 54.90,
        icone: "🧴"
    },

    {
        id: 8,
        nome: "Máscara Capilar",
        categoria: "Tratamentos",
        descricao: "Hidratação e cuidado dos fios.",
        preco: 64.90,
        icone: "🫙"
    },

    {
        id: 9,
        nome: "Cera Efeito Matte",
        categoria: "Ceras",
        descricao: "Acabamento natural e modelagem.",
        preco: 42.90,
        icone: "💈"
    }

];


/* CARRINHO */

let carrinho = [];


/* MOSTRAR PRODUTOS */

function mostrarProdutos(lista = produtos) {

    const area = document.getElementById("lista-produtos");

    area.innerHTML = "";

    if (lista.length === 0) {

        area.innerHTML = `
            <p class="sem-produtos">
                Nenhum produto encontrado.
            </p>
        `;

        return;
    }

    lista.forEach(produto => {

        area.innerHTML += `

            <div class="produto">

                <div class="produto-icone">
                    ${produto.icone}
                </div>

                <p class="categoria-produto">
                    ${produto.categoria}
                </p>

                <h3>${produto.nome}</h3>

                <p class="produto-descricao">
                    ${produto.descricao}
                </p>

                <p class="preco">
                    R$ ${produto.preco.toFixed(2).replace(".", ",")}
                </p>

                <button onclick="adicionarCarrinho(${produto.id})">
                    ADICIONAR AO CARRINHO
                </button>

            </div>

        `;

    });

}


/* FILTRAR CATEGORIAS */

function filtrar(categoria) {

    if (categoria === "Todos") {

        mostrarProdutos();

    } else {

        const resultado = produtos.filter(produto => {

            return produto.categoria === categoria;

        });

        mostrarProdutos(resultado);

    }

}


/* ADICIONAR AO CARRINHO */

function adicionarCarrinho(id) {

    const produto = produtos.find(item => item.id === id);

    if (produto) {

        carrinho.push(produto);

        atualizarContador();

        alert(produto.nome + " foi adicionado ao carrinho!");

    }

}


/* ATUALIZAR CONTADOR */

function atualizarContador() {

    document.getElementById("contador").textContent =
        carrinho.length;

}


/* VISUALIZAR CARRINHO */

function verCarrinho() {

    if (carrinho.length === 0) {

        alert("Seu carrinho está vazio!");

        return;

    }

    let total = 0;

    let mensagem = "SEU CARRINHO:\n\n";

    carrinho.forEach(produto => {

        mensagem += produto.nome + " - R$ " +
            produto.preco.toFixed(2).replace(".", ",") + "\n";

        total += produto.preco;

    });

    mensagem += "\nTOTAL: R$ " +
        total.toFixed(2).replace(".", ",");

    alert(mensagem);

}


/* INICIAR LOJA */

mostrarProdutos();
