# Otimização e Modularização do HufflePlots - 16/10/2025

As atualizações de processamento de arquivos `.xvg` do GROMACS e compilação de arquivos de interesse em `.csv` me fez refletir sobre como melhorar o entendimento do script como um todo para um usuário que queira entende-lo. **Modularização**
separa as etapas principais dos processos da ferramenta em diferentes arquivos `.py` armazenados no repositório, e acredito que vai ser útil para quando os outros alunos do laboratório precisarem fazer alterações na ferramenta, ou
puxar uma função específica para outra análise de dados. 

Para ter uma ideia de como modularizar, pedi ao Gemini para inicialmente fazer a Modularização do `ProtPlots.py`, para depois eu incorporar aos poucos as outras etapas de análise e processamento. 

## Modularização de CSV_COMPILEEEE 

1. **Estrutura de arquivos da Modularização de csv_compile.py**
```python
your_project_folder/
├── csv_main.py #constrói o ambiente principal e upload
├── csv_process.py #processamento dos dados
└── csv_ui.py #Interface
```

Intenção de Concatenar com Repositório `Module-XVG_process` e `Module-Plots` para versão final e modularizada de `HufflePlots` com **3 abas de Processamento separadas**. 