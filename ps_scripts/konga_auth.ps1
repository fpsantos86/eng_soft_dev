# Configurações
$KONGA_LOGIN_URL = "http://localhost:31337/login"  # URL do Konga Login
$KONGA_URL = "http://localhost:31337/"  # URL do Konga Login
$KONGA_PAYLOAD = @{
    identifier = "admin"  # Usuário
    password = "admin123" # Senha
} | ConvertTo-Json -Depth 10

$HEADERS = @{
    "Accept" = "application/json,text/plain,*/*"
    "Content-Type" = "application/json"
}

# Realizar Login no Konga
try {
    Write-Host "Autenticando no Konga..."
    $response = Invoke-RestMethod -Uri $KONGA_LOGIN_URL `
                                  -Method Post `
                                  -Body $KONGA_PAYLOAD `
                                  -Headers $HEADERS

    $authToken = $response.token
    Write-Host "Autenticação bem-sucedida! Token: $authToken"
} catch {
    Write-Host "Falha ao autenticar no Konga. Verifique as credenciais."
    Write-Host $_
    exit
}

# Conectar no Kong usando o token do Konga
$HEADERS_AUTH = @{
    "Authorization" = "Bearer $authToken"
}

try {
    Write-Host "Testando conexão com o Kong..."
    $kongResponse = Invoke-WebRequest  -Uri "$KONGA_URL/#!/dashboard" `
                                      -Method Get `
                                      -Headers $HEADERS_AUTH

    $statusCode = $kongResponse.StatusCode
    Write-Host "Conexão com o Kong retornou o status: $statusCode"
    
} catch {
    Write-Host "Falha ao conectar ao Kong."
    Write-Host $_
}
