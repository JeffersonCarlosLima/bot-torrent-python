import schedule
import time
import subprocess

def execute_script():
    # Aqui você pode adicionar o caminho para o script ou programa que deseja executar
    script_path = "C:\\Users\\jeffe\\AppData\\Local\\Programs\\TikTok Music\\TikTok Music Launcher.exe"
    try:
        subprocess.run([script_path], check=True)
        print("Script executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script: {e}")

# Agendar a execução do script a cada 4 horas
schedule.every(4).hours.do(execute_script)

# Loop infinito para manter o programa rodando
while True:
    schedule.run_pending()
    time.sleep(1)
#python -m venv projTor
#projTor\Scripts\activate
#deactivate  -- destaiva o venv
