import os

CDP_HOST = os.environ.get("WIDEPAY_CDP_HOST", "localhost")
CDP_PORT = int(os.environ.get("WIDEPAY_CDP_PORT", "9444"))
CDP_BASE_URL = f"http://{CDP_HOST}:{CDP_PORT}"
WIDEPAY_CARNES_URL = "https://www.widepay.com/conta/recebimentos/carnes"
BROWSER_PREFERENCIAL = os.environ.get("WIDEPAY_BROWSER", "opera_gx").lower()
ABERTURA_PREFERENCIAL = "wmi_win32_process"

# Fallback homologado quando o Opera dedicado estiver lento ou travado:
# WIDEPAY_BROWSER=chrome + WIDEPAY_CDP_PORT=9333
