const TELEGRAM_BOT_TOKEN = "8866238346:AAFqgpZclKx0pdqC05ySfRZVek02z4L883I";
const TELEGRAM_CHAT_ID = "-4326152013";

let produtoSelecionado = null;

document.getElementById('searchInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    buscarProdutos();
  }
});

async function buscarProdutos() {
  const query = document.getElementById('searchInput').value.trim();
  const limitInput = document.getElementById('limitInput').value;
  const limit = Math.max(1, Math.min(50, parseInt(limitInput) || 10));

  const statusDiv = document.getElementById('statusMessage');
  const resultsGrid = document.getElementById('resultsGrid');

  if (!query) {
    statusDiv.innerText = "Por favor, digite o nome de um produto.";
    return;
  }

  statusDiv.innerText = "✨ Buscando as melhores ofertas...";
  resultsGrid.innerHTML = "";

  try {
    // Chama a nossa rota interna na Vercel
    const response = await fetch(`/api/buscar?q=${encodeURIComponent(query)}&limit=${limit}`);
    
    if (!response.ok) {
      throw new Error(`Erro status: ${response.status}`);
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

      const imagemTratada = prod.thumbnail ? prod.thumbnail.replace('-I.jpg', '-O.jpg').replace('http://', 'https://') : '';
      const precoFormatado = prod.price ? prod.price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) : 'Consulte';

      card.innerHTML = `
        <img src="${imagemTratada}" alt="${prod.title}" loading="lazy">
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
    console.error("Erro ao carregar produtos:", err);
    statusDiv.innerText = "Não foi possível carregar os produtos. Tente novamente.";
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