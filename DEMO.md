# GUIA DE DEMO - CI/CD com ServiceNow

## Links Importantes

| Recurso | URL |
|---------|-----|
| GitHub Actions | https://github.com/mlhoffmann/devopslab/actions |
| ServiceNow | https://mlhsouza.service-now.com |
| Streamlit App | https://devopslab-demo.streamlit.app |

## Credenciais ServiceNow

```
Usuario: xxxxx
Senha: xxxxx
```

---

# CENARIO 1: Deploy Automatico (sem aprovacao)

Este cenario mostra o deploy automatico SEM gate de aprovacao.

## Passo 1 - Disparar workflow manualmente

```bash
# Acesse GitHub Actions no navegador:
# https://github.com/mlhoffmann/devopslab/actions
#
# 1. Clique em "Streamlit Deploy Pipeline (Auto)"
# 2. Clique em "Run workflow" (botao azul a direita)
# 3. Clique no botao verde "Run workflow"
```

## Passo 2 - Acompanhar execucao

O workflow executa automaticamente:

```
Build (testes) --> ServiceNow_Change_Request --> Deploy_Streamlit
     |                      |                         |
     v                      v                         v
  ~1 min                Cria CR                   Deploy
                    (vai para Review)          automatico
```

## O que mostrar na demo:

1. **GitHub Actions**: Pipeline executando os jobs em sequencia
2. **ServiceNow**: CR criada e ja em estado "Review"
3. **Streamlit**: App atualizado com nova versao

---

# CENARIO 2: Deploy com Gate de Aprovacao

Este cenario mostra o deploy COM gate de aprovacao no ServiceNow.

## Passo 1 - Fazer uma alteracao no codigo

```bash
cd /Users/marcos.hoffmann/Dropbox/devops/devopslab-1

# Editar versao no streamlit_app.py (escolha uma versao)
# Exemplo: mudar para versao 3.0
```

Edite o arquivo `streamlit_app.py` e mude a linha da versao:
```python
st.info("**Produto:** ACME Americas DevOpsLab | **Versao:** 3.0 - Demo Gate Aprovacao")
```

## Passo 2 - Commit e Push

```bash
git add streamlit_app.py
git commit -m "Demo: teste gate de aprovacao v3.0"
git push origin main
```

## Passo 3 - Acompanhar no GitHub Actions

Acesse: https://github.com/mlhoffmann/devopslab/actions

O workflow "Streamlit Deploy com Aprovacao" sera acionado:

```
Build --> ServiceNow_Change_Request --> Wait_For_Approval --> Deploy
  |                |                          |                  |
  v                v                          v                  v
~1 min        Cria CR em              AGUARDANDO            So executa
             "Authorize"              APROVACAO!            apos aprovar
```

**IMPORTANTE**: O job `Wait_For_Approval` ficara em loop verificando o estado da CR a cada 30 segundos!

## Passo 4 - Mostrar CR no ServiceNow

1. Acesse: https://mlhsouza.service-now.com
2. Login: `xxx` / `xxxx`
3. Menu: Change > All
4. Encontre a CR criada (CHG00XXXXX)
5. **Observe**: CR esta no estado "Authorize"

## Passo 5 - Aprovar a Change Request

Na tela da CR no ServiceNow:

1. Clique no botao "Scheduled" (ou mude o estado para "Scheduled")
2. Salve a CR

## Passo 6 - Observar deploy continuar

Volte ao GitHub Actions:

1. O job `Wait_For_Approval` detectara a mudanca de estado
2. Mostrara: "CHANGE REQUEST APROVADA!"
3. O job `Deploy_Streamlit` sera executado automaticamente

## O que mostrar na demo:

1. **Terminal**: Commit e push do codigo
2. **GitHub Actions**: Pipeline parado em "Wait_For_Approval"
3. **ServiceNow**: CR em estado "Authorize" aguardando
4. **ServiceNow**: Aprovar a CR (mudar para "Scheduled")
5. **GitHub Actions**: Pipeline continua e faz deploy
6. **Streamlit**: App atualizado com nova versao

---

# Estados do ServiceNow Change Request

| Estado | Codigo | Descricao |
|--------|--------|-----------|
| New | -5 | CR recem criada |
| Assess | -4 | Em avaliacao |
| **Authorize** | **-3** | **Aguardando aprovacao** |
| **Scheduled** | **-1** | **Aprovada - libera deploy** |
| Implement | -2 | Em implementacao |
| Review | 0 | Em revisao |
| Closed | 3 | Fechada |
| Canceled | 4 | Cancelada |

---

# Fluxo Visual

```
                    CENARIO 1 (Auto)
                    ================
Push/Manual --> Build --> CR (Review) --> Deploy --> Fim
                              |
                              v
                         Sem espera


                    CENARIO 2 (Aprovacao)
                    =====================
Push --> Build --> CR (Authorize) --> Wait_For_Approval --> Deploy --> Fim
                        |                    |
                        v                    v
                  Aguardando           Polling 30s
                  aprovacao            ate aprovar
                        |                    |
                        +-----> ServiceNow --+
                                Aprovar CR
```

---

# Comandos Uteis

## Ver status do git
```bash
git status
```

## Ver logs recentes
```bash
git log --oneline -5
```

## Criar CR via terminal (script local)
```bash
python3 criar_change.py "Descricao da mudanca"
```

## Ver workflows ativos
```bash
ls .github/workflows/*.yml
```
