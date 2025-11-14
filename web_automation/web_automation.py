import os
import re
import time
import shutil
import logging

import pandas as pd
from pathlib import Path
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.common.by import By


class WebAutomation:
    """ Classe reponsável pela automação do teste """


    def __init__(self) -> None:

        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO,format="[%(asctime)s] [%(levelname)s]: %(message)s")

        self._config_parser = self._parser_setup()
        self._url = self._config_parser["DEFAULT"]["siteDesafio"]
        self._download_path = Path(self._config_parser["DEFAULT"]["downloadFolder"]).absolute()
        self._download_file_name = self._config_parser["DEFAULT"]["downloadFileName"]

        self._driver = self._driver_setup()

    def _parser_setup(self) -> ConfigParser:
        """ Configura o parser de configuração """

        # self._logger.info("Lendo arquivo de configuração")

        config_parser = ConfigParser()
        config_parser.read("config.ini")

        return config_parser

    def _driver_setup(self) -> webdriver.Chrome:
        """ Configura o driver do selenium """

        # self._logger.info("Configurando o driver do selenium")

        opts = webdriver.ChromeOptions()
        opts.add_experimental_option("prefs", {
            "download.default_directory": str(self._download_path),
            "safebrowsing.enabled": True,
            })
        
        return webdriver.Chrome(options=opts)

    def _download_file(self) -> None:
        """ Procura o botão de download e baixa o arquivo"""

        # self._logger.info("Baixando o arquivo")

        os.makedirs(self._download_path, exist_ok=True)
        download_bttn = self._driver.find_element(By.CSS_SELECTOR, f"a[href$='{self._download_file_name}']")
        download_bttn.click()

    def _download_wait(self, directory: str, timeout: int, nfiles: int) -> int:
        """ Verifica se o arquivo foi baixado """

        seconds = 0
        dl_wait = True

        while dl_wait and seconds < timeout:

            time.sleep(1)
            dl_wait = False
            files = os.listdir(directory)

            if nfiles and len(files) != nfiles:
                dl_wait = True

            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True

            seconds += 1

        return seconds

    def _read_file(self) -> pd.DataFrame:
        """ Lê o arquivo baixado """

        # self._logger.info("Criando DataFrame")
        file_path = self._download_path / self._download_file_name
        df = pd.read_excel(str(file_path))

        # self._logger.info(f"Colunas do DataFrame {df.columns.tolist()}")
        # self._logger.info("Ajustando nomes das colunas")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        return df

    def _start_challange(self) -> None:
        """ Inicia o desafio """

        # self._logger.info("Iniciando o desafio")
        start_bttn = self._driver.find_element(By.XPATH, "//button[text()='Start']")
        start_bttn.click()
    
    def _fill_form(self, df: pd.DataFrame) -> None:
        """ Preenche e envia o formulário com os dados do arquivo """

        # self._logger.info("Preenchendo o formulário")

        for index, row in df.iterrows():

            # self._logger.info(f"Preenchendo formulário nª: {index + 1} {row['first_name']}")

            name = self._driver.find_element(By.XPATH, "//input[@ng-reflect-name='labelFirstName']")
            last_name = self._driver.find_element(By.XPATH, "//input[@ng-reflect-name='labelLastName']")
            address = self._driver.find_element(By.XPATH, "//input[@ng-reflect-name='labelAddress']")
            email = self._driver.find_element(By.XPATH, "//input[@ng-reflect-name='labelEmail']")
            company = self._driver.find_element(By.XPATH, "//input[@ng-reflect-name='labelCompanyName']")
            phone = self._driver.find_element(By.XPATH, "//input[@ng-reflect-name='labelPhone']")
            role = self._driver.find_element(By.XPATH, "//input[@ng-reflect-name='labelRole']")

            name.send_keys(row['first_name'])
            last_name.send_keys(row['last_name'])
            address.send_keys(row['address'])
            email.send_keys(row['email'])
            company.send_keys(row['company_name'])
            phone.send_keys(str(row['phone_number']))
            role.send_keys(row['role_in_company'])

            # self._logger.info("Enviando formulário")
            submit_bttn = self._driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_bttn.click()

    def _get_time(self) -> str:
        """ Retorna o tempo de submissão """

        time_message = self._driver.find_element(By.CLASS_NAME, "message2")
        time_text = time_message.text
        submission_time = re.search(r"in\s+(\d{4})", time_text).group(1)

        return submission_time


    def execute(self) -> None:
        """ Método executor da classe """

        try:
            os.makedirs(self._download_path, exist_ok=True)
            self._driver.get(self._url)
            self._download_file()
            download_time = self._download_wait(str(self._download_path), 1, 4)
            # self._logger.info(f"Arquivo baixado em {download_time} segundos")
            df = self._read_file()
            self._start_challange()
            self._fill_form(df)
            submission_time = self._get_time()
            self._logger.info(submission_time)

        except Exception as e:
            self._logger.error(f"Erro ao executar automação: {e}")

        finally:
            self._driver.quit()

            try:
                self._logger.info("removendo a pasta tmp")
                shutil.rmtree(str(self._download_path.parent))

            except Exception as e:
                self._logger.error(f"Erro ao remover arquivo baixado: {e}")
