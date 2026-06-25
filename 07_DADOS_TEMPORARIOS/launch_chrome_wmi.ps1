$ChromeExe = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $ChromeExe)) {
    $ChromeExe = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
}
if (-not (Test-Path $ChromeExe)) {
    $ChromeExe = "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
}
$Perfil = "C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes\08_NAVEGADOR_WIDEPAY\ChromeProfile_9333"
$Url = "https://www.widepay.com/conta/recebimentos/carnes"
$Args = @(
  "--remote-debugging-port=9333",
  "--remote-allow-origins=*",
  "--user-data-dir=""$Perfil""",
  "--no-first-run",
  "--no-default-browser-check",
  "--new-window",
  """$Url"""
)
$CmdLine = """$ChromeExe"" " + ($Args -join ' ')
Write-Host "Comando: $CmdLine"
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $CmdLine }
