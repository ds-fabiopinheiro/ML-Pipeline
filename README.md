# Projeto ML — Classificação com Classes Raras

Olá! Este projeto é um guia prático para lidar com problemas de classificação onde os "targets" positivos são extremamente raros (ex: 0,5% da base). Vamos explorar técnicas modernas para evitar falsos positivos (FP) e falsos negativos (FN), desde ajustes simples até geração de dados sintéticos.

## O Problema

- **Targets raros**: Menos de 1% da base.
- **Falsos Positivos/Negativos**: Modelos tradicionais falham.
- **Oversampling/Undersampling**: Nem sempre resolvem.
- **Dados sintéticos**: Necessidade de balanceamento realista.

## Estratégias

### 1️⃣ Avalie Corretamente
- **Métricas**: Use Precision-Recall AUC e custo esperado, não apenas accuracy/ROC.
- **Calibração**: Ajuste o limiar com Isotonic ou Platt Scaling.

### 2️⃣ Pese o Custo Antes de Balancear
- **Class Weight/Focal Loss**: `scale_pos_weight` no XGBoost ou Focal Loss (γ≈2).
- **Ajuste de Limiar**: Ex: `p >= 0.07` em vez de `0.5`.

### 3️⃣ Gere Dados Sintéticos (Quando Necessário)
- **Ferramentas**:
  - SMOTE, Borderline-SMOTE (imbalanced-learn).
  - CTGAN/TVAE (SDV) para dados tabulares.
  - TabDDPM (diffusion) para multimodalidade.
- **Validação**: TSTR (AUC não pode cair mais que 2pp).

### 4️⃣ Erros Comuns
- Oversample até 50% → Overfitting.
- Vazamento em Cross-Validation.
- Ignorar custo real dos erros (FN >> FP).

## Ferramentas Recomendadas

| Ferramenta | Descrição | Link |
|------------|-----------|------|
| imbalanced-learn | SMOTE, ensembles balanceados | [GitHub](https://github.com/scikit-learn-contrib/imbalanced-learn) |
| SDV/CTGAN | GANs para dados tabulares | [GitHub](https://github.com/sdv-dev/SDV) |
| TabDDPM | Diffusion para tabelas | [GitHub](https://github.com/yandex-research/tab-ddpm) |
| Focal Loss PyTorch | Peso para classes raras | [GitHub](https://github.com/clcarwin/focal_loss_pytorch) |

## Datasets Públicos

| Dataset | Tipo | Tamanho | % Fraude | Link |
|---------|------|---------|----------|------|
| Credit Card Fraud 2013 | Real | 284k | 0,17% | [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) |
| IEEE-CIS Fraud | Real | 1,1M | ~3% | [Kaggle](https://www.kaggle.com/competitions/ieee-fraud-detection) |
| PaySim | Sintético | 6,3M | 0,13% | [Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1) |

## Instalação Rápida

```sh
pip install imbalanced-learn sdv ctgan focal-loss-pytorch
```

## Resumo
1. Ajuste `class_weight` e limiar.
2. Experimente ensembles balanceados.
3. Gere dados sintéticos (CTGAN/TabDDPM).
4. Valide com TSTR e métricas de custo.

---
**Dúvidas?** Consulte os repositórios ou abra uma issue!