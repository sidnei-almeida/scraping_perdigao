#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para salvar o HTML da página do Mini Chicken Tradicional da Perdigão
"""

import requests
import os
from datetime import datetime


def salvar_html_produto():
    """Salva o HTML da página do Mini Chicken Tradicional"""
    
    # URL da página do produto
    url = "https://www.perdigao.com.br/produtos/empanados/todos-os-empanados/mini-chicken-tradicional-275g/"
    
    # Headers para simular um navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    print("🔍 Salvando HTML da página do Mini Chicken Tradicional...")
    print(f"📄 URL: {url}")
    
    try:
        # Fazer requisição
        print("📡 Fazendo requisição...")
        response = requests.get(url, headers=headers, timeout=30)
        
        # Verificar se a requisição foi bem-sucedida
        response.raise_for_status()
        
        # Informações da resposta
        print(f"✅ Status Code: {response.status_code}")
        print(f"📏 Tamanho: {len(response.content)} bytes")
        
        # Gerar nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mini_chicken_tradicional_{timestamp}.html"
        
        # Salvar arquivo
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"💾 Arquivo salvo: {filepath}")
        print(f"📊 Tamanho do arquivo: {len(response.text)} caracteres")
        print("✅ HTML salvo com sucesso!")
        
        return filepath
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("🦆 SCRAPER MINI CHICKEN TRADICIONAL - PERDIGÃO")
    print("=" * 60)
    
    arquivo_salvo = salvar_html_produto()
    
    if arquivo_salvo:
        print("\n🎉 Processo concluído com sucesso!")
        print(f"📁 Arquivo disponível em: {arquivo_salvo}")
    else:
        print("\n💥 Falha ao salvar o HTML. Verifique a conexão.") 