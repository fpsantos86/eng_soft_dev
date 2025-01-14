# Nome do contêiner do Kong
$kongContainer = "estudo_cqrs-kong-1"

# URL a ser testada no app_flask
$testUrl = "http://app_flask:5000/produtos"

# Comando para testar a conexão
$command = "curl $testUrl"

# Executa o comando dentro do contêiner Kong
$output = docker exec -it $kongContainer bash -c $command
Write-Host $output
# Verifica se a resposta contém os dados esperados
if ($output -like "*200 OK*") {
    Write-Host "Conexão com o app_flask bem-sucedida!" -ForegroundColor Green
} else {
    Write-Host "Falha na conexão com o app_flask. Verifique as configurações!" -ForegroundColor Red
}
