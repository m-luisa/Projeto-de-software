import requests
from bs4 import BeautifulSoup

class MetroSPScraper:
    """RF3 e RF5 - lê a página oficial "Direto do Metrô" (sem login/chave).
    observação: isso não é uma API documentada, é a página pública do site.
    se o Metrô-SP mudar o HTML, o parsing abaixo pode quebrar
    """
    
    URL = "https://www.metro.sp.gov.br/direto-do-metro"

    def buscar_status(self) -> list[dict]:
        try:  # tratamento de erro
            resposta = requests.get(self.URL, timeout=10)
            resposta.raise_for_status()
        except requests.RequestException as erro:
            raise requests.RequestException(
                f"Falha ao acessar a página do Metrô-SP: {erro}"
            ) from erro

        html = BeautifulSoup(resposta.content, "html.parser")
        itens = html.find_all("li")

        linhas = []
        for item in itens:
            divs = item.find_all("div")
            numero = nome = situacao = None
            for div in divs:
                classes = div.get("class", [])
                if "linha-numero" in classes:
                    numero = div.text.strip()
                elif "linha-nome" in classes:
                    nome = div.text.strip()
                elif "linha-situacao" in classes:
                    situacao = div.text.strip()

            """só é uma "linha" de verdade se tiver ao menos o número o resto do <li> da página pode não ser sobre uma linha"""
            if numero:
                linhas.append({"numero": numero, "nome": nome, "situacao": situacao})

        return linhas