import schedule
import time
import subprocess

def execute_script():
    # Aqui você pode adicionar o caminho para o script ou programa que deseja executar
    script_path = "C:\\Users\\Marketing\\Documents\\Projetos\\executar programas\\bot.py"  # Por exemplo, um script bash
    try:
        subprocess.run(["/bin/bash", script_path], check=True)
        print("Script executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script: {e}")

# Agendar a execução do script a cada 4 horas
schedule.every(1).minutes.do(execute_script)

# Loop infinito para manter o programa rodando
while True:
    schedule.run_pending()
    time.sleep(1)
