
# Configurando variáveis globais
$KONG_ADMIN_URL = "http://localhost:9011"  # URL do Kong Admin API
$SERVICE_NAME = "produtos-api"

# Verificar se o serviço já existe
Write-Host "Verificando se o serviço '$SERVICE_NAME' já existe..."
try {
    $existingService = Invoke-RestMethod -Uri "$KONG_ADMIN_URL/services/$SERVICE_NAME" -Method Get
    $SERVICE_ID = $existingService.id
    Write-Host "Serviço já existe com ID: $SERVICE_ID"
} catch {
    Write-Host "Serviço não encontrado. Criando o serviço: $SERVICE_NAME..."
    $serviceData = @{ 
        name = $SERVICE_NAME
        url  = "http://app_flask:5000"  # Substitua pelo URL do backend real
    } | ConvertTo-Json -Depth 10

    $serviceResponse = Invoke-RestMethod -Uri "$KONG_ADMIN_URL/services" `
                                         -Method Post `
                                         -Body $serviceData `
                                         -ContentType "application/json"

    $SERVICE_ID = $serviceResponse.id
    Write-Host "Serviço criado com ID: $SERVICE_ID"
}

# Criando as rotas
$routes = @(
    @{ methods = @("GET");    paths = @("/produtos/{id_produto}") },
    @{ methods = @("PUT");    paths = @("/produtos/{id_produto}") },
    @{ methods = @("DELETE"); paths = @("/produtos/{id_produto}") },
    @{ methods = @("POST");   paths = @("/produtos")           }
)

foreach ($route in $routes) {
    Write-Host "Criando rota para: $($route.methods[0]) $($route.paths[0])"
    $routeData = @{ 
        protocols = @("http", "https")
        methods   = $route.methods
        paths     = $route.paths
        service   = @{ id = $SERVICE_ID }
    } | ConvertTo-Json -Depth 10

    try {
        $response = Invoke-RestMethod -Uri "$KONG_ADMIN_URL/routes" `
                                      -Method Post `
                                      -Body $routeData `
                                      -ContentType "application/json"
        Write-Host "Rota criada: $($response.id)"
    } catch {
        Write-Host "Erro ao criar a rota: $_"
    }
}

Write-Host "Configuração concluída. Verifique as rotas no Kong."
