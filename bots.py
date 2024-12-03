import random
import string
from faker import Faker

fake = Faker()

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
    dia = random.randint(1, 28)  # Escolha segura para todos os meses
    mes = random.choice([
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ])
    ano = random.randint(1970, 2000)
    return dia, mes, ano

def gerar_genero():
    return random.choice(["Masculino", "Feminino"])

# Gerar uma lista de 5.000 dados fictícios
dados_ficticios = []
for _ in range(95):
    nome, sobrenome, nick = gerar_nome_e_nick()
    email = gerar_email_ficticio(nick)
    senha = gerar_senha_ficticia()
    dia, mes, ano = gerar_data_nascimento()
    genero = gerar_genero()
    # Salvar apenas o nome do email sem o domínio
    dados_ficticios.append((nome, sobrenome, nick, email.split('@')[0], senha, dia, mes, ano, genero))

# Salvar a lista de dados fictícios em um arquivo
with open("dados_ficticios.txt", "w") as f:
    for dados in dados_ficticios:
        f.write(f"Nome: {dados[0]}, Sobrenome: {dados[1]}, Nick: {dados[2]}, Email: {dados[3]}, Senha: {dados[4]}, Dia: {dados[5]}, Mes: {dados[6]}, Ano: {dados[7]}, Genero: {dados[8]}\n")

print("Dados fictícios gerados e salvos com sucesso!")
