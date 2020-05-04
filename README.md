### Introduction

CRUD simples implementado em python utilizando flask, flask-jwt-extended, flask-restx and flask-sqlalchemy.

A API possui swagger ativo para testes de funcionamento.

### Configuração

Para que o projeto funcione corretamente, deve-se configurar as seguintes variaveis de ambiente para os containers

`
.env/db.env

MYSQL_ROOT_PASSWORD=<SENHA_ROOT>
MYSQL_DATABASE=<NOME_DATABASE>


.env/api.env

SECRET=<Chave que será utilizada pelo flask-jwt-extended para criptografar os tokens JWT>
SQLALCHEMY_DATABASE_URI=<URI para acesso ao banco de dados no padrão mysql+pymysql://<usuario>:<senha>@<host>/<db_name>


### Instalação

*Requer o docker instalado*

1 - Clonar o repo

`git clone git@github.com:fnalonso/flask-api-restx.git`

2 - Efetuar a build das imagens

`docker-compose build`

3 - Subir os containers

`docker-compose up`

### Utilização

 1. Acessar o [swagger](http://localhost:5000)
 2. Criar um usuário `POST /users`
 3. Efetuar a autenticação em `POST /users/login`
 4. Configurar o token de autorização retornado no passo anterior no swagger com o valor `Bearer {access_token}`
 
 Os endpoints `cats` e `dogs` exigem Token para os métodos `POST, PUT e DELETE`.
 