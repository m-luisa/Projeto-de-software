from modelos.registro_transportes import RegistroTransportes
import requests
import logging 
logging.basicConfig(level = logging.WARNING, format="[AVISO]%(message)s")
from servicos.aviationstack_usuario import AviationStack
from servicos.gtfs_usuario import GtfsUsuario
from servicos.metro_scraper import MetroSPScraper
from api_oculta import AviationStackService, GtfsService, MetroSPService, DadosIncompletosError
from servicos.montador import montar_voo_dominio, montar_onibus_dominio, montar_trem_dominio
from modelos.historico_retratos import HistoricoRetratos
from modelos.viagem import Viagem
from modelos.registro_transportes import RegistroTransportes #rf9
from modelos.canal_notificacao import CanalEmail, CanalPush  # rf10
from modelos.usuario import UsuarioInscrito
from servicos.notificador import Notificador

"""
main.py vai integrar os requisitos funcionais 
    rf5 - buscar_voo, buscar_onibus sochamamos clientes das apis
    rf7 - dadosincompletoserror é capturado e gera um aviso em log
    rf9 - cada transporte obtido é registrado no painel
    rf10 - notificador envia avisos de atrasopelos canais escolhidos pelo usuario
    rf6 - a opção 4 do menu monta a viagem com trechos de modais diferentes
    rf4 - opcao 3 exibe voo, onibus e trens em um unico laço, chamando exibir_status
    rf2 - a opcao 5 busca novamente e usa historicoretratos para comparar o retrato mais recente 
"""

historico = HistoricoRetratos()
painel = RegistroTransportes() #rf9 - reconhecer transportes repetidos
notificador = Notificador() #rf10 - usuario se inscrever




def buscar_voo(dep_iata: str = None, quantidade: int = 10):
    #rf5 - passa por aviationstack + viationstackservice + montar_voo_dominio 
    voos_dominio = []

    #rf8 disponibilidade parcial, se a propria api falhar retorna lista vazia
    try:
        cliente_voo = AviationStack()
        lista_json = cliente_voo.buscar_voos(dep_iata=dep_iata, quantidade=quantidade)

    except (requests.RequestException, KeyError) as erro:
        print(f"Não foi possível buscar voos: {erro}")
        return voos_dominio
    for json_voo  in lista_json:
        try:
            voo_api = AviationStackService.criar_voo_json(json_voo)
            voo_dominio = montar_voo_dominio(voo_api)

            voo_dominio.id_transporte = voo_api.codigo
            historico.registrar(voo_dominio.id_transporte, voo_dominio.retrato_horario)

            voos_dominio.append(voo_dominio)
        except DadosIncompletosError as erro:
            #rf7 - voo com dados incompletos nao entram na lista
            logging.warning(str(erro))
            continue
        except (ValueError, KeyError) as erro:
            logging.warning(f"Erro de formato: {erro}")
            continue
    return voos_dominio
    

def buscar_onibus():
    onibus_dominio_lista = []

    #rf8 - falha ao buscar o feed gtfs nao impede o painel de funcionar
    try:
        cliente_onibus = GtfsUsuario(
            "http://realtime4.mobilibus.com/web/4ch6j/trip-updates?accesskey=982a57efd77a9462bf1665696fb25984"
        )
        atualizacoes = cliente_onibus.buscar_atualizacoes()
    except (requests.RequestException, KeyError) as erro:
        print("Não foi possível buscar onibus: {erro}")
        return onibus_dominio_lista

    #rf5 - cada atualização crua do gtfs passa por gtfsservice
    for a in atualizacoes:
        try:
            onibus_api = GtfsService.criar_onibus_gtfs(a)
            onibus_dominio = montar_onibus_dominio(onibus_api)

            onibus_dominio.id_transporte = onibus_api.identificador
            historico.registrar(onibus_dominio.id_transporte, onibus_dominio.retrato_horario)

            onibus_dominio_lista.append(onibus_dominio)
        #rf7 - descarta onibus com dados incompletos
        except DadosIncompletosError as erro:
            logging.warning(str(erro))
            continue
        except (ValueError, KeyError) as erro:
            logging.warning(f"Erro de formato: {erro}")
            continue
    if not onibus_dominio_lista:
        print("Nenhuma atualização de ônibus encontrada")
    
    return onibus_dominio_lista


def buscar_trens():
    trens_dominio_lista = []
 
    try:
        scraper = MetroSPScraper()
        linhas_raspadas = scraper.buscar_status()
    except requests.RequestException as erro:
        print(f"Não foi possível buscar trens: {erro}")
        return trens_dominio_lista
 
    #rf5 e rf7 - o HTML bruto já chega tratado/filtrado pelo MetroSPService
    for trem_api in MetroSPService.criar_trens_json(linhas_raspadas):
        try:
            trem_dominio = montar_trem_dominio(trem_api)
 
            trem_dominio.id_transporte = trem_api.identificador
            historico.registrar(trem_dominio.id_transporte, trem_dominio.retrato_horario)
 
            trens_dominio_lista.append(trem_dominio)
        except (ValueError, KeyError) as erro:
            logging.warning(f"Erro de formato: {erro}")
            continue
 
    if not trens_dominio_lista:
        print("Nenhum status de trem encontrado")
 
    return trens_dominio_lista


def cadastrar_usuario() -> UsuarioInscrito:
#rf10 - coleta os dados dos canais escolhidos pelo usuario e monta um usuarioinscrito, cada canal vira uma instancia distinta de canalnotificacao 
    print("\n---Cadastro para notificar atrasos ---\n")

    nome = input("Digite seu nome: ").strip()
    while not nome:
        nome = input("O nome não pode ficar vazio. Digite seu nome:").strip()

    inscricoes = []

    print("Canais disponíveis:")
    print("  1 - E-mail")
    print("  2 - Push")
    print("  3 - E-mail e Push")
    escolha = input("Escolha o(s) canal(is) [1/2/3]: ").strip()
    while escolha not in ("1", "2", "3"):
        escolha = input("Opção inválida. Digite 1, 2 ou 3: ").strip()

    if escolha in ("1", "3"):
        email = input("Digite seu e-mail: ").strip()
        while not email or "@" not in email:
            email = input("E-mail inválido, precisa ter '@'. Digite de novo: ").strip()

        inscricoes.append((CanalEmail(), email))

    if escolha in ("2", "3"):
        telefone = input("Seu telefone: ").strip()
        while not telefone:
            telefone = input("Telefone não pode ficar vazio: ").strip()

        inscricoes.append((CanalPush(), telefone))

    return UsuarioInscrito(nome, inscricoes)

def registrar_no_painel(transporte, nome: str):
    #rf9 - registra o transporte no painel e avisar se for uma busca duplicada
    if transporte is None:
        return
    #observação - aqui poderia ter um if para identificar que vai ser um adicionado um novo onibus no painel, mas o terminal ficaria muito poluido com esses avisos repetitivos de adição
    painel.registrar(transporte)
    notificador.notificar_atraso(transporte)  #rf10 avisa se tiver atraso

def exibir_menu():
    print("\n Painel de status de transportes")
    print("1 - Ver status de todos os voos;")
    print("2 - Ver status de todos os ônibus;")
    print("3 - Ver status de todos os trem;")
    print("4 - Ver painel completo (voos + ônibus + trens);")
    print("5 - Ver viagem com múltiplos trechos (voo + ônibus + trem);")
    print("6 - Buscar de novo e comparar;")
    print("7 - Sair")


def main():
    usuario = cadastrar_usuario()
    notificador.inscrever(usuario)
    canais_nomes = ", ".join(type(c).__name__.replace("Canal", "") for c, _ in usuario.inscricoes)
    print(f"\n{usuario.nome} inscrito para receber notificações por: {canais_nomes}\n")

    voos = buscar_voo()
    for v in voos:
        registrar_no_painel(v, "Voo")
    onibus_lista = buscar_onibus()
    for o in onibus_lista:
        registrar_no_painel(o, "Ônibus")
    trens_lista = buscar_trens()
    for t in trens_lista:
        registrar_no_painel(t, "Trem")

    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            if voos:
                for v in voos:
                    print(v.exibir_status())
            else:
                print("Sem dados de voo disponível.")

        elif escolha == "2":
            if onibus_lista:
                for o in onibus_lista:
                    print(o.exibir_status())
            else:
                print("Sem dado de ônibus disponível.")

        elif escolha == "3":
        #rf4 - painel unificado
            if trens_lista:
                for t in trens_lista:
                    print(t.exibir_status())
            else:
                print("Sem dado de trem disponível.")

        elif escolha == "4":
        #rf2 - busca novos retratos de horario e usa historico de retratos para comparar com o anterior
            transportes = painel.listar()  #rf9: painel já deduplicado
            if not transportes:
                print("Nenhum transporte disponível.")
            else:
                print(f"({painel.quantidade()} transporte(s) único(s) no painel)")
                for t in transportes:
                    print(t.exibir_status())

        elif escolha == "5":
            if voos and onibus_lista and trens_lista:
                viagem = Viagem([voos[0], onibus_lista[0], trens_lista[0]])
                print(viagem.exibir_status())
            else:
                print("Preciso de ao menos um voo, um ônibus E um trem disponíveis para montar a viagem.")

        elif escolha == "6":
            #rf2 - busca novos retratos de horario e usa o historico para comparar com o retrato anterior
            print("Buscando dados novos...")
            voos = buscar_voo()
            for v in voos:
                registrar_no_painel(v, "Voo")  #rf9: se for o mesmo voo, não duplica
            onibus_lista = buscar_onibus()
            for o in onibus_lista:
                registrar_no_painel(o, "Ônibus")
            trens_lista = buscar_trens()
            for t in trens_lista:
                registrar_no_painel(t, "Trem")

            for v in voos:
                print(f"Voo {v.id_transporte}:", historico.mudou(v.id_transporte))
            for o in onibus_lista:
                print(f"Ônibus {o.id_transporte}:", historico.mudou(o.id_transporte))
            for t in trens_lista:
                print(f"Trem {t.id_transporte}:", historico.mudou(t.id_transporte))

        elif escolha == "7":
            print("Finalizando.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()