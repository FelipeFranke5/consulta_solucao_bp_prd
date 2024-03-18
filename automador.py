import time

from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By


class ErroAmbiente(Exception):
    pass


class AutomacaoBraspag:
    def __init__(self, ec: str):
        self.ec = ec
        self.bp_login = ''
        self.bp_password = ''
        self.bp_url = ''
        self.bp_checkout_url = ''
        self.bp_login_title = ''
        self.cadastro_possui_api = False
        self.cadastro_possui_checkout = False
        self.iniciar_chaves_ambiente()
        self.driver = webdriver.Edge()

    def iniciar_chaves_ambiente(self):
        arq = dotenv_values('.env')
        bp_login = arq.get('BP_LOGIN')
        bp_login_title = arq.get('BP_LOGIN_TITLE')
        bp_home_title = arq.get('BP_HOME_TITLE')
        bp_password = arq.get('BP_PASSWORD')
        bp_url = arq.get('BP_URL')
        bp_checkout_url = arq.get('BP_CHECKOUT_URL')
        lista_chaves_ambiente = [
            bp_login,
            bp_login_title,
            bp_home_title,
            bp_password,
            bp_url,
            bp_checkout_url,
        ]

        for chave in lista_chaves_ambiente:
            if not chave:
                raise ErroAmbiente('Por favor, verifique o arquivo ".env".')

        self.bp_login = bp_login
        self.bp_login_title = bp_login_title
        self.bp_home_title = bp_home_title
        self.bp_password = bp_password
        self.bp_url = bp_url
        self.bp_checkout_url = bp_checkout_url

    def autenticar(self):
        self.driver.get(self.bp_url)
        time.sleep(1)
        assert self.bp_login_title in self.driver.title
        usuario = self.driver.find_element(By.XPATH, '//input[@name="Param1"]')
        senha = self.driver.find_element(By.XPATH, '//input[@name="Param2"]')
        usuario.clear()
        usuario.send_keys(self.bp_login)
        senha.clear()
        senha.send_keys(self.bp_password)
        btn_entrar = self.driver.find_element(By.XPATH, '//button[@id="enter"][@type="submit"]')
        btn_entrar.click()
        time.sleep(1)

    def pesquisar_ec_api(self):
        assert '[PRD] Pesquisar Estabelecimentos | Admin' in self.driver.title
        campo_ec = self.driver.find_element(By.XPATH, '//input[@name="EcNumber"]')
        campo_ec.clear()
        campo_ec.send_keys(self.ec)
        campo_data_inicial = self.driver.find_element(By.XPATH, '//input[@name="StartDate"]')
        campo_data_inicial.clear()
        btn_buscar = self.driver.find_element(
            By.XPATH, '//button[@id="buttonSearch"][@type="submit"]'
        )
        btn_buscar.click()
        time.sleep(3)

    def acessar_botao_api(self):
        assert self.bp_home_title in self.driver.title
        btn_cielo = self.driver.find_element(By.XPATH, '//a[@id="cielo"]')
        btn_cielo.click()
        time.sleep(1)
        btn_pesquisar_ecs = self.driver.find_element(
            By.XPATH, '//a[@id="listEc"][@href="/EcommerceCielo/List"]'
        )
        btn_pesquisar_ecs.click()
        time.sleep(1)

    def consultar_cadastro_api(self):
        self.acessar_botao_api()
        self.pesquisar_ec_api()
        resultado = self.driver.find_element(By.XPATH, '//div[@class="adm-title"]')

        if '0' in resultado.text:
            self.cadastro_possui_api = False
        else:
            self.cadastro_possui_api = True

    def pesquisar_ec_checkout(self):
        assert 'Checkout Cielo' in self.driver.title
        campo_ec = self.driver.find_element(
            By.XPATH, '//input[@name="AffiliationCode"][@id="AffiliationCode"]'
        )
        campo_ec.clear()
        campo_ec.send_keys(self.ec)
        campo_data_inicial = self.driver.find_element(By.XPATH, '//input[@name="StartCreatedDate"]')
        campo_data_inicial.clear()
        btn_buscar = self.driver.find_element(By.XPATH, '//a[@id="buttonSearch"]')
        btn_buscar.click()
        time.sleep(3)

    def consultar_cadastro_checkout(self):
        self.driver.get(self.bp_checkout_url)
        time.sleep(3)
        self.pesquisar_ec_checkout()
        resultado = self.driver.find_element(By.XPATH, '//th[@class="title"][@colspan="8"]')

        if '0' in resultado.text:
            self.cadastro_possui_checkout = False
        else:
            self.cadastro_possui_checkout = True

    def obter_solucao(self):
        if self.cadastro_possui_api and self.cadastro_possui_checkout:
            return 'API 3.0 e Checkout Cielo'
        if self.cadastro_possui_api and not self.cadastro_possui_checkout:
            return 'API 3.0'
        if not self.cadastro_possui_api and self.cadastro_possui_checkout:
            return 'Checkout Cielo'
        return 'NA'
