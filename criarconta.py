from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def ler_dados_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"O arquivo {caminho_arquivo} não foi encontrado.")
        
    with open(caminho_arquivo, "r") as f:
        dados = [linha.strip().split(", ") for linha in f.readlines()]
    return [(d[0].split(": ")[1], d[1].split(": ")[1], d[2].split(": ")[1], d[3].split(": ")[1], d[4].split(": ")[1], d[5].split(": ")[1], d[6].split(": ")[1], d[7].split(": ")[1], d[8].split(": ")[1]) for d in dados]

def criar_conta(driver, nome, sobrenome, email, senha, dia, mes, ano, genero):
    driver.get("https://accounts.google.com/signup")
    sufixo = 1
    email_final = email
    
    telefone_index = 0  # Índice inicial para os números de telefone

    try:
        # Preencher o nome e sobrenome e avançar para o próximo passo com Enter
        print("Preenchendo nome e sobrenome...")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(nome)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "lastName"))).send_keys(sobrenome + Keys.RETURN)
        time.sleep(5)

        # Preencher a data de nascimento
        print("Preenchendo data de nascimento...")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "day"))).send_keys(dia)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "month"))).send_keys(mes)
        campo_ano = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "year")))
        campo_ano.send_keys(ano)
        time.sleep(5)

        # Selecionar o gênero
        print("Selecionando gênero...")
        genero_dropdown = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "gender")))
        genero_dropdown.click()
        
        if genero == "Feminino":
            webdriver.ActionChains(driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.RETURN).perform()
        else:
            webdriver.ActionChains(driver).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.RETURN).perform()
        
        time.sleep(2)

        # Voltar para o campo do ano e pressionar Enter novamente
        campo_ano.click()
        campo_ano.send_keys(Keys.RETURN)
        time.sleep(5)

        while True:
            try:
                # Inserir o email diretamente no campo de email
                print("Inserindo email...")
                email_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "Username")))
                email_field.click()
                email_field.clear()
                time.sleep(1)  # Pausa antes de enviar as teclas
                email_field.send_keys(email_final)
                time.sleep(1)  # Pausa depois de enviar o email
                email_field.send_keys(Keys.RETURN)

                print(f"Processed email: {email_final}")  # Adicionar print para verificar processed_email no terminal

                time.sleep(5)
                
                # Verificar se há erro de email em uso
                erro_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@jsname='B34EJ']")))
                if erro_element.is_displayed() and "já está em uso" in erro_element.text:
                    print("Email já está em uso, modificando email...")
                    sufixo += 1
                    email_final = f"{email_final}{sufixo}"
                    continue  # Tentar novamente com o novo email
                
                break  # Se o email foi aceito, sair do loop

            except:
                break  # Se ocorrer uma exceção, sair do loop

        # Preencher a senha e confirmar a senha
        print("Preenchendo senha...")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(senha)
        time.sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "PasswdAgain"))).send_keys(senha)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "PasswdAgain"))).send_keys(Keys.RETURN)
        time.sleep(5)

        while True:
            try:
                # Inserir o número de telefone com DDD da Austrália
                telefone = numeros_telefone[telefone_index]
                print(f"Inserindo número de telefone: {telefone}")
                telefone_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "phoneNumberId")))
                telefone_field.click()
                telefone_field.clear()
                time.sleep(1)
                telefone_field.send_keys(telefone)
                telefone_field.send_keys(Keys.RETURN)
                time.sleep(3) 

                # Verificar se há erro de número de telefone usado muitas vezes
                erro_telefone_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@jsname='B34EJ']")))
                if erro_telefone_element.is_displayed() and ("usado muitas vezes" in erro_telefone_element.text or "não pode ser usado para verificação" in erro_telefone_element.text):
                    print("Número de telefone já foi usado muitas vezes, mudando número...")
                    telefone_index = (telefone_index + 1) % len(numeros_telefone)
                    continue  # Tentar novamente com o novo número de telefone

                break  # Se o telefone foi aceito, sair do loop

            except:
                break  # Se ocorrer uma exceção, sair do loop

        print("Aguardando inserção manual do código SMS...")
        input("Pressione Enter após inserir o código SMS manualmente...")

        # Verificação de sucesso
        if "Welcome" in driver.title:
            print("Conta criada com sucesso!")
            return "Aprovado", email_final
        else:
            print("Falha ao criar a conta.")
            return "Reprovado", email_final
    
    except Exception as e:
        print(f"Erro ao criar conta: {e}")
        return "Reprovado", email_final

# Configuração do WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)

# Ler dados do arquivo
dados_ficticios = ler_dados_arquivo("dados_ficticios.txt")

# Lista para registrar os resultados
resultados = []

# Criar contas de e-mail para os dados fictícios
for nome, sobrenome, nick, email, senha, dia, mes, ano, genero in dados_ficticios:
    status, email_final = criar_conta(driver, nome, sobrenome, email, senha, dia, mes, ano, genero)
    resultados.append((nome, sobrenome, nick, email_final, senha, dia, mes, ano, genero, status))

driver.quit()

# Salvar os resultados em um arquivo
with open("resultados_criacao_contas.txt", "w") as f:
    for data in resultados:
        f.write(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]},{data[7]},{data[8]},{data[9]}\n")

print("Contas de e-mail processadas e resultados salvos com sucesso!")
