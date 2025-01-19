# Sistema de Gestão de Produtos e Front-End

Este repositório contém uma solução completa de backend e frontend para um sistema de gestão de produtos. O projeto utiliza Docker e Docker Compose para facilitar a configuração e execução do ambiente.

---

## **Pré-requisitos**

Antes de começar, você precisará ter instalado em sua máquina:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---
### Teste na usa máquina:

 - Crie uma diretório chamado "app_produtos"
   - Dentro dele crie um arquivo docker-compose.yml
 - Cole o código abaixo:
```yml
services:
  app:
    image: fpsantos86/backend_produtos:latest
    container_name: app_flask
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: produtos_db
      MONGO_HOST: mongodb
      MONGO_PORT: 27017
      MONGO_USER: admin
      MONGO_PASSWORD: admin123
      MONGO_DB_NAME: produtos_db
      MONGO_COLLECTION_NAME: produtos
      RABBITMQ_HOST: rabbitmq
      RABBITMQ_PORT: 5672
      RABBITMQ_USER: guest
      RABBITMQ_PASSWORD: guest
      IS_DOCKER: "true"
    ports:
      - "7000:5000"
    depends_on:
      - postgres
      - mongodb
      - rabbitmq
    networks:
      - eng-soft-dev

  front-end:
    image: fpsantos86/front-end_produtos:latest
    container_name: front_end
    depends_on:
      - app
    ports:
      - "3001:3000"
    networks:
      - eng-soft-dev


```

Em seguida, abra o terminal e digite :
```bash
~$ docker-compose up -d
```

---
## Contato
Para dúvidas ou sugestões, entre em contato:

 - Autor: Felipe Pereira
 - Email: fpsantos86@hotmail.com
 - GitHub: https://github.com/fpsantos86


