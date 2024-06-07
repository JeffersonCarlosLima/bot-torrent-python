import schedule
import time
import subprocess
from datetime import datetime

def run_application():
    application_path = "/home/server/Documentos/gerador de torrents/bot.py"  # Altere para o caminho correto
    subprocess.run([application_path])
    print(f"Aplicação executada em: {datetime.now()}")

def schedule_task(hour, minute):
    schedule_time = f"{hour:02d}:{minute:02d}"
    try:
        schedule.every().day.at(schedule_time).do(run_application)
        print(f"Aplicação agendada para {schedule_time} todos os dias.")
    except schedule.ScheduleValueError as e:
        print(f"Erro ao agendar: {e}")

def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    # Defina a hora e o minuto desejados aqui
    hour = 23
    minute = 32

    # Agende a tarefa
    schedule_task(hour, minute)
    
    print("Pressione Ctrl+C para sair.")
    
    # Inicia o agendador em um loop infinito
    start_scheduler()

if __name__ == "__main__":
    main()
