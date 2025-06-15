import requests
import pandas as pd
from tqdm import tqdm
import os
from dotenv import load_dotenv
import time

# Configurações
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CSV_PATH = "/Users/fabio/Library/Mobile Documents/com~apple~CloudDocs/VSCode/PROJETO-ML/01-Introducao-ML/data/ieee-cis-fraud/processed/dicionario_dados.csv"
PARQUET_PATH = "/Users/fabio/Library/Mobile Documents/com~apple~CloudDocs/VSCode/PROJETO-ML/01-Introducao-ML/data/ieee-cis-fraud/processed/dicionario_dados.parquet"
DATA_PATH = "/Users/fabio/Library/Mobile Documents/com~apple~CloudDocs/VSCode/PROJETO-ML/01-Introducao-ML/data/ieee-cis-fraud/processed/dataset_enriquecido.parquet"

def format_description(text):
    """Adiciona aspas e escapa caracteres especiais"""
    if pd.isna(text) or text is None:
        return '""'  # Retorna aspas vazias para nulos
    # Remove quebras de linha e espaços extras antes de formatar
    cleaned_text = str(text).replace('\\n', ' ').replace('\\r', '').strip()
    return f'"{cleaned_text.replace("\"", "\"\"")}"'

def generate_column_description(col_name, dtype, nunique, nulls, avg_mode):
    prompt = f"""
    **Persona:** Engenheiro de Dados Sênior criando metadados para um Data Warehouse de detecção de fraudes.
    **Contexto:** Dataset IEEE-CIS Fraud Detection.
    **Coluna para Análise:** '{col_name}'
        - Tipo: {dtype}
        - Únicos: {nunique}
        - Nulos: {nulls}
        - {'Média' if pd.api.types.is_numeric_dtype(dtype) else 'Moda'}: {avg_mode}

    **Tarefa:** Gere uma descrição técnica para a coluna '{col_name}'.
    **Formato de Saída OBRIGATÓRIO (string única, separada por '|'):**
    "Significado Principal da Coluna | Principal Uso em Detecção de Fraude | Relações/Insights Chave com Outras Features"

    **Restrições CRÍTICAS:**
    1.  **String ÚNICA**: A saída DEVE ser uma única linha de texto.
    2.  **Separador Pipe (|)**: Use '|' para separar as 3 partes.
    3.  **Concisão Extrema**: Cada parte deve ser muito breve. O total NÃO deve exceder 180 caracteres.
    4.  **SEM FORMATACÃO**: NÃO use Markdown (sem **, *, listas, etc.), HTML, quebras de linha, ou qualquer formatação especial.
    5.  **Linguagem Técnica Direta**: Foco em ETL, engenharia de dados e valor para o negócio.

    **Exemplo de Saída CORRETA para 'TransactionAmt':**
    "Valor monetário da transação | Valores atípicos (altos/baixos) podem indicar fraude | Correlacionar com card_info (card1-6) e localização (addr1, addr2)"
    """
    
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # segundos
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "qwen/qwen-2.5-coder-32b-instruct:free", 
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1 
                },
                timeout=30
            )
            response.raise_for_status()
            description = response.json()["choices"][0]["message"]["content"].strip()
            description = description.replace('\\n', ' ').replace('\\r', '').strip()
            return format_description(description)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"Erro 429 (Too Many Requests) na coluna {col_name}. Tentativa {attempt + 1}/{MAX_RETRIES}. Aguardando {RETRY_DELAY * (attempt + 1)}s...")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))  # Backoff exponencial
                    continue
                else:
                    print(f"Máximo de retentativas atingido para a coluna {col_name}.")
                    return format_description("Limite de requisições excedido") # Mensagem específica para erro 429
            print(f"Erro HTTP na coluna {col_name}: {str(e)}")
            return format_description(None) # Retorna '""' em caso de outros erros HTTP
        except Exception as e:
            print(f"Erro inesperado na coluna {col_name}: {str(e)}")
            return format_description(None) # Retorna '""' em caso de outros erros

def update_data_dictionary():
    # Carrega os dados
    if not os.path.exists(DATA_PATH):
        print(f"Erro: Arquivo de dados não encontrado em {DATA_PATH}")
        return
    df = pd.read_parquet(DATA_PATH)
    
    # Gera estatísticas básicas
    stats = pd.DataFrame({
        'coluna': df.columns,
        'tipo': df.dtypes.astype(str), 
        'valores_unicos': [df[col].nunique() for col in df.columns],
        'valores_nulos': df.isna().sum().values,
        'estatistica': [
            df[col].mean() if pd.api.types.is_numeric_dtype(df[col]) 
            else df[col].mode()[0] if not df[col].mode().empty else None 
            for col in df.columns
        ]
    })
    
    # Adiciona descrições
    tqdm.pandas(desc="Gerando descrições")
    stats['descricao'] = stats.progress_apply(
        lambda x: generate_column_description(
            x['coluna'], x['tipo'], x['valores_unicos'], x['valores_nulos'], x['estatistica']
        ), axis=1
    )
    
    # Converte a coluna 'estatistica' para string para evitar problemas no Parquet
    # Isso é feito aqui para garantir que os tipos numéricos sejam usados no prompt, mas strings no Parquet
    stats['estatistica'] = stats['estatistica'].astype(str)

    # Salva em Parquet
    parquet_saved_successfully = False
    try:
        # Remove as aspas literais da descrição antes de salvar em Parquet
        stats_parquet = stats.copy()
        stats_parquet['descricao'] = stats_parquet['descricao'].apply(lambda x: x.strip('"') if isinstance(x, str) and x.startswith('"') and x.endswith('"') else x)
        stats_parquet.to_parquet(PARQUET_PATH, index=False)
        parquet_saved_successfully = True
    except Exception as e:
        print(f"Erro ao salvar Parquet: {str(e)}. O arquivo Parquet não será gerado ou pode estar incompleto.")

    # Salva em CSV
    try:
        stats.to_csv(CSV_PATH, index=False, encoding='utf-8-sig', quoting=1) 
        print(f"\\nCSV salvo em: {CSV_PATH}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {str(e)}")

    if parquet_saved_successfully:
        print(f"Parquet salvo em: {PARQUET_PATH}")
    else:
        print("Arquivo Parquet não foi salvo devido a erro anterior.")


if __name__ == "__main__":
    if not OPENROUTER_API_KEY:
        print("Erro: A variável de ambiente OPENROUTER_API_KEY não está definida.")
    else:
        update_data_dictionary()