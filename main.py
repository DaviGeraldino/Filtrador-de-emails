#Filtrador de emails 

#impotando as blibliotecas
import imaplib
import email
from email.header import decode_header


#credenciais de loggin no email
email_usuario = "seuemaial@gmail.com" #aqui cooloque o seu email !!!!
senha = "suasenha" #aqui coloque a sua senha de app (procure saber sobre senha de app caso voce nao saiba) deve vir algo como "abc def ghij klm"!!!!

#conectando ao servidor de email
mail = imaplib.IMAP4_SSL("imap.gmail.com")
print("Conectado ao servidor de email")

#fazendo login
mail.login(email_usuario, senha)

#selecionando a caixa de entrada e pegando todos os emails
mail.select("inbox")
status, dados = mail.search(None, 'FROM "email@dominio.com"') #aqui coloque o email do remetente que voce quer filtar os dados
lista_emails = dados[0].split()#transformando a string de emails em uma lista de emails

print (f"Total de emails: {len(lista_emails)}")#len lista == vai perga a quantidade de emails 

#ESSA PARTE FOI INUTILIZADA POIS NAO FOI NECESSARIO PEGAR OS CINCO ULTIMOS EMAILS
#pegando os ultimos cinco emails da lista(caixa de entrada)
#lista_emails = lista_emails[-5:]
#print ("Últimos 5 emails:")

# Percorrendo a lista de emails para pegar os assuntos dos emails
for email_id in lista_emails:
    status, dados = mail.fetch(email_id, "(RFC822)")#pegando o email inteiro, incluindo o cabeçalho e o corpo do email
    raw_email = dados[0][1]#pegando o email em formato bruto (bytes)
    msg = email.message_from_bytes(raw_email)#transformando o email em um objeto(facilitar a leitura do email)
    assunto, encoding = decode_header(msg["subject"])[0]#decodificando o email
    
    #verificando se o assunto do email é bytes
    if isinstance(assunto, bytes):
        assunto = assunto.decode(encoding if encoding else "utf-8")#decodificando o assunto do email para utf-8
   
    #pegando o remetente do email
    remetente = msg["from"]
    
    #pegando o corpo do email
    corpo_email = ""
    if msg.is_multipart():#verifica se o email tem varias partes
        for part in msg.walk():#percorre as partes do email
            tipo = part.get_content_type()#pegando o tipo do email (texto, imagem, etc)
            if tipo == "text/plain":#verificando se o tipo do email é texto
                corpo_email = part.get_payload(decode=True).decode("utf-8", errors="ignore")#decodificando o corpo do email
                break
    else:
        corpo_email = msg.get_payload(decode=True).decode("utf-8", errors="ignore")#decodificando o corpo do email
   
   #imprimindo os emails 
    print(f"""Assunto: {assunto}
Remetente: {remetente}
Corpo do email: {corpo_email[:200]}
          {'-' * 40}""")

