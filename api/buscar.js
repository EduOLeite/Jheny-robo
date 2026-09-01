export default async function handler(req, res) {
  // Configura cabeçalhos CORS para permitir requisições do front
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET');

  const { q, limit = 10 } = req.query;

  if (!q) {
    return res.status(400).json({ error: 'Termo de busca não informado.' });
  }

  try {
    const url = `https://api.mercadolibre.com/sites/MLB/search?q=${encodeURIComponent(q)}&limit=${limit}`;
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      }
    });

    if (!response.ok) {
      throw new Error(`Erro Mercado Livre: ${response.status}`);
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error) {
    console.error('Erro na API:', error);
    return res.status(500).json({ error: 'Falha ao buscar produtos no Mercado Livre.' });
  }
}