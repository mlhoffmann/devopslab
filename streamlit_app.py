import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Demo Petrobras CI/CD",
    page_icon="🚀",
    layout="centered"
)

# Título principal
st.title("🚀 Demo Petrobras CI/CD Hoffmann Teste 21/11!")
st.info("**Produto:** ACME Americas DevOpsLab | **Versão:** 5.0 - Teste Authorize Gate")
st.success("✅ ServiceNow DPR Integration Active")

# Informações do projeto
st.markdown("---")
st.subheader("Informações do Deploy")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Plataforma", value="Streamlit Cloud")
    st.metric(label="Pipeline", value="GitHub Actions")

with col2:
    st.metric(label="Controle de Mudança", value="ServiceNow DPR")
    st.metric(label="Status", value="✅ Ativo")

# Seção sobre o projeto
st.markdown("---")
st.subheader("📋 Sobre o Projeto")
st.write("""
Este projeto demonstra um pipeline CI/CD completo com:
- ✅ Testes automatizados com 99% coverage
- 🔍 Análise de código com SonarCloud
- 🎯 Deploy automático no Streamlit
- 📝 Integração com ServiceNow para controle de mudanças
""")

# Footer
st.markdown("---")
st.caption("DevOps Lab - Desenvolvido com Streamlit | Petrobras CI/CD")
