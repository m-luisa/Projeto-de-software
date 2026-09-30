# Painel de Status de Transportes

> Sistema em Python que monitora voos, ônibus e trens em tempo real, calcula atrasos e notifica usuários inscritos.

> Instituto de Computação (IC) — Universidade Federal de Alagoas (UFAL)

> Trabalho prático da disciplina de **Projeto de Software**, lecionada pelo professor **Baldoíno Fonseca**

## Sumário

- [Visão geral](#visão-geral)
- [Conceitos de POO aplicados](#conceitos-de-poo-aplicados)
- [Diagrama de classes (UML)](#diagrama-de-classes-uml)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Requisitos funcionais implementados](#requisitos-funcionais-implementados)
- [Tratamento de erros](#tratamento-de-erros)
- [Autoras](#autoras)

## Visão geral

O projeto implementa um **sistema de monitoramento de meios de transporte** (voos, ônibus e trens) em Python, consumindo fontes externas em tempo real (AviationStack, GTFS Realtime e a página "Direto do Metrô" do Metrô-SP) e convertendo esses dados brutos em objetos de domínio que sabem calcular seu próprio atraso.

**O que o sistema faz:**

- Busca dados reais de voos (AviationStack), ônibus (feed GTFS Realtime) e trens (página do Metrô-SP);
- Calcula o atraso de cada transporte comparando horário programado × horário real;
- Mantém um **painel deduplicado**, reconhecendo quando a mesma busca retorna o mesmo transporte;
- Guarda um **histórico de retratos** de horário, permitindo comparar "antes x agora";
- Agrupa múltiplos trechos (voo + ônibus + trem) em uma **viagem única**;
- **Notifica** usuários inscritos (e-mail/push) quando um transporte está atrasado.

## Conceitos de POO aplicados

<table>
<tr><td width="200"><b>Abstração / Herança</b></td><td>

`Transporte` é a classe-base abstrata que padroniza `Voo`, `Onibus` e `Trem` — cada um implementa sua própria regra de atraso.

</td></tr>
<tr><td><b>Polimorfismo</b></td><td>

`main.py` e `Viagem` chamam `exibir_status()` / `calcular_atraso()` igualmente para qualquer modal, sem saber qual subclasse é.

</td></tr>
<tr><td><b>Encapsulamento</b></td><td>

`Localizacao` protege latitude/longitude com atributos privados e valida os limites geográficos na criação do objeto.

</td></tr>
<tr><td><b>Tratamento de exceções</b></td><td>

Praticamente todo acesso a API externa, parsing de JSON/GTFS e conversão de horário é protegido com `try/except` específico, evitando que dado inconsistente derrube o programa.

</td></tr>
</table>

## Diagrama de classes (UML)

<details open>
<summary><b>Ver diagrama de classes interativo</b></summary>

```mermaid
classDiagram
    %% ===== DOMÍNIO: transportes =====
    class Transporte {
        <<abstract>>
        +origem
        +destino
        +retrato_horario
        +id_transporte
        +calcular_diferenca()
        +calcular_atraso()*
        +exibir_status()*
        +identificador_unico()*
        +chave_identificacao()
    }
    class Voo {
        +numero_voo
        +calcular_atraso()
        +exibir_status()
        +identificador_unico()
    }
    class Onibus {
        +linha_onibus
        +identificador
        +calcular_atraso()
        +exibir_status()
        +identificador_unico()
    }
    class Trem {
        +linha_trem
        +status_operadora
        +operacao_normal
        +identificador
        +calcular_atraso()
        +exibir_status()
        +identificador_unico()
    }
    Transporte <|-- Voo
    Transporte <|-- Onibus
    Transporte <|-- Trem
    note for Transporte "id_transporte é atribuído pelo main.py depois da criação"

    %% ===== DOMÍNIO: objetos protegidos =====
    class Retrato_horario {
        -horario_programado
        -horario_real
        +horario_programado()
        +horario_real()
        +calcular_diferenca()
    }
    Transporte o-- "1" Retrato_horario

    class Localizacao {
        -latitude
        -longitude
        +latitude()
        +longitude()
    }

    %% ===== DOMÍNIO: coleções e viagem =====
    class RegistroTransportes {
        -_registros
        +registrar(transporte) bool
        +listar()
        +quantidade()
    }
    RegistroTransportes o-- "*" Transporte

    class HistoricoRetratos {
        -_retratos
        +registrar(id_transporte, retrato)
        +ultimo(id_transporte)
        +penultimo(id_transporte)
        +mudou(id_transporte)
    }
    HistoricoRetratos o-- "*" Retrato_horario

    class Viagem {
        +trechos
        +atraso_total()
        +exibir_status()
    }
    Viagem o-- "*" Transporte

    %% ===== NOTIFICAÇÕES (RF10) =====
    class CanalNotificacao {
        <<abstract>>
        +enviar(destinatario, mensagem)*
    }
    class CanalEmail {
        -servidor_smtp
        -porta
        -remetente
        -senha_app
        +enviar(destinatario, mensagem)
    }
    class CanalPush {
        -servidor
        +enviar(destinatario, mensagem)
    }
    CanalNotificacao <|-- CanalEmail
    CanalNotificacao <|-- CanalPush

    class UsuarioInscrito {
        +nome
        +inscricoes
    }
    UsuarioInscrito o-- "*" CanalNotificacao

    class Notificador {
        -_inscritos
        -_avisos_enviados
        -_pendentes
        +inscrever(usuario)
        +notificar_atraso(transporte)
        +enviar_pendentes()
    }
    Notificador o-- "*" UsuarioInscrito
    Notificador ..> Transporte : consulta atraso
    Notificador ..> CanalNotificacao : chama enviar

    %% ===== API OCULTA (RF5 e RF7) =====
    class ValueError {
        <<built-in>>
    }
    class DadosIncompletosError {
        <<exception>>
    }
    ValueError <|-- DadosIncompletosError

    class VooApi["Voo (api_oculta.py)"] {
        +codigo
        +origem
        +destino
        +horario_programado
        +horario_estimado
    }
    class OnibusApi["Onibus (api_oculta.py)"] {
        +identificador
        +linha
        +origem
        +destino
        +horario_programado
        +horario_partida
        +horario_chegada
    }
    class TremApi["Trem (api_oculta.py)"] {
        +identificador
        +linha
        +empresa
        +origem
        +destino
        +status_operadora
        +operacao_normal
        +atualizado_em
    }

    class AviationStackService {
        +criar_voo_json(json)$
    }
    class GtfsService {
        +criar_onibus_gtfs(json)$
    }
    class MetroSPService {
        +criar_trens_json(linhas)$
        -_montar_trem(linha)$
    }
    AviationStackService ..> VooApi : cria
    GtfsService ..> OnibusApi : cria
    MetroSPService ..> TremApi : cria
    AviationStackService ..> DadosIncompletosError : lança
    GtfsService ..> DadosIncompletosError : lança
    MetroSPService ..> DadosIncompletosError : lança

    %% ===== CLIENTES DAS APIs (servicos/) =====
    class AviationStack {
        -__api_key
        +URL
        +buscar_voo(iata_code)
        +buscar_voos(dep_iata, quantidade)
    }
    class GtfsUsuario {
        +feed_url
        -_buscar_feed()
        +buscar_atualizacoes()
        +buscar_posicoes()
    }
    class MetroSPScraper {
        +URL
        +buscar_status()
    }
    GtfsUsuario ..> Localizacao : cria

    %% ===== MONTADOR: objeto da API vira objeto de domínio =====
    class montador {
        <<module>>
        +montar_voo_dominio(voo_api)
        +montar_onibus_dominio(onibus_api)
        +montar_trem_dominio(trem_api)
    }
    montador ..> VooApi : lê
    montador ..> OnibusApi : lê
    montador ..> TremApi : lê
    montador ..> Retrato_horario : cria
    montador ..> Voo : monta
    montador ..> Onibus : monta
    montador ..> Trem : monta

    %% ===== MAIN: orquestra o fluxo =====
    class main {
        <<module>>
        +buscar_voo()
        +buscar_onibus()
        +buscar_trens()
        +cadastrar_usuario()
        +registrar_no_painel(transporte, nome)
        +exibir_menu()
        +main()
    }
    main ..> AviationStack : busca JSON bruto
    main ..> GtfsUsuario : busca feed
    main ..> MetroSPScraper : busca HTML
    main ..> AviationStackService : traduz
    main ..> GtfsService : traduz
    main ..> MetroSPService : traduz
    main ..> montador : converte
    main ..> HistoricoRetratos : registra retratos
    main ..> RegistroTransportes : painel deduplicado
    main ..> Notificador : notifica atrasos
    main ..> UsuarioInscrito : cadastra
    main ..> CanalEmail : instancia
    main ..> CanalPush : instancia
    main ..> Viagem : monta viagem
```

</details>

## Estrutura do repositório

```text
Projeto-de-software/
├── main.py                      # Ponto de entrada — orquestra tudo (menu, cadastro, painel)
├── api_oculta.py                # RF5 — isola e traduz o JSON/HTML "cru" das fontes em objetos
├── requeriments.txt             # Dependências do projeto
├── .env.exemplo                 # Modelo do arquivo de variáveis de ambiente
├── .gitignore
│
├── modelos/                     # Regras de negócio / domínio (não sabem de API)
│   ├── transporte.py            # Transporte (base) + Voo, Onibus, Trem
│   ├── retrato_horario.py       # Retrato_horario — programado x real
│   ├── localizacao.py           # Localizacao — encapsula lat/long
│   ├── historico_retratos.py    # Histórico de retratos por transporte
│   ├── registro_transportes.py  # RF9 — painel deduplicado
│   ├── canal_notificacao.py     # RF10 — CanalNotificacao, CanalEmail, CanalPush
│   ├── usuario.py               # UsuarioInscrito
│   └── viagem.py                # Viagem — agrupa múltiplos trechos
│
└── servicos/                    # Integração com o mundo externo
    ├── aviationstack_usuario.py # Cliente HTTP da API AviationStack (voos)
    ├── gtfs_usuario.py          # Cliente do feed GTFS Realtime (ônibus)
    ├── metro_scraper.py         # Lê a página "Direto do Metrô" (trens)
    ├── montador.py              # Converte objetos "API" em objetos "domínio"
    └── notificador.py           # RF10 — dispara notificações de atraso
```

## Requisitos funcionais implementados

| RF | Descrição | Onde está |
|---|---|---|
| **RF5** | Isolamento e tratamento da API externa ("API oculta") | [`api_oculta.py`](api_oculta.py) |
| **RF9** | Reconhecimento de buscas duplicadas / painel deduplicado | [`modelos/registro_transportes.py`](modelos/registro_transportes.py) |
| **RF10** | Inscrição de usuário e notificação de atraso por canal (e-mail/push) | [`modelos/canal_notificacao.py`](modelos/canal_notificacao.py), [`modelos/usuario.py`](modelos/usuario.py), [`servicos/notificador.py`](servicos/notificador.py) |
| — | Validação de coordenadas geográficas (encapsulamento) | [`modelos/localizacao.py`](modelos/localizacao.py) |
| — | Histórico de horários e comparação de atraso ao longo do tempo | [`modelos/historico_retratos.py`](modelos/historico_retratos.py) |
| — | Viagem com múltiplos trechos (voo + ônibus) | [`modelos/viagem.py`](modelos/viagem.py) |

## Tratamento de erros

O sistema foi construído para nunca quebrar por causa de um dado externo inconsistente:

- **Falha de rede / API fora do ar** → `requests.RequestException` capturada em `main.py`, sistema segue sem aquele transporte;
- **JSON ou GTFS em formato inesperado** → `KeyError`/`ValueError`/`IndexError` convertidos em mensagens claras (`api_oculta.py`, `servicos/gtfs_usuario.py`);
- **Horário ausente ou mal formatado** → validado em `Retrato_horario` e no `montador.py`;
- **Coordenadas inválidas** → `Localizacao` recusa a criação do objeto;
- **Chave de API ausente** → `AviationStack` levanta erro amigável pedindo para configurar o `.env`.

## Autoras

**Grupo 5 — Projeto de Software (UFAL)**

- Ana Carolina Cavalcante de Jesus
- Julia Cabral Melo
- Maria Luísa Silva Nunes de Souza