import requests
from bs4 import BeautifulSoup

URLS_AGRICULTURA = {
    "Milho": "https://www.cepea.org.br/br/indicador/milho.aspx",
    "Soja": "https://www.cepea.org.br/br/indicador/soja.aspx",
    "Algodão": "https://www.cepea.org.br/br/indicador/algodao.aspx",
    "Café arábica": "https://www.cepea.org.br/br/indicador/cafe.aspx",
    "Trigo": "https://www.cepea.org.br/br/indicador/trigo.aspx",
    "Arroz": "https://www.cepea.org.br/br/indicador/arroz.aspx",
}

def consultar_preco_agricultura(nome_produto):
    if nome_produto not in URLS_AGRICULTURA:
        return {"erro": f"Produto '{nome_produto}' não suportado."}
    
    url = URLS_AGRICULTURA[nome_produto]
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"erro": f"Erro ao acessar a página do {nome_produto}: {e}"}
    
    soup = BeautifulSoup(response.text, "html.parser")

    tabela = soup.find("table")
    if not tabela:
        return {"erro": f"Tabela de {nome_produto} não encontrada."}
    
    tbody = tabela.find("tbody")
    linhas = tbody.find_all("tr") if tbody else tabela.find_all("tr")

    if not linhas or len(linhas) == 0:
        return {"erro": f"Nenhuma linha encontrada na tabela do {nome_produto}."}

    primeira_linha = linhas[0]
    colunas = primeira_linha.find_all("td")
    if len(colunas) < 2:
        return {"erro": f"Não foi possível extrair data e preço do {nome_produto}."}

    data = colunas[0].get_text(strip=True)
    preco = colunas[1].get_text(strip=True)

    return {"data": data, "preco": preco}
