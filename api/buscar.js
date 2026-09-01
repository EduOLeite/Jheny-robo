module.exports = async (req, res) => {
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

  const CLIENT_ID = "7613714423454405";
  const CLIENT_SECRET = "x9q0QWG6O4wDRaeqGF08hSU7SQaNWdLj";

  try {
    // 1. Solcita o Access Token temporário ao Mercado Livre via Client Credentials
    const authUrl = 'https://api.mercadolibre.com/oauth/token';
    const authParams = new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET
    });

    const authResponse = await fetch(authUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: authParams.toString()
    });

    if (!authResponse.ok) {
      const authError = await authResponse.text();
      console.error('Erro na autenticação Mercado Livre:', authError);
      return res.status(authResponse.status).json({ error: 'Falha ao autenticar no Mercado Livre.' });
    }

    const authData = await authResponse.json();
    const accessToken = authData.access_token;

    // 2. Realiza a busca utilizando o Access Token obtido
    const searchUrl = `https://api.mercadolibre.com/sites/MLB/search?q=${encodeURIComponent(q)}&limit=${limit}`;
    const searchResponse = await fetch(searchUrl, {
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });

    if (!searchResponse.ok) {
      return res.status(searchResponse.status).json({ error: `Erro Mercado Livre: ${searchResponse.status}` });
    }

    const data = await searchResponse.json();
    return res.status(200).json(data);

  } catch (error) {
    console.error('Erro no servidor Backend:', error);
    return res.status(500).json({ error: 'Falha interna no servidor ao processar a busca.' });
  }
};