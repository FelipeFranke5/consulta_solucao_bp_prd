import json
import time

from selenium.common.exceptions import NoSuchElementException

from automador import AutomacaoBraspag
from listagem import obter_listagem_ecs


class Automacao:
    def __init__(self):
        self.resposta: dict[str, str] = {}

    def salvar_arquivo_com_resposta(self):
        json_resposta = json.dumps(self.resposta, indent=4)

        try:
            with open('retorno.json', 'w', encoding='utf-8') as arquivo:
                arquivo.write(json_resposta)
            mensagem = 'Arquivo disponibilizado.'
            return mensagem
        except OSError:
            mensagem = 'Erro no momento de salvar o arquivo.'
            return mensagem

    def obter_mensagem_resposta(
        self,
        ec: str,
        tentativa: int = 0,
        finalizado: bool = False,
    ):
        while tentativa < 5 and not finalizado:
            try:
                automacao_atual = AutomacaoBraspag(ec)
                automacao_atual.autenticar()
                automacao_atual.consultar_cadastro_api()
                automacao_atual.consultar_cadastro_checkout()
                solucao = automacao_atual.obter_solucao()
            except NoSuchElementException:
                time.sleep(10)
                tentativa += 1
            else:
                finalizado = True
                return solucao

        if not finalizado:
            mensagem = 'Erro na consulta.'
            return mensagem
        return ''


    def rodar_automacoes(self):
        print('-------------------- INICIALIZANDO A AUTOMAÇÃO! --------------------')
        print('\n------------ obtendo a listagem de ecs ------------')
        ecs = obter_listagem_ecs()
        print('\n------------ listagem ok ------------')
        print('\n------------ iniciando o loop de automações ------------')

        for ec in ecs:
            resposta = self.obter_mensagem_resposta(ec)
            self.resposta[ec] = resposta

        print('\n------------ finalizando o loop de automações ------------')
        print('\n------------ salvando o retorno no arquivo json ------------')
        resposta_salvar = self.salvar_arquivo_com_resposta()

        match resposta_salvar:
            case 'Arquivo disponibilizado.':
                print('\n------------ salvo com sucesso! ------------')
            case 'Erro no momento de salvar o arquivo.':
                print('\n------------ não deu para salvar! ------------')
        print('\n-------------------- FINALIZANDO A AUTOMAÇÃO! --------------------')


if __name__ == '__main__':
    principal = Automacao()
    principal.rodar_automacoes()
