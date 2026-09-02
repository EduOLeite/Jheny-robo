module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "GET") {
    return res.status(405).json({
      error: "Método não permitido."
    });
  }

  const { q, limit = 10 } = req.query;

  if (!q || !q.trim()) {
    return res.status(400).json({
      error: "Termo de busca não informado."
    });
  }

  const clientId = process.env.MERCADO_LIVRE_CLIENT_ID;
  const clientSecret = process.env.MERCADO_LIVRE_CLIENT_SECRET;

  if (!clientId || !clientSecret) {
    console.error("Credenciais do Mercado Livre não configuradas.");

    return res.status(500).json({
      error: "Credenciais do Mercado Livre não configuradas no servidor."
    });
  }

  return res.status(501).json({
    error: "Backend do Mercado Livre preparado, mas a autenticação OAuth ainda não foi configurada."
  });
};