def obter_listagem_ecs():
    with open('lista_ec.txt', encoding='utf-8') as arquivo:
        lista_ecs = arquivo.read().splitlines()
        return lista_ecs
