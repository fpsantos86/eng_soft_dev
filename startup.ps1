# Parar e remover todos os containers, redes e volumes
docker-compose down -v

# Recriar os containers em segundo plano
docker-compose up -d --build

# Aguardar alguns segundos para garantir que todos os serviços estejam totalmente iniciados
Start-Sleep -Seconds 30

# Executar o script de configuração das rotas do Kong
./ps_scripts/config_kong_routes.ps1

# Executar o script para criar o usuário no Konga
./ps_scripts/create_konga_user.ps1