# Carford 

A Carford é uma aplicação Flask projetada para gerenciar proprietários de carros e seus veículos em Nork-Town, uma cidade peculiar com regras específicas sobre a posse de automóveis.

* **Flask:** Framework web Python para desenvolvimento da API RESTful.
* **SQLModel:** ORM para interação com o banco de dados SQL, baseado no Pydantic e SQLAlchemy.
* **SQLite:** Banco de dados SQL leve e embutido, ideal para este projeto.
* **PyJWT:** Biblioteca para geração e validação de tokens JSON Web Tokens (JWT).
* **bcrypt:** Biblioteca para hashing de senhas, garantindo segurança no armazenamento.
* **Docker:** Plataforma para conteinerização, simplificando a configuração e execução do ambiente de desenvolvimento.

## Funcionalidades

* **Gerenciamento de Proprietários:**
    * Adicionar proprietários de carros (com ou sem carros).
    * Listar todos os proprietários, indicando se são oportunidades de venda.
    * Visualizar detalhes de um proprietário específico.
    * Atualizar informações de um proprietário.
    * Remover um proprietário (e seus carros associados).
* **Gerenciamento de Carros:**
    * Adicionar um carro, associando-o a um proprietário.
    * Listar todos os carros com seus respectivos proprietários.
    * Visualizar detalhes de um carro específico.
    * Atualizar informações de um carro.
    * Remover um carro (marcando o proprietário como oportunidade de venda).
* **Autenticação:**
    * Sistema de login para acessar os endpoints da API.
    * Geração e validação de tokens JWT para garantir a segurança das rotas.

## Restrições de Negócio

* Um proprietário pode ter no máximo 3 carros.
* Um carro deve estar sempre associado a um proprietário.
* As cores permitidas para os carros são: 'amarelo', 'azul' e 'cinza'.
* Os modelos permitidos para os carros são: 'hatch', 'sedan' e 'conversível'.

## Rotas da API

| Método | Rota                 | Descrição                                       | Autenticação |
| ------ | -------------------- | ------------------------------------------------ | ----------- |
| GET    | `/`                  | Verificar o usuário no sistema (login)           | Não         |
| POST   | `/owner`             | Adicionar proprietário de carro                  | Sim         |
| GET    | `/owner`             | Listar todos os proprietários                    | Sim         |
| GET    | `/owner/<id>`        | Visualizar um proprietário específico            | Sim         |
| PATCH  | `/owner/<id>`        | Atualizar um proprietário                       | Sim         |
| DELETE | `/owner/<id>`        | Remover um proprietário                         | Sim         |
| GET    | `/car`               | Listar todos os carros                          | Sim         |
| POST   | `/car`               | Adicionar um novo carro                         | Sim         |
| GET    | `/car/<id>`          | Listar um carro específico                      | Sim         |
| PATCH  | `/car/<id>`          | Atualizar as informações do carro                | Sim         |
| DELETE | `/car/<id>`          | Apagar um carro                                  | Sim         |

## Como Rodar o Projeto

1. **Pré-requisitos:**
   * Docker e Docker Compose instalados.
2. **Clonar o Repositório:**
   ```bash
   git clone https://docs.github.com/pt/repositories
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

