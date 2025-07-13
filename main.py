#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🦆 SCRAPING PERDIGÃO - Interface CLI
=====================================
Sistema completo para coleta de dados nutricionais dos produtos da Perdigão

FUNCIONALIDADES:
1. 🕷️ Coletar URLs dos produtos
2. 📊 Extrair dados nutricionais
3. 🚀 Coleta completa (URLs + dados)
4. 📁 Gerenciar arquivos gerados
"""

import os
import sys
import time
import glob
import subprocess
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================================
# 🎨 SISTEMA DE CORES ANSI PARA TERMINAL
# ============================================================================
class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    MAGENTA = '\033[95m'
    BRANCO = '\033[97m'

# ============================================================================
# 🛠️ FUNÇÕES UTILITÁRIAS
# ============================================================================
def limpar_terminal():
    """Limpa o terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    """Exibe o banner principal do programa"""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🦆 SCRAPING PERDIGÃO                      ║
║                                                              ║
║              Coleta de Dados Nutricionais v1.0              ║
║                                                              ║
║  🕷️  Coleta URLs dos produtos                               ║
║  📊 Extração de dados nutricionais                          ║
║  🚀 Sistema completo de scraping                            ║
╚══════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def mostrar_barra_progresso(texto: str, duracao: float = 2.0):
    """Exibe uma barra de progresso animada"""
    print(f"\n{Cores.AMARELO}⏳ {texto}...{Cores.RESET}")
    barra_tamanho = 40
    for i in range(barra_tamanho + 1):
        progresso = i / barra_tamanho
        barra = "█" * i + "░" * (barra_tamanho - i)
        porcentagem = int(progresso * 100)
        print(f"\r{Cores.VERDE}[{barra}] {porcentagem}%{Cores.RESET}", end="", flush=True)
        time.sleep(duracao / barra_tamanho)
    print()

def mostrar_menu():
    """Exibe o menu principal"""
    menu = f"""
{Cores.AZUL}{Cores.BOLD}═══════════════════ MENU PRINCIPAL ═══════════════════{Cores.RESET}

{Cores.VERDE}🚀 OPERAÇÕES PRINCIPAIS:{Cores.RESET}
  {Cores.AMARELO}1.{Cores.RESET} 🕷️  {Cores.BRANCO}Coletar URLs{Cores.RESET} - Extrair URLs dos produtos Perdigão
  {Cores.AMARELO}2.{Cores.RESET} 📊 {Cores.BRANCO}Extrair Dados{Cores.RESET} - Coletar dados nutricionais
  {Cores.AMARELO}3.{Cores.RESET} 🚀 {Cores.BRANCO}Coleta Completa{Cores.RESET} - URLs + dados nutricionais

{Cores.VERDE}📁 GERENCIAR DADOS:{Cores.RESET}
  {Cores.AMARELO}4.{Cores.RESET} 📋 {Cores.BRANCO}Ver Arquivos{Cores.RESET} - Lista arquivos gerados
  {Cores.AMARELO}5.{Cores.RESET} 🗑️  {Cores.BRANCO}Limpar Dados{Cores.RESET} - Remove arquivos antigos

{Cores.VERDE}ℹ️  INFORMAÇÕES:{Cores.RESET}
  {Cores.AMARELO}6.{Cores.RESET} 📖 {Cores.BRANCO}Sobre o Programa{Cores.RESET} - Informações e estatísticas
  {Cores.AMARELO}7.{Cores.RESET} ❌ {Cores.BRANCO}Sair{Cores.RESET} - Encerrar programa

{Cores.AZUL}══════════════════════════════════════════════════════{Cores.RESET}
"""
    print(menu)

def obter_escolha() -> str:
    """Obtém a escolha do usuário"""
    try:
        escolha = input(f"{Cores.MAGENTA}👉 Digite sua opção (1-7): {Cores.RESET}").strip()
        return escolha
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Programa interrompido pelo usuário{Cores.RESET}")
        sys.exit(0)

# ============================================================================
# 🎯 FUNÇÕES ESPECÍFICAS DO PROJETO
# ============================================================================

def executar_coleta_urls():
    """Coleta URLs dos produtos da Perdigão"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🕷️  COLETANDO URLs DOS PRODUTOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.VERDE}✅ Configurações:{Cores.RESET}")
    print(f"   📊 Seções: {Cores.AMARELO}12 categorias de produtos{Cores.RESET}")
    print(f"   📁 Saída: {Cores.AMARELO}dados/product_urls.json{Cores.RESET}")
    print(f"   ⏱️  Tempo estimado: {Cores.AMARELO}2-3 minutos{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            mostrar_barra_progresso("Iniciando coleta de URLs", 1.0)
            
            # Executar o coletor de URLs
            resultado = subprocess.run([
                sys.executable, "config/url_collector.py"
            ], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                print(f"{Cores.VERDE}✅ URLs coletadas com sucesso!{Cores.RESET}")
                
                # Verificar se o arquivo foi criado
                if os.path.exists("dados/product_urls.json"):
                    with open("dados/product_urls.json", 'r', encoding='utf-8') as f:
                        import json
                        urls = json.load(f)
                    print(f"{Cores.VERDE}📊 Total de URLs coletadas: {len(urls)}{Cores.RESET}")
                else:
                    print(f"{Cores.VERMELHO}❌ Arquivo de URLs não foi criado{Cores.RESET}")
            else:
                print(f"{Cores.VERMELHO}❌ Erro na coleta: {resultado.stderr}{Cores.RESET}")
                
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def executar_extracao_dados():
    """Extrai dados nutricionais dos produtos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📊 EXTRAINDO DADOS NUTRICIONAIS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    # Verificar se existe arquivo de URLs
    if not os.path.exists("dados/product_urls.json"):
        print(f"{Cores.VERMELHO}❌ Arquivo de URLs não encontrado!{Cores.RESET}")
        print(f"{Cores.AMARELO}💡 Execute primeiro a opção 1 para coletar as URLs{Cores.RESET}")
        return
    
    # Carregar URLs
    try:
        with open("dados/product_urls.json", 'r', encoding='utf-8') as f:
            import json
            urls = json.load(f)
        
        print(f"\n{Cores.VERDE}✅ Configurações:{Cores.RESET}")
        print(f"   📊 URLs carregadas: {Cores.AMARELO}{len(urls)}{Cores.RESET}")
        print(f"   📁 Saída: {Cores.AMARELO}dados/produtos_perdigao_TIMESTAMP.csv{Cores.RESET}")
        print(f"   ⏱️  Tempo estimado: {Cores.AMARELO}5-10 minutos{Cores.RESET}")
        
        confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
        
        if confirmar in ['s', 'sim', 'y', 'yes']:
            try:
                mostrar_barra_progresso("Iniciando extração de dados", 1.0)
                
                # Executar o scraper
                resultado = subprocess.run([
                    sys.executable, "config/scraper.py"
                ], capture_output=True, text=True)
                
                if resultado.returncode == 0:
                    print(f"{Cores.VERDE}✅ Dados extraídos com sucesso!{Cores.RESET}")
                    
                    # Verificar arquivos CSV criados
                    csv_files = glob.glob("dados/produtos_perdigao_*.csv")
                    if csv_files:
                        latest_file = max(csv_files, key=os.path.getctime)
                        print(f"{Cores.VERDE}📁 Arquivo criado: {latest_file}{Cores.RESET}")
                    else:
                        print(f"{Cores.VERMELHO}❌ Nenhum arquivo CSV foi criado{Cores.RESET}")
                else:
                    print(f"{Cores.VERMELHO}❌ Erro na extração: {resultado.stderr}{Cores.RESET}")
                    
            except Exception as e:
                print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
        else:
            print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")
            
    except Exception as e:
        print(f"{Cores.VERMELHO}❌ Erro ao carregar URLs: {e}{Cores.RESET}")

def executar_coleta_completa():
    """Executa coleta completa: URLs + dados nutricionais"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🚀 COLETA COMPLETA{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Esta operação pode demorar {Cores.VERMELHO}10-15 minutos{Cores.RESET}")
    print(f"   • Serão executadas as etapas 1 e 2 em sequência")
    print(f"   • Certifique-se de ter uma conexão estável com a internet")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            # Etapa 1: Coletar URLs
            print(f"\n{Cores.VERDE}🕷️  ETAPA 1: Coletando URLs...{Cores.RESET}")
            mostrar_barra_progresso("Coletando URLs dos produtos", 2.0)
            
            resultado_urls = subprocess.run([
                sys.executable, "config/url_collector.py"
            ], capture_output=True, text=True)
            
            if resultado_urls.returncode != 0:
                print(f"{Cores.VERMELHO}❌ Erro na coleta de URLs: {resultado_urls.stderr}{Cores.RESET}")
                return
            
            print(f"{Cores.VERDE}✅ URLs coletadas com sucesso!{Cores.RESET}")
            
            # Etapa 2: Extrair dados
            print(f"\n{Cores.VERDE}📊 ETAPA 2: Extraindo dados nutricionais...{Cores.RESET}")
            mostrar_barra_progresso("Extraindo dados nutricionais", 3.0)
            
            resultado_dados = subprocess.run([
                sys.executable, "config/scraper.py"
            ], capture_output=True, text=True)
            
            if resultado_dados.returncode == 0:
                print(f"{Cores.VERDE}✅ Coleta completa finalizada com sucesso!{Cores.RESET}")
                
                # Verificar arquivos criados
                if os.path.exists("dados/product_urls.json"):
                    with open("dados/product_urls.json", 'r', encoding='utf-8') as f:
                        import json
                        urls = json.load(f)
                    print(f"{Cores.VERDE}📊 URLs coletadas: {len(urls)}{Cores.RESET}")
                
                csv_files = glob.glob("dados/produtos_perdigao_*.csv")
                if csv_files:
                    latest_file = max(csv_files, key=os.path.getctime)
                    print(f"{Cores.VERDE}📁 Arquivo de dados: {latest_file}{Cores.RESET}")
            else:
                print(f"{Cores.VERMELHO}❌ Erro na extração de dados: {resultado_dados.stderr}{Cores.RESET}")
                
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def listar_arquivos_gerados():
    """Lista arquivos gerados pelo programa"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 ARQUIVOS GERADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    pasta_dados = "dados"
    
    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return
    
    # Listar arquivos JSON
    json_files = glob.glob(f"{pasta_dados}/*.json")
    csv_files = glob.glob(f"{pasta_dados}/*.csv")
    
    if not json_files and not csv_files:
        print(f"{Cores.AMARELO}📄 Nenhum arquivo encontrado em '{pasta_dados}'{Cores.RESET}")
        return
    
    total_arquivos = len(json_files) + len(csv_files)
    print(f"\n{Cores.VERDE}📊 Total de arquivos: {total_arquivos}{Cores.RESET}\n")
    
    # Listar arquivos JSON
    if json_files:
        print(f"{Cores.CIANO}📄 Arquivos JSON:{Cores.RESET}")
        for i, arquivo in enumerate(sorted(json_files, reverse=True), 1):
            nome_arquivo = os.path.basename(arquivo)
            tamanho = os.path.getsize(arquivo)
            data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))
            
            if tamanho < 1024:
                tamanho_str = f"{tamanho} B"
            elif tamanho < 1024 * 1024:
                tamanho_str = f"{tamanho / 1024:.1f} KB"
            else:
                tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"
            
            print(f"{Cores.AMARELO}{i:2d}.{Cores.RESET} {Cores.BRANCO}{nome_arquivo}{Cores.RESET}")
            print(f"     📅 {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"     📏 {tamanho_str}")
            print()
    
    # Listar arquivos CSV
    if csv_files:
        print(f"{Cores.CIANO}📊 Arquivos CSV:{Cores.RESET}")
        for i, arquivo in enumerate(sorted(csv_files, reverse=True), 1):
            nome_arquivo = os.path.basename(arquivo)
            tamanho = os.path.getsize(arquivo)
            data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))
            
            if tamanho < 1024:
                tamanho_str = f"{tamanho} B"
            elif tamanho < 1024 * 1024:
                tamanho_str = f"{tamanho / 1024:.1f} KB"
            else:
                tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"
            
            print(f"{Cores.AMARELO}{i:2d}.{Cores.RESET} {Cores.BRANCO}{nome_arquivo}{Cores.RESET}")
            print(f"     📅 {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"     📏 {tamanho_str}")
            print()

def limpar_dados_antigos():
    """Remove arquivos antigos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🗑️  LIMPAR DADOS ANTIGOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    pasta_dados = "dados"
    
    if not os.path.exists(pasta_dados):
        print(f"{Cores.AMARELO}📁 Pasta '{pasta_dados}' não encontrada{Cores.RESET}")
        return
    
    json_files = glob.glob(f"{pasta_dados}/*.json")
    csv_files = glob.glob(f"{pasta_dados}/*.csv")
    total_arquivos = len(json_files) + len(csv_files)
    
    if total_arquivos == 0:
        print(f"{Cores.VERDE}✅ Nenhum arquivo para limpar{Cores.RESET}")
        return
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Serão removidos {Cores.VERMELHO}{total_arquivos} arquivos{Cores.RESET}")
    print(f"   • Esta ação {Cores.VERMELHO}NÃO PODE ser desfeita{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Tem certeza? Digite 'CONFIRMAR' para prosseguir: {Cores.RESET}")
    
    if confirmar == "CONFIRMAR":
        try:
            for arquivo in json_files + csv_files:
                os.remove(arquivo)
            print(f"\n{Cores.VERDE}✅ {total_arquivos} arquivos removidos com sucesso!{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro ao remover arquivos: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def mostrar_sobre():
    """Mostra informações sobre o programa"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📖 SOBRE O PROGRAMA{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.VERDE}🦆 SCRAPING PERDIGÃO{Cores.RESET}")
    print(f"   Versão: {Cores.AMARELO}1.0{Cores.RESET}")
    print(f"   Desenvolvido para coleta de dados nutricionais")
    print(f"   dos produtos da Perdigão")
    
    print(f"\n{Cores.VERDE}📊 FUNCIONALIDADES:{Cores.RESET}")
    print(f"   🕷️  Coleta URLs de 12 categorias de produtos")
    print(f"   📊 Extração de dados nutricionais completos")
    print(f"   🚀 Sistema automatizado de scraping")
    
    print(f"\n{Cores.VERDE}📁 ESTRUTURA:{Cores.RESET}")
    print(f"   config/url_collector.py - Coletor de URLs")
    print(f"   config/scraper.py - Extrator de dados")
    print(f"   dados/ - Pasta de saída dos arquivos")
    
    print(f"\n{Cores.VERDE}📋 DADOS COLETADOS:{Cores.RESET}")
    print(f"   • Nome do produto")
    print(f"   • URL do produto")
    print(f"   • Categoria")
    print(f"   • Porção (g)")
    print(f"   • Calorias (kcal)")
    print(f"   • Carboidratos (g)")
    print(f"   • Proteínas (g)")
    print(f"   • Gorduras totais (g)")
    print(f"   • Gorduras saturadas (g)")
    print(f"   • Fibras (g)")
    print(f"   • Açúcares (g)")
    print(f"   • Sódio (mg)")
    
    print(f"\n{Cores.VERDE}⚡ TECNOLOGIAS:{Cores.RESET}")
    print(f"   • Python 3.13")
    print(f"   • Requests + BeautifulSoup")
    print(f"   • Pandas para manipulação de dados")
    
    # Estatísticas dos arquivos
    pasta_dados = "dados"
    if os.path.exists(pasta_dados):
        json_files = glob.glob(f"{pasta_dados}/*.json")
        csv_files = glob.glob(f"{pasta_dados}/*.csv")
        
        print(f"\n{Cores.VERDE}📈 ESTATÍSTICAS:{Cores.RESET}")
        print(f"   📄 Arquivos JSON: {len(json_files)}")
        print(f"   📊 Arquivos CSV: {len(csv_files)}")
        
        if json_files:
            latest_json = max(json_files, key=os.path.getctime)
            with open(latest_json, 'r', encoding='utf-8') as f:
                import json
                urls = json.load(f)
            print(f"   🕷️  URLs coletadas: {len(urls)}")

def pausar():
    """Pausa a execução para o usuário ler"""
    input(f"\n{Cores.MAGENTA}Pressione ENTER para continuar...{Cores.RESET}")

def main():
    """Função principal do programa"""
    while True:
        limpar_terminal()
        mostrar_banner()
        mostrar_menu()
        
        escolha = obter_escolha()
        
        if escolha == "1":
            executar_coleta_urls()
        elif escolha == "2":
            executar_extracao_dados()
        elif escolha == "3":
            executar_coleta_completa()
        elif escolha == "4":
            listar_arquivos_gerados()
        elif escolha == "5":
            limpar_dados_antigos()
        elif escolha == "6":
            mostrar_sobre()
        elif escolha == "7":
            print(f"\n{Cores.VERDE}👋 Obrigado por usar o Scraping Perdigão!{Cores.RESET}")
            break
        else:
            print(f"\n{Cores.VERMELHO}❌ Opção inválida! Digite um número de 1 a 7.{Cores.RESET}")
        
        pausar()

if __name__ == "__main__":
    main() 