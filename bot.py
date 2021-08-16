import platform as pt
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from re import match

class CSG(object):
    def __init__(self):
        if pt.system() == 'Linux':
            options = Options()
            self.driver = Firefox(executable_path=GeckoDriverManager().install(), options=options)
        else:
            options = ChromeOptions()
            self.driver = Chrome(executable_path=ChromeDriverManager().install(), options=options)

        self.url = 'https://www.santandernegocios.com.br/portaldenegocios/'
        self.driver.get(self.url)


    def login(self, user, password):
        userXpath = '//*[@id="userLogin__input"]'
        passXpath = '//*[@id="userPassword__input"]'
        buttonXpath = '/html/body/app/ui-view/login/div/div/div/div/div[2]/div[3]/button[2]'

        userInput = self.driver.find_element_by_xpath(userXpath)
        passInput = self.driver.find_element_by_xpath(passXpath)
        button = self.driver.find_element_by_xpath(buttonXpath)

        userInput.send_keys(user)
        passInput.send_keys(password)
        self.forceClick(button)


    def goToCsg(self):
        imgXpath = '//*[@id="convivencia-area"]/div/ui-view/afe-home/div[2]/div[1]/img'
        linkSelector = '#header > div.menu.align-children-right > user-menu > div > nav > div > div:nth-child(3) > ul > li:nth-child(2) > a'

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, imgXpath)))
        
        self.driver.execute_script(f"document.querySelector('{linkSelector}').click()")
        
        sleep(3)
        
        HandleCount = self.driver.window_handles
        self.driver.switch_to_window(HandleCount[1])


    def goToSign(self):

        buttonSelector = 'document.querySelector("#ctl00_ContentPlaceHolder1_j0_j1_DataListMenu_ctl00_LinkButton2")'
        signLinkSelector = '#ctl00_cph_Menu1n5 > td > table > tbody > tr > td > a'

        try: WebDriverWait(self.driver, 7).until(EC.title_is('Menu Sistema Função inf.'))
        except: pass
        else: sleep(1)
        
        self.driver.execute_script(f"{buttonSelector}.click()")
        sleep(3)
        try: WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, signLinkSelector)))
        except: pass
        self.driver.execute_script(f"document.querySelector('{signLinkSelector}').click()")
        sleep(2)


    def addData(self, clientData):
        emprInputXpath = '//*[@id="ctl00_cph_j0_j1_PPCODORG4_CAMPO"]'
        funcTypeXpath = '//*[@id="ctl00_cph_j0_j1_FNTPFUN_CAMPO"]'
        clientTypeXpath = '//*[@id="ctl00_cph_j0_j1_PMTPCC_CAMPO"]'
        venPromXpath = '//*[@id="ctl00_cph_j0_j1_VENDPROM_CAMPO"]'
        # promCodeXpath = '//*[@id="ctl00_cph_j0_j1_PPCODORG3_CAMPO"]'
        codPromXpath = '//*[@id="ctl00_cph_j0_j1_PPCODORG3_CAMPO"]'
        cpfVendXpath = '//*[@id="ctl00_cph_j0_j1_PPCPFPROFI_CAMPO"]'
        regraXpath = '//*[@id="ctl00_cph_j0_j1_PMCODPRDR_CAMPO"]'
        cpfCliXpath = '//*[@id="ctl00_cph_j0_j2_CLCNPJ_CAMPO"]'
        submitSelector = 'document.querySelector("#BBOk_txt")'
        loadingXpath = '//*[@id="ctl00_up"]/div'

        emprInput = self.driver.find_element_by_xpath(emprInputXpath)
        emprInput.send_keys(clientData['cod_empregador'])
        emprInput.send_keys(Keys.ENTER)

        sleep(3)

        try:
            funcType = Select(self.driver.find_element_by_xpath(funcTypeXpath))
            funcValue = 'ES' if match(r'.*?ESTATU.*?', clientData['tipo_func']) else 'CS'
            funcType.select_by_value(funcValue)
        except:
            pass

        clientType = Select(self.driver.find_element_by_xpath(clientTypeXpath))
        clientType.select_by_value('CC')

        venProm = Select(self.driver.find_element_by_xpath(venPromXpath))
        venProm.select_by_value('S')
        sleep(2)

        codProm = self.driver.find_element_by_xpath(codPromXpath)
        codProm.send_keys(clientData['cod_promotor'])
        codProm.send_keys(Keys.ENTER)

        sleep(1)
        # cpfVend = self.driver.find_element_by_xpath(cpfVendXpath)
        self.driver.execute_script(f'document.evaluate(\'{cpfVendXpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = "{clientData["cpf_func"]}";')
        # cpfVend.send_keys(clientData['cpf_func'])
        # cpfVend.send_keys(Keys.ENTER)

        regra = self.driver.find_element_by_xpath(regraXpath)
        regra.send_keys(clientData['regra_corr'])
        
        cpfCli = self.driver.find_element_by_xpath(cpfCliXpath)
        # cpfCli.send_keys(clientData['cpf_cliente'])
        self.driver.execute_script(f'document.evaluate(\'{cpfCliXpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = "{clientData["cpf_cliente"]}";')
        cpfCli.send_keys(Keys.ENTER)

        sleep(2)
        # cpfCli = self.driver.find_element_by_xpath(cpfCliXpath)
        # cpfCli.send_keys(clientData['cpf_cliente'])
        self.driver.execute_script(f'document.evaluate(\'{cpfCliXpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = "{clientData["cpf_cliente"]}";')

        self.driver.execute_script(f'{submitSelector}.click()')

        sleep(3)
        try:
            WebDriverWait(self.driver, 600).until(EC.invisibility_of_element_located((By.XPATH, loadingXpath)))
        except Exception:
            pass

        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            sleep(2)
            regra = self.driver.find_element_by_xpath(regraXpath)
            # regra.clear()
            # regra.send_keys(clientData['regra_nao_corr'])
            self.driver.execute_script(f'document.evaluate(\'{regraXpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = "{clientData["regra_nao_corr"]}";')
            regra.send_keys(Keys.ENTER)
        except TimeoutException: pass

        try:
            self.driver.execute_script(f'{submitSelector}.click()')
        except Exception: pass

        try:
            WebDriverWait(self.driver, 600).until(EC.invisibility_of_element_located((By.XPATH, loadingXpath)))
        except Exception: pass


    def forceClick(self, button):
        self.windowFocus()

        # button click
        querySelector = '.' + '.'.join(button.get_attribute('class').split(' '))
        self.driver.execute_script(f'document.querySelector("{querySelector}").click()')


    def windowFocus(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.find_element_by_css_selector('body').click()


    def close(self):
        self.driver.quit()
