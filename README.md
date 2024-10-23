Este projeto é um web scraper que lê um arquivo JSON contendo links, acessa esses links usando BeautifulSoup ou Selenium, e exporta o conteúdo da página em formatos PDF e XLS.
Requisitos

Antes de começar, certifique-se de ter os seguintes itens instalados:

    Python 3.x
    pip (gerenciador de pacotes do Python)

Instalação

    Clone o repositório ou faça o download do código.

    bash

git clone https://github.com/seuusuario/seu-repositorio.git
cd seu-repositorio

Instale as dependências.

Antes de executar o programa, é necessário instalar os pacotes necessários. Execute o seguinte comando para instalar os requisitos:

bash

    pip install -r requirements.txt

    O arquivo requirements.txt inclui dependências como:
        beautifulsoup4
        selenium
        pandas (para exportação em XLS)
        
        requests (para acesso a páginas)
        openpyxl (para trabalhar com arquivos Excel)

Executando o Programa

Após instalar as dependências, você pode rodar o programa passando o arquivo JSON como argumento.

    Prepare o arquivo JSON contendo os links que deseja acessar. O arquivo deve ter o seguinte formato:

    json

{
  "links": [
    "https://exemplo.com",
    "https://outroexemplo.com"
  ]
}

Execute o programa:

bash

    python scraper.py caminho_para_o_arquivo.json

    O programa irá:
        Ler os links do arquivo JSON.
        Acessar as páginas usando BeautifulSoup ou Selenium (dependendo da estrutura do site).
        Exportar o conteúdo de cada página para um arquivo PDF e XLS.

Parâmetros opcionais

    Você pode especificar qual método usar para acessar as páginas (beautifulsoup ou selenium). Por padrão, o programa tentará usar BeautifulSoup e, caso necessário, recorrerá ao Selenium.

    bash

    python scraper.py caminho_para_o_arquivo.json --method selenium

Notas

    O Selenium requer o download do WebDriver adequado para o navegador que você vai usar (como Chrome ou Firefox). Por favor, consulte a documentação do Selenium para configurar o WebDriver no seu ambiente.
    O programa irá salvar os arquivos PDF e XLS em uma pasta chamada output/, que será criada automaticamente se não existir.
