# 🦆 Scraping Perdigão

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

Sistema completo para coleta automatizada de dados nutricionais dos produtos da Perdigão. Desenvolvido com Python, oferece uma interface CLI intuitiva e funcionalidades robustas para extração e organização de informações nutricionais.

## 📋 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [🚀 Instalação](#-instalação)
- [📖 Como Usar](#-como-usar)
- [📊 Dados Coletados](#-dados-coletados)
- [🏗️ Arquitetura](#️-arquitetura)
- [🛠️ Tecnologias](#️-tecnologias)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🤝 Contribuindo](#-contribuindo)
- [📄 Licença](#-licença)

## ✨ Funcionalidades

### 🕷️ Coleta Inteligente de URLs
- **Automação completa**: Coleta URLs de 12 categorias de produtos
- **Filtros inteligentes**: Remove URLs de seções e filtros automaticamente
- **Robustez**: Tratamento de erros e retry automático
- **Eficiência**: Pausas respeitosas entre requisições

### 📊 Extração de Dados Nutricionais
- **Dados completos**: 10 campos nutricionais essenciais
- **Precisão**: Tratamento especial para diferentes formatos de tabela
- **Flexibilidade**: Suporte a múltiplos formatos de dados
- **Validação**: Verificação automática de integridade

### 🚀 Interface CLI Profissional
- **Interface intuitiva**: Menu colorido com emojis
- **Progresso visual**: Barras de progresso animadas
- **Gerenciamento de arquivos**: Listagem e limpeza automática
- **Estatísticas**: Relatórios detalhados de execução

## 🚀 Instalação

### Pré-requisitos
- Python 3.13 ou superior
- Conexão com internet estável

### Passos de Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/sidnei-almeida/scraping_perdigao.git
cd scraping_perdigao
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute o programa**
```bash
python main.py
```

## 📖 Como Usar

### Interface CLI

Execute o programa principal:
```bash
python main.py
```

### Opções Disponíveis

| Opção | Funcionalidade | Descrição |
|-------|----------------|-----------|
| 🕷️ 1 | **Coletar URLs** | Extrai URLs de produtos de todas as categorias |
| 📊 2 | **Extrair Dados** | Coleta dados nutricionais dos produtos |
| 🚀 3 | **Coleta Completa** | Executa URLs + dados em sequência |
| 📋 4 | **Ver Arquivos** | Lista arquivos gerados com estatísticas |
| 🗑️ 5 | **Limpar Dados** | Remove arquivos antigos |
| 📖 6 | **Sobre** | Informações do programa |
| ❌ 7 | **Sair** | Encerra o programa |

### Fluxo de Trabalho Recomendado

1. **Primeira execução**: Use a opção `3` (Coleta Completa)
2. **Atualizações**: Use a opção `2` (Extrair Dados) para novos dados
3. **Manutenção**: Use a opção `4` para verificar arquivos

## 📊 Dados Coletados

O sistema coleta os seguintes dados nutricionais:

| Campo | Descrição | Unidade |
|-------|-----------|---------|
| `NOME_PRODUTO` | Nome do produto | - |
| `URL` | URL da página do produto | - |
| `PORCAO (g)` | Porção de referência | gramas |
| `CALORIAS (kcal)` | Valor energético | kcal |
| `CARBOIDRATOS (g)` | Carboidratos | gramas |
| `PROTEINAS (g)` | Proteínas | gramas |
| `GORDURAS_TOTAIS (g)` | Gorduras totais | gramas |
| `GORDURAS_SATURADAS (g)` | Gorduras saturadas | gramas |
| `FIBRAS (g)` | Fibras alimentares | gramas |
| `ACUCARES (g)` | Açúcares | gramas |
| `SODIO (mg)` | Sódio | miligramas |

### Categorias de Produtos

O sistema coleta dados de 12 categorias principais:

- 🍗 **Empanados** - Produtos empanados
- 🌭 **Salsichas** - Variedade de salsichas
- 🥓 **Linguiças** - Linguiças frescais e defumadas
- 🧀 **Frios** - Mortadelas, presuntos, salames
- 🍽️ **Pratos Prontos** - Refeições individuais
- 🥪 **Lanches** - Pães de queijo, hambúrgueres
- 🥓 **Bacon** - Cortes de bacon
- 🐷 **Suínos** - Cortes de carne suína
- 🐔 **Frango** - Produtos de frango
- 🏢 **Food Service** - Produtos para estabelecimentos
- 🎉 **Comemorativos** - Produtos especiais
- 🦃 **Peru** - Produtos de peru

## 🏗️ Arquitetura

### Componentes Principais

```
scraping_perdigao/
├── 📁 config/           # Scripts de processamento
│   ├── url_collector.py # Coletor de URLs
│   └── scraper.py       # Extrator de dados
├── 📁 dados/            # Arquivos de saída
│   ├── product_urls.json    # URLs coletadas
│   └── produtos_*.csv       # Dados nutricionais
├── 🎮 main.py           # Interface CLI
└── 📋 requirements.txt  # Dependências
```

### Fluxo de Processamento

1. **Coleta de URLs** (`url_collector.py`)
   - Acessa 12 seções de produtos
   - Filtra URLs de produtos individuais
   - Salva em `dados/product_urls.json`

2. **Extração de Dados** (`scraper.py`)
   - Lê URLs do JSON
   - Acessa cada página de produto
   - Extrai dados nutricionais
   - Salva em CSV com timestamp

3. **Interface CLI** (`main.py`)
   - Gerencia todo o processo
   - Fornece feedback visual
   - Permite gerenciamento de arquivos

## 🛠️ Tecnologias

### Core Technologies
- **Python 3.13** - Linguagem principal
- **Requests** - Requisições HTTP
- **BeautifulSoup4** - Parsing HTML
- **Pandas** - Manipulação de dados
- **LXML** - Parser XML/HTML

### Características Técnicas
- **Modular**: Código organizado em módulos
- **Robusto**: Tratamento de erros abrangente
- **Eficiente**: Otimizado para performance
- **Escalável**: Fácil adição de novas funcionalidades

## 📁 Estrutura do Projeto

```
scraping_perdigao/
├── 📁 config/
│   ├── url_collector.py     # Coletor de URLs
│   └── scraper.py           # Extrator de dados
├── 📁 dados/
│   ├── product_urls.json    # URLs dos produtos
│   └── produtos_*.csv       # Dados nutricionais
├── 🎮 main.py              # Interface CLI
├── 📋 requirements.txt      # Dependências Python
├── 📄 README.md            # Este arquivo
└── 📄 template_main.py     # Template para CLI
```

## 🤝 Contribuindo

### Como Contribuir

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Padrões de Código

- **PEP 8**: Seguir padrões Python
- **Docstrings**: Documentar funções
- **Type Hints**: Usar tipagem quando possível
- **Error Handling**: Tratar exceções adequadamente

### Reportando Bugs

- Use as **Issues** do GitHub
- Inclua informações detalhadas
- Adicione logs de erro quando possível

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Sidnei Almeida**

- **GitHub**: [@sidnei-almeida](https://github.com/sidnei-almeida)
- **Projeto**: [scraping_perdigao](https://github.com/sidnei-almeida/scraping_perdigao)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela! ⭐**

</div> 