# Painel de status de transportes 

> Trabalho prático da disciplina de **Projeto de Software** lecionada pelo professor Baldoíno Fonseca
> 
> Instituto de Computação (IC) — Universidade Federal de Alagoas (UFAL)
> 
> Grupo 5: Ana Carolina Cavalcante de Jesus, Julia Cabral Melo e Maria Luísa Silva Nunes de Souza

---

## Menu de navegação do código

**RF5 API oculta**  - Isolamento e tratamento da API externa, [`api-oculta.py`](./api-oculta.py) 


**Sistema completo** Integração do painel, [`main.py`](./main.py) 

---

## Descrição do projeto
O projeto implementa um **sistema de monitoramento de meio de transportes** em Python, baseado nos princípios estudados na disciplina de **Projeto de Software**:

- **Abstração e herança** : atribuímos a classe base abstrata para padronização dos modais;
- **Polimorfismo**: tratamento, de modo igual, os diferentes transportes analisados (voos, ônibus e trens);
- **Encapsulamento e exceções**: validação restritiva das coordenadas geográficas, por meio da latitude e longitude, e, com isso, a proteção contra dados inválidos, uma vez que há a identificação de erro mediante aos dados incoerentes.

O objetivo do nosso projeto é montar um sistema seguro de gerência de veículos, independente de seu modal, e a verificação de possíveis atrasos em tempo real.

---

## Diagrama de classes (UML)

<img width="8192" height="2404" alt="Modal Transporte Status Flow-2026-08-18-190556" src="https://github.com/user-attachments/assets/54c08a09-3d70-4018-a816-6342c0036ff4" />


## Para compilar e executar o código
Para rodar o sistema completo:
```bash
python3 main.py


