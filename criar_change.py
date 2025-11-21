#!/usr/bin/env python3
"""
Criar Change Request no ServiceNow associado ao DPR Model Release
Usa credenciais do arquivo .env
"""
import os
import sys
import requests
from pathlib import Path

# Carregar .env manualmente (sem dependencia externa)
def load_env():
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        print("Erro: Arquivo .env nao encontrado!")
        print("Crie o arquivo .env com as credenciais")
        sys.exit(1)

    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

load_env()

# Credenciais do .env
INSTANCE = os.environ.get('SERVICENOW_INSTANCE')
USERNAME = os.environ.get('SERVICENOW_USERNAME')
PASSWORD = os.environ.get('SERVICENOW_PASSWORD')
DPR_RELEASE_SYS_ID = os.environ.get('DPR_RELEASE_SYS_ID')
PHASE_SYS_ID = os.environ.get('DPR_PHASE_SYS_ID')

def criar_change(descricao):
    """Cria Change Request e associa ao DPR"""

    print("=" * 60)
    print("CRIAR CHANGE REQUEST")
    print("=" * 60)

    # 1. Criar CR
    print(f"\n1. Criando Change Request...")
    print(f"   Descricao: {descricao}")

    cr_payload = {
        "short_description": descricao,
        "description": f"Change criado via script\n\n{descricao}",
        "type": "standard",
        "priority": "3",
        "risk": "3",
        "impact": "3"
    }

    response = requests.post(
        f"https://{INSTANCE}/api/now/table/change_request",
        json=cr_payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        auth=(USERNAME, PASSWORD),
        timeout=30
    )

    if response.status_code not in [200, 201]:
        print(f"   ERRO: {response.status_code}")
        print(response.text[:200])
        return None

    result = response.json().get('result', {})
    cr_number = result.get('number')
    cr_sys_id = result.get('sys_id')

    print(f"   OK! CR: {cr_number}")

    # 2. Associar ao DPR
    print(f"\n2. Associando ao DPR Model Release...")

    rel_payload = {
        "change_request": cr_sys_id,
        "release": DPR_RELEASE_SYS_ID,
        "release_phase": PHASE_SYS_ID
    }

    rel_response = requests.post(
        f"https://{INSTANCE}/api/now/table/sn_dpr_model_release_phase_cr",
        json=rel_payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        auth=(USERNAME, PASSWORD),
        timeout=30
    )

    if rel_response.status_code not in [200, 201]:
        print(f"   ERRO: {rel_response.status_code}")
        return cr_number

    print(f"   OK! Associado ao DPR 'Ajust model'")

    # Resultado
    print("\n" + "=" * 60)
    print("SUCESSO!")
    print("=" * 60)
    print(f"CR: {cr_number}")
    print(f"Release: Ajust model")
    print(f"Phase: Development")
    print(f"\nLink: https://{INSTANCE}/nav_to.do?uri=change_request.do?sys_id={cr_sys_id}")

    return cr_number

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 criar_change.py \"Descricao da mudanca\"")
        print("\nExemplo:")
        print("  python3 criar_change.py \"Atualizar versao Streamlit para 2.3\"")
        sys.exit(1)

    descricao = sys.argv[1]
    criar_change(descricao)
