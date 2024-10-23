
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 04:27:44 2024

@author: user

"""
from requests_html import HTMLSession
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from fpdf import FPDF
from selenium import webdriver

#fig, ax = plt.subplots(figsize=(50, 50))

cabecalho = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}
COLUNAS_PLANILHA = ['Photo', 'Código', 'Descrição', 'Compra', 'Venda', 'Tamanhos']
COLUNAS_DOCUMENTO = ['Photo', 'Código', 'Descrição', 'Preço']
arquivo_json = 'links.json'
options = webdriver.FirefoxOptions()
serv = webdriver.FirefoxService(executable_path='/usr/bin/geckodriver' )
driver = webdriver.Firefox(options = options, service = serv)
client = requests.Session()
    #options.add_argument(f"--proxy-server={proxy}")    
    #options.add_argument("start-maximized")
    #options.add_argument("disable-infobars")options.add_argument("--disable-extensions")
actions = ActionChains(driver)
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--verbose")
        #options.add_argument("--remote-debugging-port=9222") 
options.add_argument('--headless')
options.add_argument("--disable-gpu")    
cache_tempo = 10 * 60  # Cache por 10 minutos
cache_valor = None
cache_timestamp = 0
data_pdf = []
    
url_cambio = 'https://www.xe.com/pt/currencyconverter/convert/?Amount=1&From=GBP&To=BRL'
def calcula_preco_venda(preco):
    libra_esterlina = cotacao_libra()
    if preco >= 1 and preco <= 14.99:
        preco = preco + 2.50 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 15 and preco <= 29.99:
        preco = preco + 2.50 + 10 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 30 and preco <= 49.99:
        preco = preco + 2.50 + 15 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 50 and preco <= 79.99:
        preco = preco + 5 + 20 + (preco * 0.023) + (preco * 0.053 * libra_esterlina) 
        return preco 
    elif preco >= 80 and preco <= 119.99:
        preco = preco + 5 + 25 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 120 and preco <= 149.99:
        preco = preco + 5 + 30 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 150 and preco <= 199.99:
        preco = preco + 5 + 35 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 200 and preco <= 299.99:
        preco = preco + 10 + 40 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 300 and preco <= 399.99:
        return preco + 10 + 50 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
    elif preco >= 400 and preco <= 499.99:
        return preco + 10 + 60 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
    elif preco >= 500 and preco <= 799.99:
        
        preco = preco + 10 + 70 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 800 and preco <= 999.99:
        preco = preco + 10 + 80 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 1000 and preco <= 1499.99:
        preco = preco = preco + 10 + 80 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 1500 and preco <= 1999.99:
        preco = preco + 10 + 100 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 2000 and preco <= 2999.99:
        preco = preco + 10 + 120 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 3000 and preco <= 3999.99:
        preco = preco + 10 + 140 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 4000 and preco <= 4999.99:
        preco = preco + 10 + 160 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 5000 and preco <= 5999.99:
        preco = preco + 10 + 180 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    elif preco >= 6000 and preco <= 6999.99:
        preco = preco + 10 + 200 + (preco * 0.023) + (preco * 0.053 * libra_esterlina)
        return preco
    else:
        return "Preço fora do intervalo"
def calcula_preco_reais(preco) -> float:
    libra_esterlina = cotacao_libra()
    preco_produto = libra_esterlina * float(preco)
    return preco_produto



def cotacao_libra() -> float:
    global cache_valor, cache_timestamp
    
    # Verifica se o valor está em cache e se ainda é válido
    if cache_valor is not None and (time.time() - cache_timestamp) < cache_tempo:
        logging.info(f'Usando valor em cache: {cache_valor}')
        return cache_valor

    try:
        r = requests.get(url_cambio)
        r.raise_for_status()  # Levanta exceção em caso de erro HTTP
    except requests.exceptions.HTTPError as e:
        logging.error(f'Erro HTTP ao obter valor da taxa de câmbio: {e}')
        return None
    except requests.exceptions.ConnectionError as e:
        logging.error(f'Erro ao se conectar a API para buscar a taxa de câmbio: {e}')
        return None
    except Exception as e:
        logging.error(f'Erro ao obter valor da taxa de câmbio: {e}')
        return None

    try:
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            result_element = soup.find('p', string='1,00 Libra esterlina =').find_next_sibling('p').find_all(string=True, recursive=False)[0]
            resultado = re.sub(",", ".", result_element)
            cache_valor = float(resultado)  # Armazena o valor em cache
            cache_timestamp = time.time()  # Armazena o tempo da última atualização
            logging.info(f'Taxa de Câmbio: {cache_valor}')
            return cache_valor
    except Exception as e:
        logging.error(f'Erro ao converter valor de GBP para BRL: {e}')
        return None
def gera_nome_arquivo(url_linha):
    nome_arquivo = ""
    if "houseoffraser" in url_linha:
        nome_arquivo = "houseoffrase"
        
    elif "sportsdirect" in url_linha:
        nome_arquivo = "sportsdirect"
        
    elif "18montrose" in url_linha:
        nome_arquivo = "18montrose"
        
    elif "evanscycles" in url_linha:
        nome_arquivo = "evanscycles"
    elif "game" in url_linha:
        nome_arquivo = "game"
    elif "studio" in url_linha:
        nome_arquivo = "studio"
    elif "scottsmenwear" in url_linha:
        nome_arquivo = "scottsmenwear"
    elif "flannels" in url_linha:
        nome_arquivo = "scottsmenwear"
    return nome_arquivo
def extracao_comum(url_linha):
    data_planilha = []
    tamanhos = []
    data_pdf = []
    cotacao_libra()  # Supondo que essa função já esteja definida
    page = 0
    i = 0
    x = 0
    df_planilha = pd.DataFrame(columns=COLUNAS_PLANILHA)

    driver.get(url_linha)
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
    while True:
        page += 1

        produtos_lista = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//ul[@id = 'navlist']/li//a[@class = 'ProductImageList']"))
        )

        imagens = driver.find_elements(By.XPATH, "//img[@class = 'rtimg MainImage img-responsive']")
        for imagem in imagens:
            imagem_produto = imagem.get_attribute("src")

            response = requests.get(imagem_produto)
            img_data = BytesIO(response.content)
            img = Image(img_data)
            data_pdf.append({'Photo': img})
            data_planilha.append({'Photo': img_data})

        for index, value in enumerate(produtos_lista):
            produtos_lista = WebDriverWait(driver, 100).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//ul[@id = 'navlist']/li//a[@class = 'ProductImageList']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", produtos_lista[index])

            imagem = produtos_lista[index].find_element(By.XPATH, "//img[@class = 'rtimg MainImage img-responsive']").get_attribute("src")

            driver.execute_script("arguments[0].click();", produtos_lista[index])

            i += 1
            time.sleep(5)
            driver.save_screenshot(gera_nome_arquivo(url_linha) + str(i) + ".png")

            pagina_produto = driver.page_source
            soup = BeautifulSoup(pagina_produto, "html5lib")
            codigo_produto = driver.current_url.split('colcode=')[-1]

            nome_marca = soup.find("span", id="lblProductBrand").text
            nome_modelo = soup.find("span", id="lblProductName").text
            nome_produto = nome_marca + nome_modelo

            preco = soup.find("span", id='lblSellingPrice').text
            preco = re.sub("£", "", preco)
            preco_produto = float(preco)

            lista_tamanhos = driver.find_element(By.XPATH, "//ul[@id = 'ulSizes']")
            if lista_tamanhos:
                for tamanho in lista_tamanhos.find_elements(By.XPATH, "//li[@id = 'liItem']"):
                    tamanho_produto = tamanho.text
                    tamanhos.append(tamanho_produto)

            preco_reais = calcula_preco_reais(preco_produto)
            preco_venda = calcula_preco_venda(preco_produto)

            data_planilha.append({
                'Código': codigo_produto,
                'Descrição': nome_produto,
                'Compra': preco_produto,
                'Venda': preco_venda,
                'Tamanhos': tamanhos
            })

            data_pdf.append({
                'Código': codigo_produto,
                'Descrição': nome_produto,
                'Preço': preco_produto,
                'Photo': img
            })
            driver.back()

        try:
            proximo_botao = WebDriverWait(driver, 500).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id = 'divPagination']//a[@class = 'swipeNextClick NextLink ']"))
            )
            if proximo_botao:
                driver.execute_script("arguments[0].scrollIntoView();", proximo_botao)
                driver.execute_script("arguments[0].click();", proximo_botao)
                x += 1
                time.sleep(5)
            else:
                break
        except TimeoutException:
            break

    nome_arquivo = gera_nome_arquivo(url_linha)
    figura = gera_pdf(data_pdf)
    pdf_pages = PdfPages("catalogo_" + nome_arquivo + ".pdf")
    pdf_pages.savefig(figura)
    pdf_pages.close()

    df_planilha = pd.DataFrame(data_planilha)
    df_planilha.to_excel("planilha_" + nome_arquivo + ".xlsx")
    
def extracao_comum(url_linha):
    data_planilha = []
    tamanhos = []
    data_pdf = []
    cotacao_libra()  # Supondo que essa função já esteja definida
    page = 0
    i = 0
    x = 0
    df_planilha = pd.DataFrame(columns=COLUNAS_PLANILHA)

    driver.get(url_linha)
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
    while True:
        page += 1

        produtos_lista = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//ul[@id = 'navlist']/li//a[@class = 'ProductImageList']"))
        )

        imagens = driver.find_elements(By.XPATH, "//img[@class = 'rtimg MainImage img-responsive']")
        for imagem in imagens:
            imagem_produto = imagem.get_attribute("src")

            response = requests.get(imagem_produto)
            img_data = BytesIO(response.content)
            img = Image(img_data)
            data_pdf.append({'Photo': img})
            data_planilha.append({'Photo': img_data})

        for index, value in enumerate(produtos_lista):
            produtos_lista = WebDriverWait(driver, 100).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//ul[@id = 'navlist']/li//a[@class = 'ProductImageList']"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", produtos_lista[index])

            imagem = produtos_lista[index].find_element(By.XPATH, "//img[@class = 'rtimg MainImage img-responsive']").get_attribute("src")

            driver.execute_script("arguments[0].click();", produtos_lista[index])

            i += 1
            time.sleep(5)
            driver.save_screenshot(gera_nome_arquivo(url_linha) + str(i) + ".png")

            pagina_produto = driver.page_source
            soup = BeautifulSoup(pagina_produto, "html5lib")
            codigo_produto = driver.current_url.split('colcode=')[-1]

            nome_marca = soup.find("span", id="lblProductBrand").text
            nome_modelo = soup.find("span", id="lblProductName").text
            nome_produto = nome_marca + nome_modelo

            preco = soup.find("span", id='lblSellingPrice').text
            preco = re.sub("£", "", preco)
            preco_produto = float(preco)

            lista_tamanhos = driver.find_element(By.XPATH, "//ul[@id = 'ulSizes']")
            if lista_tamanhos:
                for tamanho in lista_tamanhos.find_elements(By.XPATH, "//li[@id = 'liItem']"):
                    tamanho_produto = tamanho.text
                    tamanhos.append(tamanho_produto)

            preco_reais = calcula_preco_reais(preco_produto)
            preco_venda = calcula_preco_venda(preco_produto)

            data_planilha.append({
                'Código': codigo_produto,
                'Descrição': nome_produto,
                'Compra': preco_produto,
                'Venda': preco_venda,
                'Tamanhos': tamanhos
            })

            data_pdf.append({
                'Código': codigo_produto,
                'Descrição': nome_produto,
                'Preço': preco_produto,
                'Photo': img
            })
            driver.back()

        try:
            proximo_botao = WebDriverWait(driver, 500).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id = 'divPagination']//a[@class = 'swipeNextClick NextLink ']"))
            )
            if proximo_botao:
                driver.execute_script("arguments[0].scrollIntoView();", proximo_botao)
                driver.execute_script("arguments[0].click();", proximo_botao)
                x += 1
                time.sleep(5)
            else:
                break
        except TimeoutException:
            break

    nome_arquivo = gera_nome_arquivo(url_linha)
    figura = gera_pdf(data_pdf)
    pdf_pages = PdfPages("catalogo_" + nome_arquivo + ".pdf")
    pdf_pages.savefig(figura)
    pdf_pages.close()

    df_planilha = pd.DataFrame(data_planilha)
    df_planilha.to_excel("planilha_" + nome_arquivo + ".xlsx")

    
def extrai_dados_lovellsports(url_linha):
    # Inicializar listas e variáveis
    data_planilha = []
    data_pdf = []
    tamanhos = []
    
    # Criar workbook e DataFrame para planilha Excel
    wb = Workbook()
    ws = wb.active
    cotacao_libra()  # Supondo que essa função já esteja definida
    i = 0
    df_planilha = pd.DataFrame(columns=COLUNAS_PLANILHA)
    
    driver.get(url_linha)
    pagina_resultados = driver.page_source
    soup = BeautifulSoup(pagina_resultados, "html.parser")
    lista_produtos = soup.find_all("div", class_="item")

    # Processar os produtos e suas imagens
    x = 1  # Para controle de páginas
    y = 0  # Para controle de produtos
    
    while True:
        imagens = soup.find_all("div", class_="image")
        
        for produto, imagem in zip(lista_produtos, imagens):
            # Obter link da imagem
            imagem_tag = imagem.find_next("img")
            if imagem_tag:
                imagem_produto = imagem_tag['src']
                image_response = requests.get(imagem_produto)
                image_data = BytesIO(image_response.content)
                
                # Adicionar a imagem ao PDF (lista temporária)
                data_pdf.append({
                    'Photo': image_data,
                })
                
                # Adicionar a imagem à planilha Excel
                img = Image(image_data)
                ws.add_image(img, f'A{y + 2}')  # Exemplo de posição: Coluna A, a partir da linha 2
            
            # Processar informações do produto
            y += 1
            link_produto = produto.find("a", class_="main").attrs["href"]
            pagina_produto = requests.get(link_produto)
            soup_produto = BeautifulSoup(pagina_produto.text, "lxml")
            
            # Obter nome, código e preço do produto
            nome_produto = soup_produto.find("h1", class_="product-name").text
            codigo_produto = pagina_produto.url.split("/")[-1]
            preco = soup_produto.find("span", class_="price-main special").text
            preco_libra = re.sub("£", "", preco)
            preco_produto = float(preco_libra)
            
            # Obter tamanhos disponíveis
            lista_tamanhos = soup_produto.find_all("div", class_="orderButtonDiv")
            tamanhos_produto = []
            if lista_tamanhos:
                for tamanho in lista_tamanhos:
                    texto_tamanho = tamanho.text.strip()
                    if "-" in texto_tamanho:
                        tamanho_produto = texto_tamanho.split('-')[0].strip()
                        tamanhos_produto.append(tamanho_produto)
                    elif "(" in texto_tamanho:
                        tamanho_produto = texto_tamanho.split('(')[0].strip()
                        tamanhos_produto.append(tamanho_produto)

            preco_reais = calcula_preco_reais(preco_produto)  # Função precisa estar definida
            preco_venda = calcula_preco_venda(preco_produto)  # Função precisa estar definida

            # Adicionar dados à planilha e ao PDF
            data_planilha.append({
                'Código': codigo_produto,
                'Descrição': nome_produto,
                'Compra': preco_produto,
                'Venda': preco_venda,
                'Tamanhos': tamanhos_produto
            })
            
            data_pdf.append({
                'Código': codigo_produto,
                'Descrição': nome_produto,
                'Preço': preco_produto
            })
            
            
            ws[f'B{y + 2}'] = codigo_produto
            ws[f'C{y + 2}'] = nome_produto
            ws[f'D{y + 2}'] = preco_produto
            ws[f'E{y + 2}'] = preco_venda
            ws[f'F{y + 2}'] = ", ".join(tamanhos_produto)

        
        try:
            print("Procurando o botão 'Próximo'...")
            time.sleep(5)
            proximo_botao = WebDriverWait(driver, 500).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='pgr']//a[@id='pageLink2']"))
            )
            
            if proximo_botao:
                driver.execute_script("arguments[0].scrollIntoView();", proximo_botao)
                driver.execute_script("arguments[0].click();", proximo_botao)
                print(f"Página {x + 1} processada.")
                x += 1
                time.sleep(5)
            else:
                print("Botão 'Próximo' não encontrado. Finalizando.")
                break
        except TimeoutException:
            print("Tempo esgotado esperando o botão 'Próximo'. Finalizando.")
            break

    # Gerar PDF com as imagens e dados
    figura = gera_pdf(data_pdf)  # Assumindo que você tenha essa função
    pdf_pages = PdfPages("catalogo_lovellsports.pdf")
    pdf_pages.savefig(figura)
    pdf_pages.close()

    # Salvar a planilha Excel com as imagens embutidas
    wb.save("catalogo_lovellsports.xlsx")

    #driver.quit()  # Fechar o navegador ao final
import requests
from urllib.parse import urlparse

def get_products(url_linha):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    # Pegar o caminho da URL
    path = urlparse(url_linha).path

    # API base
    url = 'https://www.prodirectsport.com/api/v1/search'

    page = 1
    all_products = []

    while True:
        params = {
            'location': f'{path}?pg={page}',
        }
        
        # Fazendo a requisição
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        # Verifica se há produtos na página atual
        if 'products' not in data or not data['products']:
            break

        all_products.extend(data['products'])
        page += 1

    return all_products

# URL da página inicial

"""
def extrai_dados_prodirectsports(url_linha):
    # Extrair produtos de todas as páginas
    products = get_products(url_linha)
    
    # Criar a lista de dados para a planilha
    product_data = []
    
    for product in products:
        preco = product["pricing"]["current"]
        preco_venda = calcula_preco_venda(preco)
        preco_reais = calcula_preco_reais(preco)
        sizes = ', '.join([size['name'] for size in product.get('variants', [])])
        product_data.append({
            'Name': product["name"],
            'Preco': preco,
            "Venda": preco_venda,
            'SKU': product["id"],
            'Sizes': sizes,
            'Image URL': product["image"]
        })

    # Criar DataFrame e salvar em Excel
    df = pd.DataFrame(product_data)
    df.to_excel("products.xlsx", index=False)
    print("Planilha Excel gerada com sucesso!")
    
    # Chamar função para gerar o PDF
    gera_pdf(products)
   """     
        
        
           

def extrai_dados_prodirectsports(url_linha):
    # Extrair produtos de todas as páginas
    products = get_products(url_linha)
    
    # Criar a lista de dados para a planilha
    product_data = []
    
    for product in products:
        preco = product["pricing"]["current"]
        preco_venda = calcula_preco_venda(preco)
        preco_reais = calcula_preco_reais(preco)
        sizes = ', '.join([size['name'] for size in product.get('variants', [])])
        product_data.append({
            'Name': product["name"],
            'Preco': preco,
            "Venda": preco_venda,
            'SKU': product["id"],
            'Sizes': sizes,
            'Image URL': product["image"]
        })

    # Criar DataFrame e salvar em Excel
    df = pd.DataFrame(product_data)
    df.to_excel("products.xlsx", index=False)
    print("Planilha Excel gerada com sucesso!")
    
    # Chamar função para gerar o PDF
    gera_pdf(products)def gera_pdf(data_pdf):
    # Função para gerar as páginas do PDF com as imagens e os dados
    fig, ax = plt.subplots(figsize=(8.27, 11.69))  # Tamanho A4 em polegadas
    ax.axis('off')

    for i, item in enumerate(data_pdf):
        ax.text(0.1, 1 - 0.1 * (i + 1), f"Código: {item['Código']}, Preço: {item['Preço']}")
        
        if 'Photo' in item:
            image_data = item['Photo']
            img = plt.imread(image_data, format='png')
            ax.imshow(img, aspect='auto', extent=[0.5, 1, 0.9 - 0.1 * (i + 1), 0.9 - 0.1 * (i + 1) - 0.1])
        
        if (i + 1) % 5 == 0:  # Limitar 5 produtos por página
            plt.show()
            fig, ax = plt.subplots(figsize=(8.27, 11.69))
            ax.axis('off')

    return fig
    

    
def redireciona():
    with open(arquivo_json) as arquivo:
        
        dados = json.load(arquivo)
        for url_linha in dados.values():
            if (url_linha.startswith('https://www.sportsdirect.com/') or
                url_linha.startswith('https://www.flannels.com/') or 
                url_linha.startswith('https://www.cruisefashion.com/') or
                url_linha.startswith('https://www.evanscycles.com/') or
                url_linha.startswith('https://www.houseoffraser.co.uk/') or
                url_linha.startswith('https://www.scottsmenswear.com/') or
                url_linha.startswith('https://www.studio.co.uk/') or
                url_linha.startswith('https://www.18montrose.com/') or
                url_linha.startswith('https://www.game.co.uk/')):
                extracao_comum(url_linha)
            elif url_linha.startswith('https://www.lovellsports.com/'):
                extrai_dados_lovellsports(url_linha)
            elif url_linha.startswith('https://www.usc.co.uk/'):
                extrai_dados_usc(url_linha)
            elif url_linha.startswith("https://www.prodirectsport.com/"):
                extrai_dados_prodirectsports(url_linha)
            
                
            
            else:
                print('URL inválida:', url_linha)

if __name__ == "__main__":
    redireciona()
    print("redirecionou")
