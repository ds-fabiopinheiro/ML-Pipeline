# Modelos Preditivos

## Plano de Estudos
1. **Algoritmos Supervisionados**
   - Regressão, árvores de decisão, redes neurais.
2. **Otimização de Hiperparâmetros**
   - GridSearch, RandomSearch, Bayesian Optimization.
3. **Validação de Modelos**
   - Métricas (AUC, RMSE), cross-validation.

## Arquitetura do Fluxo Preditivo
```mermaid
graph LR
    A[Dados] --> B[Pré-processamento]
    B --> C[Treinamento]
    C --> D[Avaliação]
    D --> E[Deploy]
```

## Ferramentas
- Scikit-learn, XGBoost, TensorFlow
- MLflow (versionamento)

## Próximos Passos
- Praticar com datasets como MNIST ou Boston Housing.
- Explorar AutoML (H2O, TPOT).