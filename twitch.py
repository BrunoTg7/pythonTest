import pyautogui
import time
import os
import tempfile

def ler_resultados_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return []
    with open(caminho_arquivo, "r") as f:
        resultados = [linha.strip().split(", ") for linha in f.readlines()]
    return [(r[2].split(": ")[1], r[3].split(": ")[1], r[4].split(": ")[1]) for r in resultados if len(r) > 9]  # Retornar nick, email, e senha

def abrir_browser(instancia):
    user_data_dir = os.path.join(tempfile.gettempdir(), f"edgeprofile{instancia}")
    os.makedirs(user_data_dir, exist_ok=True)
    pyautogui.hotkey('win', 'r')
    pyautogui.write(f'msedge --user-data-dir="{user_data_dir}" --inprivate')
    pyautogui.press('enter')
    time.sleep(5)

def logar_na_conta(nick, email, senha, instancia):
    abrir_browser(instancia)
    pyautogui.write('https://www.twitch.tv/login')
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.write(nick)
    pyautogui.press('tab')
    pyautogui.write(senha)
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(5)

    input("Pressione Enter após inserir o código de verificação e confirmar manualmente...")
    print(f"Login realizado para a conta {nick}")
    time.sleep(5)

# Ler resultados anteriores
resultados_aprovados = ler_resultados_arquivo("resultados_criacao_contas.txt")

# Logar em cada conta aprovada com instância diferente
for i, (nick, email, senha) in enumerate(resultados_aprovados):
    logar_na_conta(nick, email, senha, i)
