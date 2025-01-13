# Configurando variáveis globais
$KONG_ADMIN_URL = "http://localhost:9011"  # URL do Kong Admin API
$SERVICE_NAME = "produtos-api"

# Verificar se o serviço já existe e removê-lo
Write-Host "Verificando se o serviço '$SERVICE_NAME' já existe..."
try {
    $existingService = Invoke-RestMethod -Uri "$KONG_ADMIN_URL/services/$SERVICE_NAME" -Method Get
    $SERVICE_ID = $existingService.id
    Write-Host "Serviço já existe com ID: $SERVICE_ID. Removendo..."
    Invoke-RestMethod -Uri "$KONG_ADMIN_URL/services/$SERVICE_ID" -Method Delete
    Write-Host "Serviço removido."
} catch {
    Write-Host "Serviço não encontrado. Prosseguindo com a criação do serviço: $SERVICE_NAME..."
}

# Criar o serviço
Write-Host "Criando o serviço: $SERVICE_NAME..."
$serviceData = @{ 
    name = $SERVICE_NAME
    url  = "http://app_flask:5000"  # Certifique-se de que o URL está correto e acessível pelo Kong
} | ConvertTo-Json -Depth 10

$serviceResponse = Invoke-RestMethod -Uri "$KONG_ADMIN_URL/services" `
                                     -Method Post `
                                     -Body $serviceData `
                                     -ContentType "application/json"

$SERVICE_ID = $serviceResponse.id
Write-Host "Serviço criado com ID: $SERVICE_ID"

# Criando as rotas
$routes = @(
    @{ methods = @("GET");    paths = @("/{id_produto}") },
    @{ methods = @("GET");    paths = @("/{id_produto}/") },
    @{ methods = @("PUT");    paths = @("/{id_produto}") },
    @{ methods = @("PUT");    paths = @("/{id_produto}/") },
    @{ methods = @("DELETE"); paths = @("/{id_produto}") },
    @{ methods = @("DELETE"); paths = @("/{id_produto}/") },
    @{ methods = @("POST");   paths = @("/")},
    @{ methods = @("GET");    paths = @("/")}
)

foreach ($route in $routes) {
    Write-Host "Verificando se a rota já existe para: $($route.methods[0]) $($route.paths[0])"
    try {
        $existingRoute = Invoke-RestMethod -Uri "$KONG_ADMIN_URL/routes" -Method Get
        $routeExists = $existingRoute.data | Where-Object { $_.paths -contains $route.paths[0] -and $_.methods -contains $route.methods[0] }
        if ($routeExists) {
            Write-Host "Rota já existe: $($route.methods[0]) $($route.paths[0]). Removendo..."
            Invoke-RestMethod -Uri "$KONG_ADMIN_URL/routes/$($routeExists.id)" -Method Delete
            Write-Host "Rota removida."
        }
    } catch {
        Write-Host "Erro ao verificar a rota: $_"
    }

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

# Configuração do plugin CORS em formato JSON
$bodyCors = @{
    name = "cors"
    config = @{
        origins = @("*")
        methods = @("GET", "POST", "PUT", "DELETE", "OPTIONS")
        headers = @("Accept", "Authorization", "Content-Type")
        credentials = $false
    }
} | ConvertTo-Json -Depth 10

# Enviar a requisição com o corpo JSON
Invoke-RestMethod -Method Post -Uri "$KONG_ADMIN_URL/services/$SERVICE_ID/plugins" -Body $bodyCors -ContentType "application/json"

# Configuração do plugin request-transformer para permitir requisições JSON
$bodyTransformer = @{
    name = "request-transformer"
    config = @{
        add = @{
            headers = @("Content-Type:application/json")
        }
    }
} | ConvertTo-Json -Depth 10

# Enviar a requisição com o corpo JSON
Invoke-RestMethod -Method Post -Uri "$KONG_ADMIN_URL/services/$SERVICE_ID/plugins" -Body $bodyTransformer -ContentType "application/json"

Write-Host "Configuração concluída. Verifique as rotas no Kong."
