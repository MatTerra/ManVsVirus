# Man VS Virus

Aqui vai um parágrafo de descrição do seu projeto

## Primeiros Passos

Para instalar uma versão de desenvolvimento do sistema, siga os passos abaixo.
Para fazer o deploy do sistema para produção, confira a seção de [Deploy](#deploy)

### Pré requisitos

O backend do sistema é desenvolvido em python e pensado para rodar em um cluster kubernetes. O frontend é desenvolvido em React e pode ser servido em um servidor comum ou em um container em um cluster kubernetes.

É necessário um sistema de gerenciamento de usuários compatível com a especificação swagger abaixo e que forneça um token JWT como resposta.

```
basePath: '/v1'

paths:
  /users:
    post:
      description: Cria um novo usuário
      parameters:
      - name: 'user'
        in: body
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
            passwordConfirmation:
              type: string
  /users/login
    post:
      description: Faz o login
      parameters:
      - name: 'user'
        in: body
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
      responses:
        200:
          schema:
            type: object
            properties:
              httpStatusCode: 
                type: string
              success:
                type: string
              message:
                type: string
              data:
                type: object
                properties:
                  token:
                    type: string
                  tokenExpirationDate:
                    type: string
                  status:
                    type: string
```

Por enquanto o sistema que utilizo é proprietário, se e quando for disponibilizado, acresentarei as informações de deploy dele, bem como o link para o repo. Por enquanto, você pode utilizar o flask + connexion para fazer uma api em python, inclusive a definição acima pode ser utilizada para o arquivo .yml da api.

Antes de prosseguir para a instalação, baixe e instale o python, o node e o npm em seu computador. Utilizo Linux para o desenvolvimento então nunca instalei as dependências do React em um sistema windows. Contudo, não deve ser nada complicado e uma rápida pesquisa no google terá a resposta. Recomendo que você utilize o Visual Studio Code para o desenvolvimento em React. Para o desenvolvimento em python, costumo usar o PyCharm, mas você pode usar o Visual Studio Code também.

### Instalando

Para configurar nosso ambiente de desenvolvimento, vamos começar preparando o ambiente do backend. Caso você não tenha instalado junto com o python, instale o pyenv. Embora você possa instalar todas as bibliotecas que utilizaremos na sua instalação padrão do python, recomendo fortemente que você não pule as etapas de configuração do ambiente virtual para evitar conflitos de versão com outros projetos.

Com o pyenv instalado, vamos baixar a versão 3.8.2 do python. Caso sua distribuição não forneça os binários para esta versão, utilize a versão estável mais recente.

```
$ pyenv install 3.8.2
```

Depois de instalado, o python 3.8.2 deve estar disponível em /home/your_user/.pyenv/versions/3.8.2. Caso queira confirmar o local, você pode repetir o comando acima.

Em seguida, vamos instalar o virtualenv para gerar nosso ambiente virtual, para isso rode o comando abaixo(podem ser necessárias permissões de superusuário):

```
# pip install virtualenv 
```

Com o virtualenv instalado vamos criar o ambiente virtual com o comando abaixo. Corrija o endereço do python para o que instalamos com o pyenv.

```
$ virtualenv -p /home/user/.pyenv/versions/3.8.2/bin/python venv
```

Depois que o ambiente estiver criado, ative-o com o comando abaixo. (Para desativar utilize `deactivate`)

```
$ source venv/bin/activate
```

Para verificar a configuração do sistema, rode o comando abaixo e verifique se a saída é como a apresentada:
```
$ python --version
Python 3.8.2
```

Para instalar as bibliotecas necessárias, acesse a pasta raiz do projeto e execute o comando abaixo com o ambiente virtual ativado:
```
$ pip install -r requirements.txt
```

Agora continuaremos para a configuração do React.

Utilizaremos o yarn como gerenciador de pacotes. Para instalar as dependências, rode o comando abaixo após instalar o yarn.

```
$ yarn install
```

Em seguida, inicie o servidor de teste com o comando abaixo:

```
$ yarn start
```

Em seguida, acesse o teste em localhost:3000

## Rodando os testes

**TODO** Os teste unitários ainda não foram desenvolvidos... Infelizmente não começamos o projeto usando TDD, mas provavelmente acresentaremos eles durante os próximos dias. (Se você está vendo esse README anos depois dele ter sido escrito e ainda não existem testes... Sinto muito)

### Quebre em teste de ponta a ponta

Ainda não temos...

### E testes de estilo de código

Existirão!

## Deploy

Adicione notas para deploy para produção

## Ferramentas de build

* [yarn](https://yarnpkg.com/) - Gerenciador de pacotes do React
* Não temos ferramentas de build para o python.

## Contribuindo

Por favor leia [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes do nosso código de conduta e do processo de submissão de PR's para nós.

## Versionamento

Usamos [SemVer](http://semver.org/) para versionamento. Para versões disponíveis, veja as [tags nesse repositório](tags). 

## Autores

* **Mateus Berardo** - *Trabalho Inicial* - [MatTerra](https://github.com/MatTerra)

Veja também a lista de [contribuidores](contributors) que participaram nesse projeto.

## Licença

Esse projeto está licenciado sob uma licença GNU v3 - veja o arquivo [LICENSE](LICENSE) para detalhes

## Agradecimentos

* **Billie Thompson** - *Trabalho Inicial do Modelo de README* - [PurpleBooth](https://github.com/PurpleBooth)

