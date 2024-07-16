import schedule
import time
import subprocess

def execute_script(script_path):
    try:
        subprocess.run([script_path], check=True)
        print("Script executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script: {e}")

def schedule_task(script_path, interval):
    schedule.clear()  # Limpa qualquer agendamento anterior
    schedule.every(interval).minutes.do(execute_script, script_path=script_path)
    print(f"Script agendado para ser executado a cada {interval} minutos.")

# Caminho do script ou programa que você deseja executar
script_path = "C:\\Users\\jeffe\\AppData\\Local\\Programs\\TikTok Music\\TikTok Music Launcher.exe"

# Defina o intervalo de tempo em minutos
interval = 1# Por exemplo, 60 minutos

# Agendar a tarefa
schedule_task(script_path, interval)

# Loop infinito para manter o programa rodando
while True:
    schedule.run_pending()
    time.sleep(1)

