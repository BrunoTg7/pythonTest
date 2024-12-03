import streamlit as st
import random
import string
from faker import Faker
import pyautogui
import time
import os
import tempfile
import psutil
import sched
import threading

fake = Faker()

# Funções para Gerar Dados Fictícios
def gerar_email_ficticio(nick, dominio="gmail.com"):
    return f"{nick}@{dominio}"

def gerar_senha_ficticia(tamanho=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choices(caracteres, k=tamanho))
    return senha

def gerar_nome_e_nick():
    nome = fake.first_name()
    sobrenome = fake.last_name()
    numero = ''.join(random.choices(string.digits, k=2))
    nick = f"{nome}{sobrenome}{numero}"
    return nome, sobrenome, nick

def gerar_data_nascimento():
    dia = random.randint(1, 28)
    mes = random.choice([
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ])
    ano = random.randint(1970, 2000)
    return dia, mes, ano

def gerar_genero():
    return random.choice(["Masculino", "Feminino"])

def gerar_dados_ficticios(quantidade):
    dados_ficticios = []
    for _ in range(quantidade):
        nome, sobrenome, nick = gerar_nome_e_nick()
        email = gerar_email_ficticio(nick)
        senha = gerar_senha_ficticia()
        dia, mes, ano = gerar_data_nascimento()
        genero = gerar_genero()
        dados_ficticios.append((nome, sobrenome, nick, email.split('@')[0], senha, dia, mes, ano, genero))

    with open("dados_ficticios.txt", "w") as f:
        for dados in dados_ficticios:
            f.write(f"Nome: {dados[0]}, Sobrenome: {dados[1]}, Nick: {dados[2]}, Email: {dados[3]}, Senha: {dados[4]}, Dia: {dados[5]}, Mes: {dados[6]}, Ano: {dados[7]}, Genero: {dados[8]}\n")

    st.success("Dados fictícios gerados e salvos com sucesso!")

# Funções para Criar Contas
def ler_dados_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r") as f:
        dados = [linha.strip().split(", ") for linha in f.readlines()]
    return [(d[0].split(": ")[1], d[1].split(": ")[1], d[2].split(": ")[1], d[3].split(": ")[1], d[4].split(": ")[1], d[5].split(": ")[1], d[6].split(": ")[1], d[7].split(": ")[1], d[8].split(": ")[1]) for d in dados]

def ler_resultados_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return []
    with open(caminho_arquivo, "r") as f:
        resultados = [linha.strip().split(", ") for linha in f.readlines()]
    return [(r[2].split(": ")[1], r[9].split(": ")[1]) for r in resultados if len(r) > 9]

def abrir_browser(instancia):
    user_data_dir = os.path.join(tempfile.gettempdir(), f"edgeprofile_{instancia}")
    os.makedirs(user_data_dir, exist_ok=True)
    os.system(f'start msedge --user-data-dir="{user_data_dir}" --inprivate')
    time.sleep(5)

def navegar_para_site():
    abrir_browser(0)  # Abre uma nova aba do navegador
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

    input("Pressione Enter após inserir o código de verificação e confirmar manualmente...")

def remover_linha_arquivo(caminho_arquivo, nick):
    with open(caminho_arquivo, "r") as f:
        linhas = f.readlines()
    with open(caminho_arquivo, "w") as f:
        for linha in linhas:
            if nick not in linha:
                f.write(linha)

def criar_contas():
    dados_ficticios = ler_dados_arquivo("dados_ficticios.txt")
    resultados_aprovados = ler_resultados_arquivo("resultados_criacao_contas.txt")

    for i, (nome, sobrenome, nick, email, senha, dia, mes, ano, genero) in enumerate(dados_ficticios):
        if any(res_nick == nick and status == "Aprovado" for res_nick, status in resultados_aprovados):
            st.write(f"O nick {nick} já foi aprovado anteriormente. Pulando...")
            continue

        abrir_browser(i)
        navegar_para_site()
        preencher_formulario(nome, sobrenome, nick, email, senha, dia, mes, ano)
        time.sleep(10)
        with open("resultados_criacao_contas.txt", "a") as f:
            f.write(f"Nome: {nome}, Sobrenome: {sobrenome}, Nick: {nick}, Email: {email_criado}, Senha: {senha}, Dia: {dia}, Mes: {mes}, Ano: {ano}, Genero: {genero}, Status: Aprovado\n")
        st.write(f"Conta criada para {nick} e resultado salvo com sucesso!")

        remover_linha_arquivo("dados_ficticios.txt", nick)

    st.success("Contas criadas com sucesso!")

# Funções para Fazer Login
def ler_resultados_login(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return []
    with open(caminho_arquivo, "r") as f:
        resultados = [linha.strip().split(", ") for linha in f.readlines()]
    return [(r[2].split(": ")[1], r[3].split(": ")[1], r[4].split(": ")[1]) for r in resultados if len(r) > 9]

def abrir_browser_login(instancia):
    user_data_dir = os.path.join(tempfile.gettempdir(), f"edgeprofile_login{instancia}")
    os.makedirs(user_data_dir, exist_ok=True)
    os.system(f'start msedge --user-data-dir="{user_data_dir}" --inprivate')
    time.sleep(5)

def logar_na_conta(nick, email, senha, instancia):
    abrir_browser_login(instancia)
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

def fazer_login():
    resultados_aprovados = ler_resultados_login("resultados_criacao_contas.txt")

    for i, (nick, email, senha) in enumerate(resultados_aprovados):
        logar_na_conta(nick, email, senha, i)

    st.success("Login realizado com sucesso!")

# Lista global para guardar informações sobre as abas abertas e estado automático
abertas = []
automatico_instancias_ativo = False
automatico_nova_janela_ativo = False
tempo_espera_instancias = 60
tempo_espera_nova_janela = 60
thread_instancias = None
thread_nova_janela = None
stop_event_instancias = threading.Event()
stop_event_nova_janela = threading.Event()

# Variáveis para estatísticas de uso
contador_iniciar_instancias = 0
contador_parar_instancias = 0
contador_iniciar_nova_janela = 0
contador_parar_nova_janela = 0

def abrir_instancias_navegador(urls, numero_instancias):
    global abertas
    def abrir_browser(instancia, url, browser='edge'):
        user_data_dir = os.path.join(tempfile.gettempdir(), f"{browser}_profile_{instancia}")
        os.makedirs(user_data_dir, exist_ok=True)
        if browser == 'edge':
            os.system(f'start msedge --user-data-dir="{user_data_dir}" --inprivate {url}')
        elif browser == 'chrome':
            os.system(f'start chrome --user-data-dir="{user_data_dir}" --incognito {url}')
        abertas.append((user_data_dir, browser))
        time.sleep(5)

    browsers = ['edge', 'chrome']
    for i in range(numero_instancias):
        url = urls[i % len(urls)]
        browser = browsers[i % len(browsers)]
        abrir_browser(i, url, browser)

def fechar_abas_instancias():
    global abertas
    # Fechar apenas abas anônimas do Edge e do Chrome usando psutil
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'msedge.exe' or proc.info['name'] == 'chrome.exe':
            try:
                proc_cmdline = proc.cmdline()
                if '--inprivate' in proc_cmdline or '--incognito' in proc.cmdline():
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    abertas = []

def fechar_abas_edge():
    # Fechar apenas abas anônimas do Edge usando psutil
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'msedge.exe':
            try:
                proc_cmdline = proc.cmdline()
                if '--inprivate' in proc.cmdline():
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

def abrir_nova_janela(url):
    fechar_abas_edge()
    time.sleep(2)
    os.system(f'start msedge --inprivate {url}')

def agendar_automatico_instancias(urls, numero_instancias, stop_event):
    while not stop_event.is_set():
        abrir_instancias_navegador(urls, numero_instancias)
        if stop_event.wait(tempo_espera_instancias):
            break
        fechar_abas_instancias()

def agendar_automatico_nova_janela(url, tempo_espera_nova_janela, stop_event):
    while not stop_event.is_set():
        abrir_nova_janela(url)
        if stop_event.wait(tempo_espera_nova_janela):
            break

def iniciar_automatico_instancias(urls, numero_instancias):
    global automatico_instancias_ativo, thread_instancias, stop_event_instancias, contador_iniciar_instancias
    automatico_instancias_ativo = True
    stop_event_instancias.clear()
    thread_instancias = threading.Thread(target=agendar_automatico_instancias, args=(urls, numero_instancias, stop_event_instancias))
    thread_instancias.start()
    contador_iniciar_instancias += 1
    st.success(f"Automático para Instâncias iniciado (estado: {automatico_instancias_ativo})")

def parar_automatico_instancias():
    global automatico_instancias_ativo, stop_event_instancias, thread_instancias, tempo_espera_instancias, contador_parar_instancias
    automatico_instancias_ativo = False
    stop_event_instancias.set()
    if thread_instancias is not None:
        thread_instancias.join()
        thread_instancias = None
    fechar_abas_instancias()
    tempo_espera_instancias = 0
    contador_parar_instancias += 1
    st.success(f"Automático para Instâncias parado (estado: {automatico_instancias_ativo})")

def iniciar_automatico_nova_janela(url, tempo_espera_nova_janela):
    global automatico_nova_janela_ativo, thread_nova_janela, stop_event_nova_janela, contador_iniciar_nova_janela
    automatico_nova_janela_ativo = True
    stop_event_nova_janela.clear()
    thread_nova_janela = threading.Thread(target=agendar_automatico_nova_janela, args=(url, tempo_espera_nova_janela, stop_event_nova_janela))
    thread_nova_janela.start()
    contador_iniciar_nova_janela += 1
    st.success(f"Automático para Nova Janela iniciado (estado: {automatico_nova_janela_ativo})")

def parar_automatico_nova_janela():
    global automatico_nova_janela_ativo, stop_event_nova_janela, thread_nova_janela, tempo_espera_nova_janela, contador_parar_nova_janela
    automatico_nova_janela_ativo = False
    stop_event_nova_janela.set()
    if thread_nova_janela is not None:
        thread_nova_janela.join()
        thread_nova_janela = None
    fechar_abas_edge()
    tempo_espera_nova_janela = 0
    contador_parar_nova_janela += 1
    st.success(f"Automático para Nova Janela parado (estado: {automatico_nova_janela_ativo})")

# Código de interface para integração do Streamlit

st.title("Ferramentas de Automação")

# Gerar Dados Fictícios
st.header("Gerar Dados Fictícios")
quantidade = st.number_input("Quantidade de Dados:", min_value=1, value=95, step=1)
if st.button("Gerar Dados"):
    gerar_dados_ficticios(quantidade)

# Criar Contas
st.header("Criar Contas")
if st.button("Criar Contas"):
    criar_contas()

# Fazer Login
st.header("Fazer Login")
if st.button("Fazer Login"):
    fazer_login()

# Abrir Múltiplas Instâncias do Navegador
st.header("Abrir Múltiplas Instâncias do Navegador")
num_instancias = st.number_input("Número de Instâncias:", min_value=1, value=5, step=1, key="num_instancias")
url_input_instancias = st.text_area("Insira URLs, uma por linha:", key="url_input_instancias")

if st.button("Abrir Navegador", key="abrir_navegador"):
    urls = [url.strip() for url in url_input_instancias.split('\n') if url.strip()]
    if num_instancias >= 20 and len(urls) == 1:
        urls = urls * num_instancias  # Repetir o link se for abrir 20 ou mais instâncias e apenas um link foi fornecido
    abrir_instancias_navegador(urls, num_instancias)
    time.sleep(3)

# Botão para Fechar Abas de Instâncias
if st.button("Fechar Abas (Instâncias)", key="fechar_abas_instancias"):
    fechar_abas_instancias()
    st.success("Todas as abas das instâncias foram fechadas com sucesso!")
# Abrir Nova Janela
st.header("Abrir e Fechar Janelas")
url_nova_janela = st.text_input("Insira a URL para abrir:", key="url_nova_janela")

if st.button("Abrir Nova Janela", key="abrir_nova_janela"):
    abrir_nova_janela(url_nova_janela)
    st.success(f"Janela nova aberta com a URL: {url_nova_janela}")
    time.sleep(5)


# Botão para Fechar Abas do Edge
if st.button("Fechar Abas (Edge)", key="fechar_abas_edge"):
    fechar_abas_edge()
    st.success("Todas as abas do Edge foram fechadas com sucesso!")

# Seletor de Tempo Automático para Instâncias
st.header("Controle Automático de Instâncias")

tempo_espera_instancias_selecao = st.selectbox("Selecione o intervalo de tempo para Instâncias:", options=["30s", "1min", "2min", "5min", "10min", "12min", "15min", "20min"], key="tempo_espera_instancias")

# Converta o tempo selecionado para segundos
tempos = {
    "30s": 30,
    "1min": 60,
    "2min": 120,
    "5min": 300,
    "10min": 600,
    "12min": 720,
    "15min": 900,
    "20min": 1200
}
tempo_espera_instancias = tempos[tempo_espera_instancias_selecao]

if st.button("Iniciar Automático (Instâncias)", key="iniciar_automatico_instancias"):
    urls = [url.strip() for url in url_input_instancias.split('\n') if url.strip()]
    threading.Thread(target=iniciar_automatico_instancias, args=(urls, num_instancias)).start()
    st.success(f"Automático iniciado para Instâncias com intervalo de {tempo_espera_instancias_selecao}")

if st.button("Parar Automático (Instâncias)", key="parar_automatico_instancias"):
    parar_automatico_instancias()
    st.success(f"Automático para Instâncias parado com sucesso. Estado: {automatico_instancias_ativo}")

# Seletor de Tempo Automático para Nova Janela
st.header("Controle Automático de Nova Janela")

tempo_espera_nova_janela_selecao = st.selectbox("Selecione o intervalo de tempo para Nova Janela:", options=["30s", "1min", "2min", "5min", "10min", "12min", "15min", "20min"], key="tempo_espera_nova_janela")

# Converta o tempo selecionado para segundos
tempos_nova_janela = {
    "30s": 30,
    "1min": 60,
    "2min": 120,
    "5min": 300,
    "10min": 600,
    "12min": 720,
    "15min": 900,
    "20min": 1200
}
tempo_espera_nova_janela = tempos_nova_janela[tempo_espera_nova_janela_selecao]

if st.button("Iniciar Automático (Nova Janela)", key="iniciar_automatico_nova_janela"):
    threading.Thread(target=iniciar_automatico_nova_janela, args=(url_nova_janela, tempo_espera_nova_janela)).start()
    st.success(f"Automático iniciado para Nova Janela com intervalo de {tempo_espera_nova_janela_selecao}")

if st.button("Parar Automático (Nova Janela)", key="parar_automatico_nova_janela"):
    parar_automatico_nova_janela()
    st.success(f"Automático para Nova Janela parado com sucesso. Estado: {automatico_nova_janela_ativo}")

# Exibir o estado atual dos processos automáticos
st.header("Estado Atual dos Processos Automáticos")
st.write(f"Estado automático das instâncias: {automatico_instancias_ativo}")
st.write(f"Estado automático da nova janela: {automatico_nova_janela_ativo}")

# Estatísticas de uso
st.header("Estatísticas de Uso")
st.write(f"Contador iniciar instâncias: {contador_iniciar_instancias}")
st.write(f"Contador parar instâncias: {contador_parar_instancias}")
st.write(f"Contador iniciar nova janela: {contador_iniciar_nova_janela}")
st.write(f"Contador parar nova janela: {contador_parar_nova_janela}")
