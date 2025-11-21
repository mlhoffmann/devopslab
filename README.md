# DevOps Lab - CI/CD com ServiceNow Integration

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mlhoffmann_devopslab&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mlhoffmann_devopslab)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mlhoffmann_devopslab&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mlhoffmann_devopslab)
[![DevOpsLab Pipeline](https://github.com/mlhoffmann/devopslab/actions/workflows/streamlit-deploy.yml/badge.svg)](https://github.com/mlhoffmann/devopslab/actions/workflows/streamlit-deploy.yml)

Pipeline CI/CD completa com integracão ServiceNow DPR (Digital Product Release) e deploy no Streamlit Cloud. Demonstra dois cenarios: deploy automatico e deploy com gate de aprovacao.

---

## Indice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Pre-requisitos](#pre-requisitos)
- [Configuracao](#configuracao)
- [Como Usar](#como-usar)
- [Guia de Demo](#guia-de-demo)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Troubleshooting](#troubleshooting)

---

## Sobre o Projeto

Este projeto demonstra uma pipeline DevOps completa com:

| Funcionalidade | Descricao |
|----------------|-----------|
| Testes Automatizados | Pytest com cobertura de codigo |
| Analise de Qualidade | Integracao com SonarCloud |
| Controle de Mudancas | ServiceNow Change Request + DPR |
| Gate de Aprovacao | Deploy aguarda aprovacao no ServiceNow |
| Deploy Automatico | Streamlit Cloud |
| CI/CD | GitHub Actions com multiplos stages |

### Modos de Deploy

| Modo | Descricao | Uso |
|------|-----------|-----|
| **auto** | Deploy direto sem esperar aprovacao | Ambientes de desenvolvimento |
| **com_aprovacao** | Aguarda CR ser aprovada no ServiceNow | Ambientes de producao |

---

## Arquitetura

### Fluxo Automatico
```
Push → Build → Testes → SonarCloud → CR criada → Deploy → CR atualizada
```

### Fluxo com Aprovacao
```
Push → Build → Testes → SonarCloud → CR criada (Authorize)
                                          ↓
                                   [Aguarda aprovacao]
                                          ↓
                              CR aprovada (Scheduled)
                                          ↓
                                       Deploy
```

### Diagrama de Jobs

```
┌─────────┐    ┌─────────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│  Build  │───>│ ServiceNow_Change   │───>│ Wait_For_Approval│───>│ Deploy_Com_Aprovacao│
│         │    │     _Request        │    │  (se necessario) │    │                     │
└─────────┘    └─────────────────────┘    └──────────────────┘    └─────────────────────┘
                                                   │
                                                   v
                                          ┌──────────────┐
                                          │ Deploy_Auto  │
                                          │ (se auto)    │
                                          └──────────────┘
```

---

## Pre-requisitos

### Contas Necessarias

1. **GitHub** - Repositorio do codigo
2. **ServiceNow** - Instancia com modulo Change Management e DPR
3. **SonarCloud** - Analise de qualidade (opcional)
4. **Streamlit Cloud** - Deploy da aplicacao

### Ferramentas Locais

```bash
# Python 3.11+
python --version

# Git
git --version

# Pip
pip --version
```

---

## Configuracao

### 1. Fork/Clone do Repositorio

```bash
git clone https://github.com/SEU_USUARIO/devopslab.git
cd devopslab
```

### 2. GitHub Secrets

Configure os seguintes secrets em **Settings > Secrets and variables > Actions**:

| Secret | Descricao | Exemplo |
|--------|-----------|---------|
| `SERVICENOW_INSTANCE` | URL da instancia ServiceNow (sem https://) | `sua-instancia.service-now.com` |
| `SERVICENOW_USERNAME` | Usuario com permissao para criar Change Requests | `admin` |
| `SERVICENOW_PASSWORD` | Senha do usuario | `********` |
| `SONAR_TOKEN` | Token do SonarCloud (opcional) | `sqa_xxxxx` |

### 3. ServiceNow - DPR Model Release

Para associar as Change Requests ao DPR, voce precisa dos sys_ids:

```
DPR_RELEASE_SYS_ID  = sys_id do Model Release
DPR_PHASE_SYS_ID    = sys_id da Phase (ex: Development)
```

**Como obter os sys_ids:**

1. Acesse sua instancia ServiceNow
2. Navegue ate **Digital Product Release > Model Releases**
3. Abra o release desejado
4. Copie o `sys_id` da URL (parametro `sys_id=xxxxx`)
5. Repita para a Phase desejada

**Atualize no workflow** (`.github/workflows/streamlit-deploy.yml`):

```yaml
DPR_RELEASE_SYS_ID="SEU_RELEASE_SYS_ID"
PHASE_SYS_ID="SEU_PHASE_SYS_ID"
```

### 4. SonarCloud (Opcional)

1. Acesse [sonarcloud.io](https://sonarcloud.io)
2. Importe seu repositorio
3. Atualize `sonar-project.properties`:

```properties
sonar.projectKey=SEU_USUARIO_SEU_PROJETO
sonar.organization=SEU_USUARIO
```

### 5. Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte seu repositorio GitHub
3. Configure:
   - **Main file path**: `streamlit_app.py`
   - **Branch**: `main`

---

## Como Usar

### Instalacao Local

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Executar aplicacao
streamlit run streamlit_app.py

# Executar testes
pytest test.py test_streamlit.py -v

# Executar com coverage
coverage run -m pytest test.py test_streamlit.py
coverage report -m
```

### Criar Change Request via Terminal

```bash
# Configurar variaveis de ambiente
export SERVICENOW_INSTANCE="sua-instancia.service-now.com"
export SERVICENOW_USERNAME="seu-usuario"
export SERVICENOW_PASSWORD="sua-senha"
export DPR_RELEASE_SYS_ID="sys_id_do_release"
export DPR_PHASE_SYS_ID="sys_id_da_phase"

# Executar script
python criar_change.py "Descricao da mudanca"
```

---

## Guia de Demo

### Cenario 1: Deploy Automatico

1. Acesse: **GitHub Actions** > **Streamlit Deploy Pipeline**
2. Clique em **Run workflow**
3. Selecione modo: **auto**
4. Clique em **Run workflow**

**O que acontece:**
- Build e testes executam
- Change Request e criada no ServiceNow
- Deploy acontece automaticamente (sem esperar aprovacao)
- CR vai para estado Review

### Cenario 2: Deploy com Gate de Aprovacao

1. Acesse: **GitHub Actions** > **Streamlit Deploy Pipeline**
2. Clique em **Run workflow**
3. Selecione modo: **com_aprovacao**
4. Clique em **Run workflow**

**O que acontece:**
- Build e testes executam
- Change Request e criada no ServiceNow em estado **Authorize**
- Job **Wait_For_Approval** fica aguardando (polling a cada 30s)

5. Acesse o **ServiceNow**
6. Encontre a CR criada (Change > All)
7. Mude o estado de **Authorize** para **Scheduled**
8. Salve

**O que acontece:**
- Workflow detecta a aprovacao
- Deploy e executado
- CR vai para estado Review

### Estados do ServiceNow Change Request

| Estado | Codigo | Descricao |
|--------|--------|-----------|
| New | -5 | CR recem criada |
| Assess | -4 | Em avaliacao |
| **Authorize** | **-3** | Aguardando aprovacao |
| **Scheduled** | **-1** | Aprovada - libera deploy |
| Implement | -2 | Em implementacao |
| Review | 0 | Em revisao |
| Closed | 3 | Fechada |
| Canceled | 4 | Cancelada |

---

## Estrutura do Projeto

```
devopslab/
├── .github/
│   └── workflows/
│       └── streamlit-deploy.yml    # Workflow principal
├── streamlit_app.py                # Aplicacao Streamlit
├── app.py                          # Aplicacao Flask (legado)
├── test.py                         # Testes Flask
├── test_streamlit.py               # Testes Streamlit
├── criar_change.py                 # Script para criar CR via terminal
├── requirements.txt                # Dependencias Python
├── sonar-project.properties        # Configuracao SonarCloud
├── README.md                       # Este arquivo
└── DEMO.md                         # Guia rapido de demo
```

### Arquivos Principais

| Arquivo | Descricao |
|---------|-----------|
| `streamlit-deploy.yml` | Workflow com dois modos (auto/com_aprovacao) |
| `streamlit_app.py` | Interface web da aplicacao |
| `criar_change.py` | Cria CR via terminal usando .env |
| `sonar-project.properties` | Configuracao do SonarCloud |

---

## Troubleshooting

### Erro: "Unable to process file command 'output'"

**Causa:** Mensagem de commit com multiplas linhas quebra o GITHUB_OUTPUT.

**Solucao:** O workflow ja usa `git log -1 --pretty=%s` (apenas subject).

### Erro: CR nao e criada

**Verificar:**
1. Secrets configurados corretamente
2. Usuario tem permissao no ServiceNow
3. Instancia ServiceNow esta acessivel

### Erro: Wait_For_Approval nao detecta aprovacao

**Verificar:**
1. CR foi movida para estado **Scheduled** (-1) ou **Implement** (-2)
2. Nao apenas clicar no botao, mas **salvar** a CR

### Deploy nao atualiza o Streamlit

**Verificar:**
1. Streamlit Cloud esta conectado ao repositorio
2. Branch configurada e `main`
3. Arquivo principal e `streamlit_app.py`

---

## Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudancas (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## Licenca

Este projeto esta sob a licenca MIT.

---

## Autor

Marcos Hoffmann

---

**DevOps Lab** - CI/CD com ServiceNow Integration
