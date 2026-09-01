module.exports = async (req, res) => {
  // Permite acesso de qualquer origem (CORS)
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  const { q, limit = 10 } = req.query;

  if (!q) {
    return res.status(400).json({ error: 'Termo de busca não informado.' });
  }

  try {
    const url = `https://api.mercadolibre.com/sites/MLB/search?q=${encodeURIComponent(q)}&limit=${limit}`;
    const response = await fetch(url);

    if (!response.ok) {
      return res.status(response.status).json({ error: `Erro Mercado Livre: ${response.status}` });
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error) {
    console.error('Erro na função backend:', error);
    return res.status(500).json({ error: 'Falha ao buscar produtos no Mercado Livre.' });
  }
};