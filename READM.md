# Teste Dev JR Reylab

Teste para a empresa Reylab para desenvolvedor Júnior, o teste consiste em completar o desafio do site [RPAChallange](https://rpachallenge.com/), automatizando o download, preenchimento de formulário e buscando o tempo de execução.

## Tecnologias utilizadas:
* Python 3.11
* Selenium 4.38.0
* Pandas 2.3.3
* Openpyxl 3.1.5

## Setup

### Instalando o Python:
Para rodar o projeto será necessário ter o Python instalado na sua máquina. Os sistemas Linux recentas já possuem o Python instalado mas caso queira ter certeza, pode rodar o seguinte comando para verificar:
```
which python3
```
e o comando para validar a versão:
```
python3 --version
```
Caso não tenha o python instalado pode ver como instalar o Python clicando [aqui](https://www.python.org/downloads/).

### Criando o ambiente:
Utilizei o conda para lidar com o ambiente deste projeto, para instalar o conda clique [aqui](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

Após instalado utilizar o seguinte comando para criar um abiente com o Python 3.11 instalado:
``` 
conda create -n web_automation python=3.11 
```

Depois rode para ativar o ambiente:
``` 
conda activate web_automation 
```

### Instalando as dependências do projeto:
O Projeto utiliza o [Selenium](https://www.selenium.dev/pt-br/documentation/), e o [Pandas](https://pandas.pydata.org/) junto do [Openpyxl](https://pypi.org/project/openpyxl/). Para instalar as dependências utilize o comando: 
```
 pip install -r requirements.txt
 ```

## Rodando o projeto

Para rodar o projeto vá até a pasta em que ele foi extraido, e na raiz rode o comando 
```
python main.py
```

## Considerações
Foi um desafio bem divertido, aprender o básico do Selenium é satisfatório, mas tive um pouco de dificuldade localizando alguns elementos da página, como os campos do formulário, que tinham uns nomes aleatórios e acertar o local do download do arquivo excel, que precisa ser um caminho absoluto, fora isso tudo fluiu muito bem, terminei o projeto dia 13/11/2025 às 21:15.

Decidi fazer o script da automação em outra pasta em vez de em um arquivo só por questões de organização, caso precise rodar mais de alguma automação junta ou algum outro processo isso seria feito através do arquivo main.py, dessa forma sigo o padrão SOLID.

Tentei separar bem as funções e deixar elas simples de serem lidas para facilitar o entendimento e facilitar futuros testes