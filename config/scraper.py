#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper para coletar dados nutricionais dos produtos da Perdigão
Extrai informações da tabela nutricional e cria um DataFrame
"""

import sys
sys.path.append('.')
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import logging
import json
from typing import Dict, Optional, List
from datetime import datetime
import os


class PerdigaoScraper:
    def __init__(self):
        """Inicializa o scraper com requests"""
        self.setup_logging()
        
        # Headers para simular navegador
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Mapeamento de campos nutricionais
        self.nutricional_mapping = {
            'Carboidratos (g)': 'CARBOIDRATOS (g)',
            'Proteínas (g)': 'PROTEINAS (g)',
            'Gorduras Totais (g)': 'GORDURAS_TOTAIS (g)',
            'Gorduras Saturadas (g)': 'GORDURAS_SATURADAS (g)',
            'Fibra Alimentar (g)': 'FIBRAS (g)',
            'Açúcares Totais (g)': 'ACUCARES (g)',
            'Sódio (mg)': 'SODIO (mg)'
        }
    
    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('scraper_perdigao.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Usa requests para obter o HTML da página
        """
        try:
            self.logger.info(f"Acessando página: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except Exception as e:
            self.logger.error(f"Erro ao carregar página: {e}")
            return None
    
    def extract_product_name(self, soup: BeautifulSoup) -> str:
        """Extrai o nome do produto da página"""
        try:
            # Buscar o título do produto
            title_element = soup.find('h1', class_='product-title')
            if title_element:
                return title_element.get_text(strip=True)
            
            # Fallback: buscar qualquer h1
            h1_element = soup.find('h1')
            if h1_element:
                return h1_element.get_text(strip=True)
            
            return "Nome não encontrado"
            
        except Exception as e:
            self.logger.error(f"Erro ao extrair nome do produto: {e}")
            return "Nome não encontrado"
    

    
    def extract_porcao(self, soup: BeautifulSoup) -> str:
        """Extrai a porção da tabela nutricional"""
        try:
            # Buscar a célula que contém "Porção"
            porcao_cells = soup.find_all('td', class_='nutricional-table-title')
            for cell in porcao_cells:
                text = cell.get_text(strip=True)
                if 'Porção' in text:
                    # Extrair apenas o valor (ex: "100g" de "Porção 100g")
                    match = re.search(r'Porção\s*(\d+g)', text)
                    if match:
                        return match.group(1)
            return "100g"  # Valor padrão
        except Exception as e:
            self.logger.error(f"Erro ao extrair porção: {e}")
            return "100g"
    
    def extract_nutritional_data(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extrai os dados nutricionais da tabela
        
        Returns:
            Dicionário com os valores nutricionais
        """
        nutritional_data = {}
        try:
            table = soup.find('table', class_='nutricional-table')
            if not table:
                self.logger.warning("Tabela nutricional não encontrada")
                return nutritional_data
            rows = table.find_all('tr')
            for row in rows:
                if row is not None:
                    cells = row.find_all('td', class_='nutricional-table-row')
                    if len(cells) >= 2:
                        nutrient_name = cells[0].get_text(strip=True)
                        nutrient_value = cells[1].get_text(strip=True)
                        # Calorias: qualquer campo que comece com 'Valor Energético', ignorando o que está entre parênteses
                        if re.match(r'^Valor Energético(\s*\(.*\))?$', nutrient_name):
                            nutritional_data['CALORIAS (kcal)'] = nutrient_value
                            self.logger.debug(f"Extraído: {nutrient_name} = {nutrient_value}")
                        elif nutrient_name in self.nutricional_mapping:
                            field_name = self.nutricional_mapping[nutrient_name]
                            nutritional_data[field_name] = nutrient_value
                            self.logger.debug(f"Extraído: {nutrient_name} = {nutrient_value}")
            if 'FIBRAS (g)' not in nutritional_data:
                nutritional_data['FIBRAS (g)'] = '0 g'
                self.logger.info("Fibra Alimentar não encontrada, definindo como 0 g")
            return nutritional_data
        except Exception as e:
            self.logger.error(f"Erro ao extrair dados nutricionais: {e}")
            return nutritional_data
    
    def clean_nutritional_value(self, value: str, field: str = "") -> str:
        """
        Limpa o valor nutricional removendo unidades e caracteres especiais
        Se for calorias, pega só o número antes de qualquer símbolo separador (=, /, \, |, &, %, #, etc.)
        
        Args:
            value: Valor original (ex: "236 kcal", "19 g", "500 mg", "235 = 987", "235/987")
            field: Nome do campo (para tratamento especial de calorias)
            
        Returns:
            Valor limpo (ex: "236", "19", "500")
        """
        try:
            value = value.strip()
            # Se for calorias, pegar só o valor antes de qualquer símbolo separador
            if field == 'CALORIAS (kcal)':
                # Pega só o que vem antes de qualquer símbolo separador
                value = re.split(r'[=\\/|&%#]', value)[0].strip()
            # Extrair apenas o primeiro número (com vírgula ou ponto)
            match = re.search(r'([\d,\.]+)', value)
            if match:
                cleaned = match.group(1).replace(',', '.')
                return cleaned
            return "0"
        except Exception as e:
            self.logger.error(f"Erro ao limpar valor nutricional '{value}': {e}")
            return "0"
    
    def scrape_product(self, url: str) -> Optional[Dict]:
        """
        Faz scraping completo de um produto
        
        Args:
            url: URL da página do produto
            
        Returns:
            Dicionário com todos os dados do produto ou None se houver erro
        """
        self.logger.info(f"Iniciando scraping do produto: {url}")
        
        # Obter conteúdo da página
        soup = self.get_page_content(url)
        if not soup:
            return None
        
        # Extrair dados básicos
        product_name = self.extract_product_name(soup)
        porcao = self.extract_porcao(soup)
        
        # Extrair dados nutricionais
        nutritional_data = self.extract_nutritional_data(soup)
        
        # Criar dicionário com todos os dados
        product_data = {
            'NOME_PRODUTO': product_name,
            'URL': url,
            'PORCAO (g)': porcao.replace('g', ''),  # Remover 'g' da porção
        }
        
        # Adicionar dados nutricionais limpos
        for field, value in nutritional_data.items():
            cleaned_value = self.clean_nutritional_value(value, field)
            product_data[field] = cleaned_value
        
        # Garantir que todos os campos existam
        required_fields = [
            'CALORIAS (kcal)', 'CARBOIDRATOS (g)', 'PROTEINAS (g)',
            'GORDURAS_TOTAIS (g)', 'GORDURAS_SATURADAS (g)', 'FIBRAS (g)',
            'ACUCARES (g)', 'SODIO (mg)'
        ]
        
        for field in required_fields:
            if field not in product_data:
                product_data[field] = "0"
                self.logger.warning(f"Campo {field} não encontrado, definindo como 0")
        
        self.logger.info(f"Scraping concluído para: {product_name}")
        return product_data
    
    def scrape_products(self, urls: List[str]) -> pd.DataFrame:
        """
        Faz scraping de múltiplos produtos e retorna um DataFrame
        
        Args:
            urls: Lista de URLs dos produtos
            
        Returns:
            DataFrame com todos os dados
        """
        all_products = []
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Processando produto {i}/{len(urls)}")
            
            product_data = self.scrape_product(url)
            if product_data:
                all_products.append(product_data)
            else:
                self.logger.error(f"Falha ao processar produto: {url}")
        
        # Criar DataFrame
        df = pd.DataFrame(all_products)
        
        # Ordenar colunas na ordem especificada
        column_order = [
            'NOME_PRODUTO', 'URL', 'PORCAO (g)',
            'CALORIAS (kcal)', 'CARBOIDRATOS (g)', 'PROTEINAS (g)',
            'GORDURAS_TOTAIS (g)', 'GORDURAS_SATURADAS (g)', 'FIBRAS (g)',
            'ACUCARES (g)', 'SODIO (mg)'
        ]
        
        # Reordenar colunas (apenas as que existem)
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        return df
    
    def save_dataframe(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Salva o DataFrame em arquivo CSV
        
        Args:
            df: DataFrame para salvar
            filename: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"produtos_perdigao_{timestamp}.csv"
        
        # Garantir que o arquivo tenha extensão .csv
        if filename and not filename.endswith('.csv'):
            filename += '.csv'
        
        # Salvar na pasta dados
        dados_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dados')
        os.makedirs(dados_dir, exist_ok=True)
        
        final_filename = filename if filename else "produto.csv"
        filepath = os.path.join(dados_dir, final_filename)
        
        try:
            df.to_csv(filepath, index=False, encoding='utf-8')
            self.logger.info(f"DataFrame salvo em: {filepath}")
            self.logger.info(f"Total de produtos: {len(df)}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar DataFrame: {e}")
            return ""


def main():
    """Função principal para teste"""
    scraper = PerdigaoScraper()
    
    # Caminho para o arquivo JSON com as URLs
    json_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dados', 'product_urls.json')
    
    print("🦆 SCRAPER PERDIGÃO - DADOS NUTRICIONAIS")
    print("=" * 50)
    
    # Verificar se o arquivo JSON existe
    if not os.path.exists(json_file):
        print(f"❌ Arquivo não encontrado: {json_file}")
        print("Execute primeiro o url_collector.py para gerar a lista de URLs")
        return
    
    # Carregar URLs do JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            urls = json.load(f)
        print(f"📋 Carregadas {len(urls)} URLs do arquivo: {json_file}")
    except Exception as e:
        print(f"❌ Erro ao carregar URLs do JSON: {e}")
        return
    
    if not urls:
        print("❌ Nenhuma URL encontrada no arquivo JSON")
        return
    
    # Fazer scraping de todos os produtos
    df = scraper.scrape_products(urls)
    
    if not df.empty:
        print("\n✅ Dados extraídos com sucesso!")
        print(f"\n📊 Total de produtos processados: {len(df)}")
        
        # Salvar com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"produtos_perdigao_{timestamp}.csv"
        filepath = scraper.save_dataframe(df, filename)
        
        if filepath:
            print(f"\n💾 Arquivo salvo em: {filepath}")
        else:
            print("\n❌ Erro ao salvar arquivo")
    else:
        print("\n❌ Falha ao extrair dados dos produtos")


if __name__ == "__main__":
    main() 