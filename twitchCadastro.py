import pyautogui
import time
import random
import string
from faker import Faker
import os
import tempfile

fake = Faker()

def ler_dados_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r") as f:
        dados = [linha.strip().split(", ") for linha in f.readlines()]
    return [(d[0].split(": ")[1], d[1].split(": ")[1], d[2].split(": ")[1], d[3].split(": ")[1], d[4].split(": ")[1], d[5].split(": ")[1], d[6].split(": ")[1], d[7].split(": ")[1], d[8].split(": ")[1]) for d in dados]

def ler_resultados_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return []
    with open(caminho_arquivo, "r") as f:
        resultados = [linha.strip().split(", ") for linha in f.readlines()]
    return [(r[2].split(": ")[1], r[9].split(": ")[1]) for r in resultados if len(r) > 9]  # Retornar apenas o nick e o status

def abrir_browser(instancia):
    user_data_dir = os.path.join(tempfile.gettempdir(), f"edgeprofile_{instancia}")
    os.makedirs(user_data_dir, exist_ok=True)
    os.system(f'start msedge --user-data-dir="{user_data_dir}" --inprivate')
    time.sleep(5)

def navegar_para_site():
    pyautogui.write('https://www.twitch.tv/')
    pyautogui.press('enter')
    time.sleep(5)

def preencher_formulario(nome, sobrenome, nick, email, senha, dia, mes, ano):
    global email_criado
    email_criado = f'bruno2004antoniotg+{email}@gmail.com'
    pyautogui.click(x=1733, y=128)
    time.sleep(1)
    pyautogui.write(nick)
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.write(senha)
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.write(str(dia))
    pyautogui.press('tab')
    pyautogui.write(mes)
    pyautogui.press('tab')
    pyautogui.write(str(ano))
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.hotkey('shift', 'tab')
    time.sleep(2)
    pyautogui.write(email_criado)
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(2)
    pyautogui.press('tab')
    pyautogui.press('enter')

    # Esperar pela sua permissão antes de continuar
    input("Pressione Enter após inserir o código de verificação e confirmar manualmente...")

def remover_linha_arquivo(caminho_arquivo, nick):
    with open(caminho_arquivo, "r") as f:
        linhas = f.readlines()
    with open(caminho_arquivo, "w") as f:
        for linha in linhas:
            if nick not in linha:
                f.write(linha)

# Ler dados fictícios
dados_ficticios = ler_dados_arquivo("dados_ficticios.txt")
# Ler resultados anteriores
resultados_aprovados = ler_resultados_arquivo("resultados_criacao_contas.txt")

# Processar cada dado fictício
for i, (nome, sobrenome, nick, email, senha, dia, mes, ano, genero) in enumerate(dados_ficticios):
    # Verificar se o nick já foi aprovado anteriormente
    if any(res_nick == nick and status == "Aprovado" for res_nick, status in resultados_aprovados):
        print(f"O nick {nick} já foi aprovado anteriormente. Pulando...")
        continue

    abrir_browser(i)
    navegar_para_site()
    preencher_formulario(nome, sobrenome, nick, email, senha, dia, mes, ano)
    time.sleep(10)
    # Salvar o resultado em um arquivo no formato desejado
    with open("resultados_criacao_contas.txt", "a") as f:
        f.write(f"Nome: {nome}, Sobrenome: {sobrenome}, Nick: {nick}, Email: {email_criado}, Senha: {senha}, Dia: {dia}, Mes: {mes}, Ano: {ano}, Genero: {genero}, Status: Aprovado\n")
    print(f"Conta criada para {nick} e resultado salvo com sucesso!")

    # Remover a linha correspondente do arquivo de dados fictícios
    remover_linha_arquivo("dados_ficticios.txt", nick)
