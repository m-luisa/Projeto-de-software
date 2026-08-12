# Painel de status de transportes 

> Trabalho prático da disciplina de **Projeto de Software** lecionada pelo professor Baldoíno Fonseca
> 
> Instituto de Computação (IC) — Universidade Federal de Alagoas (UFAL)
> 
> Grupo 5: Ana Carolina Cavalcante de Jesus, Julia Cabral Melo e Maria Luísa Silva Nunes de Souza

---

## Menu de navegação do código

| **RF5 - API Oculta** | Isolamento e tratamento da API externa (AviationStack) | [`rf5_api_oculta.py`](./rf5_api_oculta.py) |
| **Sistema Completo** | Execução unificada e integração do painel | [`main.py`](./main.py) |

---

## Descrição do projeto
O projeto implementa um **sistema de monitoramento de meio de transportes** em Python, baseado nos princípios estudados na disciplina de **Projeto de Software**:

- **Abstração e herança** : atribuímos a classe base abstrata para padronização dos modais;
- **Polimorfismo**: tratamento, de modo igual, os diferentes transportes analisados (voos, ônibus e trens);
- **Encapsulamento e exceções**: validação restritiva das coordenadas geográficas, por meio da latitude e longitude, e, com isso, a proteção contra dados inválidos, uma vez que há a identificação de erro mediante aos dados incoerentes.

O objetivo do nosso projeto é montar um sistema seguro de gerência de veículos, independente de seu modal, e a verificação de possíveis atrasos em tempo real.

---

## Diagrama de classes (UML)

<img width="8192" height="3493" alt="Modal Transporte Status Flow-2026-08-05-151853" src="https://github.com/user-attachments/assets/8cf2a10e-1372-4e96-bac7-3cfe16185dfa" /> 

## Para compilar e executar o código
Para rodar o sistema completo:
```bash
python3 main.py


