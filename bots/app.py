from flask import Flask, request, jsonify, render_template
import random
import string
from faker import Faker
import pyautogui
import time
import os
import tempfile
import psutil
import threading
import pyperclip

app = Flask(__name__)
fake = Faker()

# Variáveis globais
automatico_instancias_ativo = False
automatico_nova_janela_ativo = False
stop_event_instancias = threading.Event()
stop_event_nova_janela = threading.Event()
thread_instancias = None
thread_nova_janela = None
contador_iniciar_instancias = 0
contador_parar_instancias = 0
contador_iniciar_nova_janela = 0
contador_parar_nova_janela = 0

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
        dados_ficticios.append({
            "nome": nome,
            "sobrenome": sobrenome,
            "nick": nick,
            "email": email.split('@')[0],
            "senha": senha,
            "dia": dia,
            "mes": mes,
            "ano": ano,
            "genero": genero
        })
    # Salvar os dados no arquivo
    with open("dados_ficticios.txt", "w") as f:
        for dado in dados_ficticios:
            f.write(f"{dado['nome']},{dado['sobrenome']},{dado['nick']},{dado['email']},{dado['senha']},{dado['dia']},{dado['mes']},{dado['ano']},{dado['genero']}\n")
    return dados_ficticios

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_data', methods=['GET'])
def generate_data():
    quantidade = int(request.args.get('quantidade', 1))
    dados = gerar_dados_ficticios(quantidade)
    return jsonify(dados)

def ler_dados_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r") as f:
        dados = [linha.strip().split(",") for linha in f.readlines()]
    dados_corrigidos = []
    for d in dados:
        try:
            dados_corrigidos.append((d[0], d[1], d[2], d[3], d[4], int(d[5]), d[6], int(d[7]), d[8]))
        except ValueError as e:
            print(f"Erro ao converter dados: {e}. Linha: {d}")
            continue  # Ignora a linha que causou o erro
    return dados_corrigidos


def ler_resultados_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return []
    with open(caminho_arquivo, "r") as f:
        resultados = [linha.strip().split(",") for linha in f.readlines()]
    return [(r[2].split()[-1].strip(), r[9].split()[-1].strip()) for r in resultados if len(r) > 9]



def abrir_browser(instancia):
    user_data_dir = os.path.join(tempfile.gettempdir(), f"edgeprofile_{instancia}")
    os.makedirs(user_data_dir, exist_ok=True)
    os.system(f'start msedge --user-data-dir="{user_data_dir}" --inprivate')
    time.sleep(5)

def navegar_para_site():
    pyautogui.write('https://www.twitch.tv/')
    pyautogui.press('enter')
    time.sleep(10)

def preencher_formulario(nome, sobrenome, nick, email, senha, dia, mes, ano):
    global email_criado
    email_criado = f'bruno2004antoniotg+{email}@gmail.com'
    pyautogui.click(x=1733, y=128)
    time.sleep(1)
    pyautogui.write(nick)
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.typewrite(senha, interval=0.1)
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

def remover_linha_arquivo(caminho_arquivo, nick):
    with open(caminho_arquivo, "r") as f:
        linhas = f.readlines()
    with open(caminho_arquivo, "w") as f:
        for linha in linhas:
            if nick not in linha:
                f.write(linha)

@app.route('/criar_contas', methods=['POST'])
def criar_contas():
    dados_ficticios = ler_dados_arquivo("dados_ficticios.txt")
    resultados_aprovados = ler_resultados_arquivo("resultados_criacao_contas.txt")
    for i, (nome, sobrenome, nick, email, senha, dia, mes, ano, genero) in enumerate(dados_ficticios):
        if any(res_nick == nick and status == "Aprovado" for res_nick, status in resultados_aprovados):
            continue
        abrir_browser(i)
        navegar_para_site()
        preencher_formulario(nome, sobrenome, nick, email, senha, dia, mes, ano)
        time.sleep(10)
        with open("resultados_criacao_contas.txt", "a") as f:
            f.write(f"Nome: {nome}, Sobrenome: {sobrenome}, Nick: {nick}, Email: {email_criado}, Senha: {senha}, Dia: {dia}, Mes: {mes}, Ano: {ano}, Genero: {genero}, Status: Aprovado\n")
        remover_linha_arquivo("dados_ficticios.txt", nick)
    return jsonify({"status": "Contas criadas com sucesso!"})

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
    time.sleep(8)
    print("Nick:", nick)  # Log para depuração
    print("Email:", email)  # Log para depuração
    print("Senha:", senha)  # Log para depuração
    pyautogui.write(nick)
    pyautogui.press('tab')
    time.sleep(1)
    pyperclip.copy(senha)  # Copia a senha para a área de transferência
    pyautogui.hotkey('ctrl', 'v')  # Cola a senha no campo de senha
    print("Senha digitada:", senha)  # Log para verificar a senha digitada
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(5)

    input("Pressione Enter após inserir o código de verificação e confirmar manualmente...")
    print(f"Login realizado para a conta {nick}")
    time.sleep(5)

@app.route('/fazer_login', methods=['POST'])
def fazer_login():
    resultados_aprovados = ler_resultados_login("resultados_criacao_contas.txt")
    for i, (nick, email, senha) in enumerate(resultados_aprovados):
        logar_na_conta(nick, email, senha, i)
    return jsonify({"status": "Login realizado com sucesso!"})


@app.route('/abrir_instancias', methods=['POST'])
def abrir_instancias():
    data = request.json
    urls = data.get('urls', [])
    numero_instancias = int(data.get('numero_instancias', 1))
    abrir_instancias_navegador(urls, numero_instancias)
    return jsonify({"status": "Instâncias do navegador abertas com sucesso!"})

def abrir_instancias_navegador(urls, numero_instancias):
    def abrir_browser(instancia, url, browser='edge'):
        user_data_dir = os.path.join(tempfile.gettempdir(), f"{browser}_profile_{instancia}")
        os.makedirs(user_data_dir, exist_ok=True)
        if browser == 'edge':
            os.system(f'start msedge --user-data-dir="{user_data_dir}" --inprivate {url}')
        elif browser == 'chrome':
            os.system(f'start chrome --user-data-dir="{user_data_dir}" --incognito {url}')
        time.sleep(5)

    browsers = ['edge', 'chrome']
    for i in range(numero_instancias):
        url = urls[i % len(urls)]
        browser = browsers[i % len(browsers)]
        abrir_browser(i, url, browser)

def fechar_abas_instancias():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'msedge.exe' or proc.info['name'] == 'chrome.exe':
            try:
                proc_cmdline = proc.cmdline()
                if '--inprivate' in proc_cmdline or '--incognito' in proc.cmdline():
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

@app.route('/fechar_abas_instancias', methods=['POST'])
def fechar_abas_instancias_route():
    fechar_abas_instancias()
    return jsonify({"status": "Todas as abas das instâncias foram fechadas com sucesso!"})

def abrir_nova_janela(url):
    os.system(f'start msedge --inprivate {url}')


@app.route('/abrir_nova_janela', methods=['POST'])
def abrir_nova_janela_route():
    data = request.json
    url = data.get('url')
    abrir_nova_janela(url)
    return jsonify({"status": f"Nova janela aberta com a URL: {url}"})

def fechar_abas_edge():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'msedge.exe':
            try:
                proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

@app.route('/fechar_abas_edge', methods=['POST'])
def fechar_abas_edge_route():
    fechar_abas_edge()
    return jsonify({"status": "Todas as abas do Edge foram fechadas com sucesso!"})


def agendar_automatico_instancias(urls, numero_instancias, tempo_espera_instancias, stop_event):
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
        fechar_abas_edge()


@app.route('/iniciar_automatico_instancias', methods=['POST'])
def iniciar_automatico_instancias():
    global automatico_instancias_ativo, thread_instancias, stop_event_instancias, contador_iniciar_instancias
    data = request.json
    urls = data.get('urls', [])
    numero_instancias = int(data.get('numero_instancias', 1))
    tempo_espera_instancias = int(data.get('tempo_espera_instancias', 60))
    automatico_instancias_ativo = True
    stop_event_instancias.clear()
    thread_instancias = threading.Thread(target=agendar_automatico_instancias, args=(urls, numero_instancias, tempo_espera_instancias, stop_event_instancias))
    thread_instancias.start()
    contador_iniciar_instancias += 1
    return jsonify({"status": f"Automático para Instâncias iniciado (estado: {automatico_instancias_ativo})"})

@app.route('/parar_automatico_instancias', methods=['POST'])
def parar_automatico_instancias():
    global automatico_instancias_ativo, stop_event_instancias, thread_instancias, contador_parar_instancias
    automatico_instancias_ativo = False
    stop_event_instancias.set()
    if thread_instancias is not None:
        thread_instancias.join()
        thread_instancias = None
    fechar_abas_instancias()
    contador_parar_instancias += 1
    return jsonify({"status": f"Automático para Instâncias parado (estado: {automatico_instancias_ativo})"})

@app.route('/iniciar_automatico_nova_janela', methods=['POST'])
def iniciar_automatico_nova_janela():
    global automatico_nova_janela_ativo, thread_nova_janela, stop_event_nova_janela, contador_iniciar_nova_janela
    data = request.json
    url = data.get('url')
    tempo_espera_nova_janela = int(data.get('tempo_espera_nova_janela', 60))
    automatico_nova_janela_ativo = True
    stop_event_nova_janela.clear()
    thread_nova_janela = threading.Thread(target=agendar_automatico_nova_janela, args=(url, tempo_espera_nova_janela, stop_event_nova_janela))
    thread_nova_janela.start()
    contador_iniciar_nova_janela += 1
    return jsonify({"status": f"Automático para Nova Janela iniciado (estado: {automatico_nova_janela_ativo})"})

@app.route('/parar_automatico_nova_janela', methods=['POST'])
def parar_automatico_nova_janela():
    global automatico_nova_janela_ativo, stop_event_nova_janela, thread_nova_janela, contador_parar_nova_janela
    automatico_nova_janela_ativo = False
    stop_event_nova_janela.set()
    if thread_nova_janela is not None:
        thread_nova_janela.join()
        thread_nova_janela = None
    fechar_abas_edge()
    contador_parar_nova_janela += 1
    return jsonify({"status": f"Automático para Nova Janela parado (estado: {automatico_nova_janela_ativo})"})


@app.route('/status', methods=['GET'])
def status():
    status_data = {
        "Estado automático das instâncias": automatico_instancias_ativo,
        "Estado automático da nova janela": automatico_nova_janela_ativo,
    }
    return jsonify(status_data)

@app.route('/estatisticas', methods=['GET'])
def estatisticas():
    stats = {
        "Contador iniciar instâncias": contador_iniciar_instancias,
        "Contador parar instâncias": contador_parar_instancias,
        "Contador iniciar nova janela": contador_iniciar_nova_janela,
        "Contador parar nova janela": contador_parar_nova_janela
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
