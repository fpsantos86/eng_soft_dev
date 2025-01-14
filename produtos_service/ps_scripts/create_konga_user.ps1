# Variáveis
$KONGA_URL = "http://localhost:31337/register" # URL do endpoint do Konga
$payload = 'username=admin&email=admin@admin.com&password=admin123&password_confirmation=admin123'


# Cabeçalhos da Requisição
$headers = @{
    "Content-Type" = "application/x-www-form-urlencoded"
}

# Enviando a Requisição
try {
    $response = Invoke-WebRequest -Uri  "http://localhost:31337/register" -Method Post -Body 'username=admin&email=admin@admin.com&password=admin123&password_confirmation=admin123'


    # Obtendo apenas o status HTTP
    $statusCode = $response.StatusCode
    Write-Host "Conexão com o Kong retornou o status: $statusCode"
    Write-Host "Usuário criado com sucesso!"
} catch {
    Write-Host "Erro ao criar o usuário:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
