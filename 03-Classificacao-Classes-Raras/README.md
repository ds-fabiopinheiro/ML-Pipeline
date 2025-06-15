# Classificação com Classes Raras

Este projeto explora técnicas avançadas para lidar com problemas de classificação onde os "targets" positivos são extremamente raros (ex: 0,5% da base).

## Plano de Estudos

### Semana 1: Avaliação e Custo
1. **Métricas Adequadas**
   - Precision-Recall AUC.
   - Expected Cost (Custo Esperado).
2. **Ajuste de Limiar**
   - Isotonic/Platt Scaling.
   - Threshold Moving (ex: `p >= 0.07`).

### Semana 2: Peso para Classes
1. **Class Weight**
   - `scale_pos_weight` no XGBoost/LightGBM.
2. **Focal Loss**
   - Implementação em PyTorch.

### Semana 3: Geração de Dados Sintéticos
1. **Ferramentas**
   - SMOTE-NC, Borderline-SMOTE.
   - CTGAN/TVAE (SDV).
   - TabDDPM (Diffusion).
2. **Validação**
   - TSTR (Train-on-Synthetic-Test-on-Real).
   - Distâncias Marginais (KS/JS).

## Recursos
- [SDV/CTGAN](https://github.com/sdv-dev/SDV)
- [TabDDPM](https://github.com/yandex-research/tab-ddpm)

## Próximos Passos
- Utilize os scripts em `scripts/` para gerar dados sintéticos.
- Valide com datasets reais (ex: Credit Card Fraud).

---
**Dúvidas?** Consulte a documentação ou abra uma issue!
