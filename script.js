const TELEGRAM_BOT_TOKEN = "8866238346:AAFqgpZclKx0pdqC05ySfRZVek02z4L883I";
const TELEGRAM_CHAT_ID = "-4326152013"; // Exemplo: "@canal_jheny" ou "-100xxxxxxx"

let produtoSelecionado = null;

// Permite buscar pressionando Enter no teclado do celular/computador
document.getElementById('searchInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    buscarProdutos();
  }
});

async function buscarProdutos() {
  const query = document.getElementById('searchInput').value.trim();
  const limit = document.getElementById('limitSelect').value;
  const statusDiv = document.getElementById('statusMessage');
  const resultsGrid = document.getElementById('resultsGrid');

  if (!query) {
    statusDiv.innerText = "Digite o nome de um produto para pesquisar.";
    return;
  }

  statusDiv.innerText = "✨ Buscando as melhores ofertas...";
  resultsGrid.innerHTML = "";

  try {
    const response = await fetch(`https://api.mercadolibre.com/sites/MLB/search?q=${encodeURIComponent(query)}&limit=${limit}`);
    
    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const data = await response.json();
    const produtos = data.results;

    statusDiv.innerText = "";

    if (!produtos || produtos.length === 0) {
      statusDiv.innerText = `Nenhum produto encontrado para "${query}".`;
      return;
    }

    produtos.forEach(prod => {
      const card = document.createElement('div');
      card.className = 'card';
      
      const imagemTratada = prod.thumbnail ? prod.thumbnail.replace('-I.jpg', '-O.jpg') : '';
      const precoFormatado = prod.price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

      card.innerHTML = `
        <img src="${imagemTratada}" alt="${prod.title}">
        <h4>${prod.title}</h4>
        <div class="price">${precoFormatado}</div>
        <button class="btn-select">Ver Oferta</button>
      `;

      card.onclick = () => abrirModal({
        title: prod.title,
        price: precoFormatado,
        link: prod.permalink,
        image: imagemTratada
      });

      resultsGrid.appendChild(card);
    });

  } catch (err) {
    statusDiv.innerText = "Não foi possível carregar os produtos. Tente novamente.";
    console.error(err);
  }
}

function abrirModal(produto) {
  produtoSelecionado = produto;
  
  document.getElementById('modalTitle').innerText = produto.title;
  document.getElementById('modalPrice').innerText = produto.price;
  document.getElementById('modalImg').src = produto.image;
  document.getElementById('modalLink').value = produto.link;
  document.getElementById('modalMlBtn').href = produto.link;
  
  document.getElementById('productModal').style.display = 'flex';
}

function fecharModal() {
  document.getElementById('productModal').style.display = 'none';
  produtoSelecionado = null;
}

async function enviarParaTelegram() {
  if (!produtoSelecionado) return;

  if (TELEGRAM_BOT_TOKEN.includes("SEU_BOT_TOKEN") || TELEGRAM_CHAT_ID.includes("SEU_CHAT_ID")) {
    alert("Configure o BOT_TOKEN e o CHAT_ID no arquivo script.js para habilitar o envio!");
    return;
  }

  const btn = document.getElementById('modalTelegramBtn');
  btn.innerText = "Enviando...";
  btn.disabled = true;

  const mensagem = `🛍️ *ACHADINHO IMPERDÍVEL!*\n\n` +
                   `📌 *${produtoSelecionado.title}*\n` +
                   `💰 *Preço:* ${produtoSelecionado.price}\n\n` +
                   `🔗 [Garantir Oferta no Mercado Livre](${produtoSelecionado.link})`;

  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: TELEGRAM_CHAT_ID,
        text: mensagem,
        parse_mode: 'Markdown',
        disable_web_page_preview: false
      })
    });

    const data = await res.json();

    if (data.ok) {
      alert("✅ Oferta enviada com sucesso para o Telegram!");
      fecharModal();
    } else {
      alert("❌ Erro ao enviar para o Telegram: " + data.description);
    }
  } catch (err) {
    alert("❌ Falha na conexão com o Telegram.");
    console.error(err);
  } finally {
    btn.innerText = "✈️ Enviar para o Telegram";
    btn.disabled = false;
  }
}