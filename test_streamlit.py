import pytest
import os
import sys


def test_streamlit_app_exists():
    """Verifica se o arquivo streamlit_app.py existe"""
    assert os.path.exists('streamlit_app.py'), "streamlit_app.py deve existir"


def test_streamlit_app_imports():
    """Verifica se o streamlit pode ser importado"""
    try:
        import streamlit
        assert True
    except ImportError:
        assert False, "Streamlit deve ser importável"


def test_streamlit_app_content():
    """Verifica se o arquivo contém conteúdo válido"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert 'streamlit' in content, "Arquivo deve importar streamlit"
        assert 'st.title' in content or 'st.write' in content, "Arquivo deve usar componentes Streamlit"


def test_streamlit_app_has_page_config():
    """Verifica se tem configuração de página"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert 'st.set_page_config' in content, "Deve configurar a página"
        assert 'page_title' in content, "Deve ter título da página"
        assert 'page_icon' in content, "Deve ter ícone da página"


def test_streamlit_app_has_title():
    """Verifica se tem título principal"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert 'st.title' in content, "Deve ter título"
        assert 'Petrobras' in content, "Título deve conter 'Petrobras'"


def test_streamlit_app_has_metrics():
    """Verifica se tem métricas"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert 'st.metric' in content, "Deve ter métricas"
        assert 'st.columns' in content, "Deve usar colunas"


def test_streamlit_app_has_product_info():
    """Verifica se tem informação do produto"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert 'ACME Americas DevOpsLab' in content, "Deve mencionar o produto"
        assert 'st.info' in content, "Deve usar st.info para destacar produto"


def test_streamlit_app_has_description():
    """Verifica se tem descrição do projeto"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert 'pipeline CI/CD' in content, "Deve mencionar pipeline CI/CD"
        assert 'ServiceNow DPR' in content, "Deve mencionar ServiceNow DPR"
        assert 'GitHub Actions' in content, "Deve mencionar GitHub Actions"


def test_streamlit_app_has_footer():
    """Verifica se tem footer"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert 'st.caption' in content, "Deve ter caption para footer"
        assert 'DevOps Lab' in content, "Footer deve conter 'DevOps Lab'"


def test_streamlit_app_has_coverage_mention():
    """Verifica se menciona cobertura de testes"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert '100% coverage' in content or 'coverage' in content.lower(), "Deve mencionar coverage"


def test_streamlit_app_has_sections():
    """Verifica se tem seções organizadas"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert 'st.subheader' in content, "Deve ter sub-cabeçalhos"
        assert 'st.markdown' in content, "Deve usar markdown para separadores"


def test_streamlit_app_mentions_streamlit_cloud():
    """Verifica se menciona Streamlit Cloud"""
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
        assert 'Streamlit Cloud' in content or 'Streamlit' in content, "Deve mencionar plataforma Streamlit"


def test_streamlit_app_code_structure():
    """Verifica estrutura do código"""
    with open('streamlit_app.py', 'r') as f:
        lines = f.readlines()

        # Deve ter importação no início
        assert any('import streamlit' in line for line in lines[:10]), "Import deve estar no início"

        # Deve ter comentários
        assert any('#' in line for line in lines), "Deve ter comentários"

        # Deve ter múltiplas chamadas streamlit
        st_calls = sum(1 for line in lines if 'st.' in line)
        assert st_calls >= 10, f"Deve ter pelo menos 10 chamadas st.* (encontrado: {st_calls})"
