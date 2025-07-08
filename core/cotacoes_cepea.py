import requests
from bs4 import BeautifulSoup

def consultar_boi_gordo():
    url = "https://www.cepea.org.br/br/indicador/boi-gordo.aspx"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"erro": f"Erro ao acessar a página do Boi Gordo: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")

    tabela = soup.find("table", id="imagenet-indicador1")
    if not tabela:
        return {"erro": "Tabela de Boi Gordo não encontrada."}

    tbody = tabela.find("tbody")
    if not tbody:
        return {"erro": "Corpo da tabela (tbody) não encontrado."}

    linhas = tbody.find_all("tr")
    if not linhas or len(linhas) == 0:
        return {"erro": "Nenhuma linha encontrada na tabela do Boi Gordo."}

    primeira_linha = linhas[0]
    colunas = primeira_linha.find_all("td")
    if len(colunas) < 2:
        return {"erro": "Não foi possível extrair data e preço do Boi Gordo."}

    data = colunas[0].get_text(strip=True)
    preco = colunas[1].get_text(strip=True)

    return {"data": data, "preco": preco}


def consultar_preco_cepea(nome_produto):
    if nome_produto == "Boi Gordo":
        return consultar_boi_gordo()

    urls = {
        "Bezerro - MS": "https://www.cepea.org.br/br/indicador/bezerro.aspx",
        "Bezerro - SP": "https://www.cepea.org.br/br/indicador/bezerro-media-sao-paulo.aspx",
        "Frango": "https://www.cepea.org.br/br/indicador/frango.aspx",
        "Leite (Brasil)": "https://www.cepea.org.br/br/indicador/leite.aspx",
    }

    if nome_produto not in urls:
        return {"erro": f"Produto '{nome_produto}' não suportado."}

    url = urls[nome_produto]
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

    linhas = tabela.find_all("tr")
    if len(linhas) < 2:
        return {"erro": f"Estrutura inesperada na tabela do {nome_produto}."}

    try:
        if nome_produto == "Leite (Brasil)":
            for linha in linhas[1:]:
                cols = linha.find_all("td")
                if len(cols) < 3:
                    continue
                local = cols[1].get_text(strip=True).lower()
                if local == "brasil":
                    data = cols[0].get_text(strip=True)
                    preco = cols[2].get_text(strip=True)
                    return {"data": data, "preco": preco}
            return {"erro": "Cotação para Brasil não encontrada."}

        tbody = tabela.find("tbody")
        if tbody:
            linhas_dados = tbody.find_all("tr")
        else:
            linhas_dados = linhas[1:]

        for linha in linhas_dados:
            cols = linha.find_all("td")
            if len(cols) >= 2:
                data = cols[0].get_text(strip=True)
                preco = cols[1].get_text(strip=True)
                if data and preco:
                    return {"data": data, "preco": preco}

        return {"erro": f"Não foi possível extrair dados válidos do {nome_produto}."}

    except Exception as e:
        return {"erro": f"Erro ao processar dados do {nome_produto}: {e}"}
