# Definição de variáveis
$KONGA_URL = "http://localhost:31337"  # URL do Konga
$USERNAME = "admin"  # Nome de usuário
$PASSWORD = "admin123"  # Senha

# Realizando login no Konga
Write-Host "Autenticando no Konga..."
$loginPayload = @{ identifier = $USERNAME; password = $PASSWORD } | ConvertTo-Json -Depth 10

$headers = @{ "Content-Type" = "application/json" }
$response = Invoke-RestMethod -Uri "$KONGA_URL/login" -Method Post -Body $loginPayload -Headers $headers

if ($response -and $response.token) {
    $token = $response.token
    Write-Host "Autenticação bem-sucedida. Token: $token"

    # Configurando cabeçalhos com o token de autenticação
    $authHeaders = @{ 
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $token"
    }

    # Verificando conexões existentes
    Write-Host "Verificando conexões existentes no Konga..."
    $existingConnections = Invoke-RestMethod -Uri "$KONGA_URL/api/kongnode" -Method Get -Headers $authHeaders

    $connection = $existingConnections | Where-Object { $_.kong_admin_url -eq "http://kong:8001" }

    if ($connection) {
        Write-Host "Conexão já existe. ID: $($connection.id)"
    } else {
        Write-Host "Criando nova conexão no Konga..."
        $connectionPayload = @{ 
            type = "default"
            name = "kong"
            kong_admin_url = "http://kong:8001"
            kong_api_key = ""
            username = ""
            password = ""
        } | ConvertTo-Json -Depth 10

        $newConnection = Invoke-RestMethod -Uri "$KONGA_URL/api/kongnode" -Method Post -Body $connectionPayload -Headers $authHeaders
        Write-Host "Nova conexão criada. ID: $($newConnection.id)"
    }

    # Testando conexão com o Kong
    $connectionId = $connection?.id -or $newConnection?.id
    if ($connectionId) {
        Write-Host "Testando conexão com o Kong. ID da conexão: $connectionId"
        $testResponse = Invoke-RestMethod -Uri "$KONGA_URL/kong?connection_id=$connectionId" -Method Get -Headers $authHeaders -ErrorAction Stop

        if ($testResponse) {
            Write-Host "Conexão com o Kong testada com sucesso. Status: $($testResponse.status)"
        } else {
            Write-Host "Falha ao testar a conexão com o Kong."
        }
    } else {
        Write-Host "Nenhuma conexão disponível para testar."
    }
} else {
    Write-Host "Falha na autenticação no Konga."
}
