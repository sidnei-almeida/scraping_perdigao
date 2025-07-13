import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

def get_product_urls_from_section(section_url):
    """
    Coleta URLs de produtos de uma seção específica
    """
    try:
        print(f"Acessando: {section_url}")
        response = requests.get(section_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Procura por links de produtos (padrão: href="produtos/...")
        product_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('produtos/') and '/produtos/' not in href:
                # Constrói a URL completa
                full_url = urljoin('https://www.perdigao.com.br/', href)
                product_links.append(full_url)
        
        # Remove duplicatas mantendo a ordem
        unique_links = list(dict.fromkeys(product_links))
        print(f"Encontrados {len(unique_links)} links únicos")
        
        return unique_links
        
    except Exception as e:
        print(f"Erro ao acessar {section_url}: {e}")
        return []

def filter_product_urls(all_urls):
    """
    Filtra URLs para manter apenas produtos individuais
    """
    # URLs de seções, filtros e subcategorias para excluir
    exclude_urls = [
        'https://www.perdigao.com.br/produtos/',
        'https://www.perdigao.com.br/produtos/empanados',
        'https://www.perdigao.com.br/produtos/salsichas',
        'https://www.perdigao.com.br/produtos/linguicas',
        'https://www.perdigao.com.br/produtos/frios',
        'https://www.perdigao.com.br/produtos/pratos-prontos',
        'https://www.perdigao.com.br/produtos/lanches',
        'https://www.perdigao.com.br/produtos/bacon',
        'https://www.perdigao.com.br/produtos/suinos',
        'https://www.perdigao.com.br/produtos/frango',
        'https://www.perdigao.com.br/produtos/food-service',
        'https://www.perdigao.com.br/produtos/comemorativos',
        'https://www.perdigao.com.br/produtos/peru',
        'https://www.perdigao.com.br/produtos/empanados/todos-os-empanados',
        'https://www.perdigao.com.br/produtos/salsichas/todas-as-salsichas',
        'https://www.perdigao.com.br/produtos/linguicas/todas-as-linguicas-defumadas',
        'https://www.perdigao.com.br/produtos/linguicas/linguicas-frescais-recheadas',
        'https://www.perdigao.com.br/produtos/linguicas/linguicas-frescais',
        'https://www.perdigao.com.br/produtos/frios/mortadela-tradicional',
        'https://www.perdigao.com.br/produtos/frios/presuntos',
        'https://www.perdigao.com.br/produtos/frios/mortadela-ouro',
        'https://www.perdigao.com.br/produtos/frios/salame',
        'https://www.perdigao.com.br/produtos/frios/apresuntado',
        'https://www.perdigao.com.br/produtos/frios/mortadela-tubular',
        'https://www.perdigao.com.br/produtos/frios/lanche',
        'https://www.perdigao.com.br/produtos/pratos-prontos/refeicao-individual',
        'https://www.perdigao.com.br/produtos/pratos-prontos/pizzas',
        'https://www.perdigao.com.br/produtos/pratos-prontos/lasanhas',
        'https://www.perdigao.com.br/produtos/pratos-prontos/feijoada',
        'https://www.perdigao.com.br/produtos/pratos-prontos/empanado-a-parmegiana',
        'https://www.perdigao.com.br/produtos/lanches/pao-de-queijo',
        'https://www.perdigao.com.br/produtos/lanches/hamburgueres',
        'https://www.perdigao.com.br/produtos/bacon/cortes-de-bacon',
        'https://www.perdigao.com.br/produtos/suinos/cortes-de-todos-os-suinos',
        'https://www.perdigao.com.br/produtos/suinos/cortes-de-todos-os-suinos-temperados',
        'https://www.perdigao.com.br/produtos/frango/produtos-in-natura-de-frango',
        'https://www.perdigao.com.br/produtos/frango/produtos-in-natura-de-frango-temperados',
        'https://www.perdigao.com.br/produtos/food-service/salsichas',
        'https://www.perdigao.com.br/produtos/food-service/lanches',
        'https://www.perdigao.com.br/produtos/food-service/linguicas',
        'https://www.perdigao.com.br/produtos/food-service/frios',
        'https://www.perdigao.com.br/produtos/food-service/cortes-suinos',
        'https://www.perdigao.com.br/produtos/food-service/cortes-de-frango',
        'https://www.perdigao.com.br/produtos/food-service/todos-itens-de-food-service',
        'https://www.perdigao.com.br/produtos/comemorativos/pernil',
        'https://www.perdigao.com.br/produtos/comemorativos/chester',
        'https://www.perdigao.com.br/produtos/comemorativos/tender',
        'https://www.perdigao.com.br/produtos/comemorativos/peru',
        'https://www.perdigao.com.br/produtos/comemorativos/lombo',
        'https://www.perdigao.com.br/produtos/comemorativos/frango',
        'https://www.perdigao.com.br/produtos/peru/cortes-de-todos-os-perus'
    ]
    
    # Filtra URLs
    filtered_urls = []
    for url in all_urls:
        if url not in exclude_urls:
            filtered_urls.append(url)
    
    print(f"URLs antes do filtro: {len(all_urls)}")
    print(f"URLs após o filtro: {len(filtered_urls)}")
    print(f"URLs removidas: {len(all_urls) - len(filtered_urls)}")
    
    return filtered_urls

def collect_all_product_urls():
    """
    Coleta URLs de produtos de todas as seções
    """
    sections = {
        'EMPANADOS': 'https://www.perdigao.com.br/produtos/empanados/',
        'SALSICHAS': 'https://www.perdigao.com.br/produtos/salsichas/',
        'LINGUIÇAS': 'https://www.perdigao.com.br/produtos/linguicas/',
        'FRIOS': 'https://www.perdigao.com.br/produtos/frios/',
        'PRATOS PRONTOS': 'https://www.perdigao.com.br/produtos/pratos-prontos/',
        'LANCHES': 'https://www.perdigao.com.br/produtos/lanches/',
        'BACON': 'https://www.perdigao.com.br/produtos/bacon/',
        'SUINOS': 'https://www.perdigao.com.br/produtos/suinos/',
        'FRANGO': 'https://www.perdigao.com.br/produtos/frango/',
        'FOOD SERVICE': 'https://www.perdigao.com.br/produtos/food-service/',
        'COMEMORATIVOS': 'https://www.perdigao.com.br/produtos/comemorativos/',
        'PERU': 'https://www.perdigao.com.br/produtos/peru/'
    }
    
    all_product_urls = []
    
    for section_name, section_url in sections.items():
        print(f"\n=== COLETANDO {section_name} ===")
        product_urls = get_product_urls_from_section(section_url)
        all_product_urls.extend(product_urls)
        
        # Pausa entre requisições para ser respeitoso
        time.sleep(1)
    
    # Remove duplicatas finais
    final_urls = list(dict.fromkeys(all_product_urls))
    
    print(f"\n=== RESULTADO DA COLETA ===")
    print(f"Total de URLs únicas coletadas: {len(final_urls)}")
    
    return final_urls

def save_urls_to_json(urls, filename='product_urls.json'):
    """
    Salva as URLs em um arquivo JSON
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(urls, f, indent=2, ensure_ascii=False)
    print(f"URLs salvas em: {filename}")

if __name__ == "__main__":
    print("=== COLETOR DE URLs DE PRODUTOS PERDIGÃO ===")
    
    # Coleta todas as URLs
    all_urls = collect_all_product_urls()
    
    # Filtra URLs para manter apenas produtos individuais
    print(f"\n=== APLICANDO FILTRO ===")
    filtered_urls = filter_product_urls(all_urls)
    
    # Salva URLs filtradas
    save_urls_to_json(filtered_urls, 'dados/product_urls.json')
    
    # Mostra algumas URLs como exemplo
    if filtered_urls:
        print("\n=== EXEMPLOS DE URLs DE PRODUTOS ===")
        for i, url in enumerate(filtered_urls[:5]):
            print(f"{i+1}. {url}")
        if len(filtered_urls) > 5:
            print(f"... e mais {len(filtered_urls) - 5} URLs") 