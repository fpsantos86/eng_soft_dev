# Variáveis
$KONGA_URL = "http://localhost:31337/register" # URL do endpoint do Konga
$payload = 'username=admin&email=admin@admin.com&password=admin123&password_confirmation=admin123'


# Cabeçalhos da Requisição
$headers = @{
    "Content-Type" = "application/x-www-form-urlencoded"
}

# Enviando a Requisição
try {
    $response = Invoke-RestMethod -Uri $KONGA_URL -Method Post -Body $payload -Headers $headers
    Write-Host "Usuário criado com sucesso:" -ForegroundColor Green
    Write-Host $response
} catch {
    Write-Host "Erro ao criar o usuário:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
