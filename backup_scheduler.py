"""
Gerenciador de Agendamento Automático de Backups
"""

import subprocess
import os
from pathlib import Path

class BackupScheduler:
    def __init__(self):
        self.config_file = Path("backup_schedule.conf")
        self.cron_comment = "# Backup Disparador Email"
    
    def get_current_schedule(self):
        """Obtém o agendamento atual do crontab"""
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.split("\n")
                for i, line in enumerate(lines):
                    if self.cron_comment in line and i + 1 < len(lines):
                        return lines[i + 1]
            return None
        except Exception:
            return None
    
    def set_schedule(self, cron_expression, script_path):
        """Define um novo agendamento no crontab"""
        try:
            # Obter crontab atual
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )
            
            current_crontab = result.stdout if result.returncode == 0 else ""
            
            # Remover linhas antigas do backup
            lines = current_crontab.split("\n")
            new_lines = []
            skip_next = False
            
            for i, line in enumerate(lines):
                if self.cron_comment in line:
                    skip_next = True
                    continue
                if skip_next:
                    skip_next = False
                    continue
                if line.strip():
                    new_lines.append(line)
            
            # Adicionar nova linha
            new_lines.append(self.cron_comment)
            new_lines.append(f"{cron_expression} {script_path}")
            new_lines.append("")  # Linha vazia no final
            
            # Aplicar novo crontab
            new_crontab = "\n".join(new_lines)
            
            process = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                # Salvar configuração no arquivo
                self.config_file.write_text(f"{cron_expression}\n{script_path}")
                return True, "Agendamento configurado com sucesso!"
            else:
                return False, f"Erro: {stderr}"
                
        except Exception as e:
            return False, str(e)
    
    def remove_schedule(self):
        """Remove o agendamento do crontab"""
        try:
            # Obter crontab atual
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return True, "Nenhum crontab configurado"
            
            current_crontab = result.stdout
            
            # Remover linhas do backup
            lines = current_crontab.split("\n")
            new_lines = []
            skip_next = False
            
            for line in lines:
                if self.cron_comment in line:
                    skip_next = True
                    continue
                if skip_next:
                    skip_next = False
                    continue
                if line.strip():
                    new_lines.append(line)
            
            # Aplicar novo crontab
            new_crontab = "\n".join(new_lines) + "\n"
            
            process = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                if self.config_file.exists():
                    self.config_file.unlink()
                return True, "Agendamento removido com sucesso!"
            else:
                return False, f"Erro: {stderr}"
                
        except Exception as e:
            return False, str(e)
    
    def get_schedule_description(self, cron_expression):
        """Converte expressão cron em descrição legível"""
        parts = cron_expression.split()
        
        if len(parts) != 5:
            return "Expressão inválida"
        
        minute, hour, day, month, weekday = parts
        
        descriptions = []
        
        # Minuto
        if minute == "*":
            descriptions.append("todo minuto")
        elif "/" in minute:
            interval = minute.split("/")[1]
            descriptions.append(f"a cada {interval} minutos")
        else:
            descriptions.append(f"no minuto {minute}")
        
        # Hora
        if hour == "*":
            descriptions.append("todas as horas")
        elif "/" in hour:
            interval = hour.split("/")[1]
            descriptions.append(f"a cada {interval} horas")
        else:
            descriptions.append(f"às {hour}h")
        
        # Dia
        if day != "*":
            descriptions.append(f"dia {day}")
        
        # Mês
        if month != "*":
            meses = {
                "1": "Janeiro", "2": "Fevereiro", "3": "Março",
                "4": "Abril", "5": "Maio", "6": "Junho",
                "7": "Julho", "8": "Agosto", "9": "Setembro",
                "10": "Outubro", "11": "Novembro", "12": "Dezembro"
            }
            descriptions.append(f"em {meses.get(month, month)}")
        
        # Dia da semana
        if weekday != "*":
            dias = {
                "0": "Domingo", "1": "Segunda", "2": "Terça",
                "3": "Quarta", "4": "Quinta", "5": "Sexta", "6": "Sábado"
            }
            descriptions.append(f"nas {dias.get(weekday, weekday)}-feiras")
        
        return " ".join(descriptions)

scheduler = BackupScheduler()
