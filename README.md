# Carford 

A Carford é uma aplicação Flask projetada para gerenciar proprietários de carros e seus veículos em Nork-Town, uma cidade peculiar com regras específicas sobre a posse de automóveis.

* **Flask:** Framework web Python para desenvolvimento da API RESTful.
* **SQLModel:** ORM para interação com o banco de dados SQL, baseado no Pydantic e SQLAlchemy.
* **SQLite:** Banco de dados SQL leve e embutido, ideal para este projeto.
* **PyJWT:** Biblioteca para geração e validação de tokens JSON Web Tokens (JWT).
* **Bcrypt:** Biblioteca para hashing de senhas, garantindo segurança no armazenamento.
* **Docker:** Plataforma para conteinerização, simplificando a configuração e execução do ambiente de desenvolvimento.

## Funcionalidades

* **Gerenciamento de Proprietários:**
    * Adicionar proprietários.
    * Listar todos os proprietários, indicando se são oportunidades de venda.
    * Visualizar detalhes de um proprietário específico.
    * Atualizar informações de um proprietário.
    * Remover um proprietário (e seus carros associados).
* **Gerenciamento de Carros:**
    * Adicionar um carro, associando-o a um proprietário.
    * Listar todos os carros com seus respectivos proprietários.
    * Visualizar detalhes de um carro específico.
    * Atualizar informações de um carro.
    * Remover um carro (marcando o proprietário como oportunidade de venda, caso ele só tenha este carro associado).
* **Autenticação:**
    * Sistema de login para acessar os endpoints da API.
    * Geração e validação de tokens JWT para garantir a segurança das rotas.

## Validações

A API implementa as seguintes validações para garantir a integridade dos dados:

* **Proprietário (owner):**
    * **Campos obrigatórios:** `name`
    * **Limite de carros:** Um proprietário pode ter no máximo 3 carros.
* **Carro (car) :**
    * **Campos obrigatórios:** `model`, `color`, `owner_id`
    * **Valores permitidos para _model_:** `hatch`, `sedan` ou `convertible`
    * **Valores permitidos para _color_:** `yellow`, `blue` ou `gray`
    * **Proprietário existente:** O `owner_id` deve corresponder a um proprietário válido.
* **Autenticação:**
    * **Token JWT válido:** Todas as rotas protegidas exigem um token JWT válido. Por padrão, o tempo válido do token é de 15 minutos, sendo possível alterar o tempo no `.env`.
* **Códigos de Erro HTTP** 
   * A API foi equipada com os códigos de erro HTTP adequados para indicar o resultado das requisições, facilitando a identificação e resolução de problemas.

## Rotas da API

_Usuário padrão:_ **`username: admin`** | **`password: admin`**


| Método | Rota                 |  Descrição                                      | Body                             | Autenticação|
| ------ | -------------------- | ------------------------------------------------| --------                         | ----------- |
| POST    | `/`                 | Verificar o usuário no sistema (login)           | `username`, `passoword`          | Não         |  
| POST   | `/owner`             | Adicionar um proprietário ao sistema            | `name`                           | Sim         |
| GET    | `/owner`             | Listar todos os proprietários                   |   --                             | Sim         |
| GET    | `/owner/<id>`        | Visualizar um proprietário específico           |   --                             | Sim         |
| PATCH  | `/owner/<id>`        | Atualizar um proprietário                       |   `name`                         | Sim         |
| DELETE | `/owner/<id>`        | Remover um proprietário                         |   --                             | Sim         |
| GET    | `/car`               | Listar todos os carros                          |   --                             | Sim         |
| POST   | `/car`               | Adicionar um novo carro                         |   `color`, `model` `owner_id`    | Sim         |
| GET    | `/car/<id>`          | Listar um carro específico                      |    --                            | Sim         |
| PATCH  | `/car/<id>`          | Atualizar as informações do carro               |   `color`, `model` `owner_id`    | Sim         |
| DELETE | `/car/<id>`          | Apagar um carro                                 |    --                            | Sim         |
    


## Como Executar o Projeto

O projeto oferece duas opções para execução: com Docker (recomendado para ambiente consistente) ou sem Docker (para desenvolvimento local).

### Opção 1: Com Docker 

1. **Pré-requisitos:**
   * Docker e Docker Compose instalados.
2. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/lauannyrb/carford.git
   ```
3. **Acessar a pasta do projeto:**
   ```bash
   cd carford
   ```
4. **Copiar o arquivo de exemplo das variáveis de ambiente:**
   ```bash
   cp .env.example .env
   ```
5. **Criar e iniciar os containers:**
   ```bash
   docker-compose up -d --build
   ```

A API estará disponível em `http://localhost:5000`, ou então na porta definida no .env

### Opção 2: Sem Docker (Desenvolvimento Local)

1. **Pré-requisitos:**
   * Python 3.12 instalado.
   * Virtualenv (opcional, mas recomendado):
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
2. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Iniciar a aplicação:**
   ```bash
   python main.py
   ```
   
A API estará disponível em `http://localhost:5000`, ou então na porta definida no .env


## Testes Automatizados

A API inclui uma suíte de testes automatizados utilizando o framework Pytest para garantir a qualidade do código e o correto funcionamento das funcionalidades.

**Execução dos Testes:**

```bash
pytest -vv
```

**Cobertura dos Testes:**

* **Autenticação:**
    * Verifica se o login com credenciais inválidas retorna os erros apropriados.
    * Garante que apenas usuários autenticados podem acessar as rotas protegidas.
* **Gerenciamento de Proprietários:**
    * Testa a criação, listagem, visualização, atualização e exclusão de proprietários.
    * Verifica se a restrição de no máximo 3 carros por proprietário é respeitada.
* **Gerenciamento de Carros:**
    * Testa a criação, listagem, visualização, atualização e exclusão de carros.
    * Valida as cores e modelos permitidos para os carros.
    * Garante que um carro só pode ser criado se associado a um proprietário existente.
* **Validação de Dados:**
    * Verifica se os campos obrigatórios são fornecidos nas requisições.
    * Testa se os dados inválidos (cores, modelos, etc.) são rejeitados.
* **Tratamento de Erros:**
    * Garante que os códigos de erro HTTP corretos são retornados em caso de falhas.
    * Verifica se as mensagens de erro são informativas e úteis.
