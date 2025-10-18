"""
Painel de configuração de jobs automáticos para o Streamlit
"""

import streamlit as st
import database as db
from datetime import datetime
import subprocess
from pathlib import Path


def mostrar_painel_jobs():
    """Mostra painel de configuração e monitoramento de jobs"""
    
    st.title("⚙️ Jobs Automáticos")
    
    # Verificar status do serviço
    pid_file = Path('scheduler.pid')
    servico_rodando = False
    pid = None
    
    if pid_file.exists():
        try:
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Verificar se processo existe
            import os
            try:
                os.kill(pid, 0)
                servico_rodando = True
            except OSError:
                servico_rodando = False
                pid_file.unlink()
        except:
            servico_rodando = False
    
    # Status do serviço
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if servico_rodando:
            st.success(f"✅ Serviço Rodando (PID: {pid})")
        else:
            st.error("❌ Serviço Parado")
    
    with col2:
        if servico_rodando:
            if st.button("🛑 Parar Serviço", use_container_width=True):
                try:
                    subprocess.run(['venv/bin/python', 'run_scheduler.py', 'stop'])
                    st.success("✅ Serviço parado!")
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
        else:
            if st.button("▶️ Iniciar Serviço", use_container_width=True):
                try:
                    # Configurar variáveis de ambiente antes de iniciar
                    import os
                    env = os.environ.copy()
                    env['DYLD_LIBRARY_PATH'] = '/opt/homebrew/lib:' + env.get('DYLD_LIBRARY_PATH', '')
                    env['PKG_CONFIG_PATH'] = '/opt/homebrew/lib/pkgconfig:' + env.get('PKG_CONFIG_PATH', '')
                    
                    # Usar o wrapper que configura as variáveis corretas
                    subprocess.Popen(
                        ['venv/bin/python', 'run_scheduler.py'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True,
                        env=env,
                        cwd=Path(__file__).parent
                    )
                    st.success("✅ Serviço iniciado! Aguarde alguns segundos...")
                    import time
                    time.sleep(2)  # Dar tempo para o serviço iniciar
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao iniciar: {e}")
                    import traceback
                    st.code(traceback.format_exc())
    
    with col3:
        if servico_rodando:
            if st.button("🔄 Recarregar", use_container_width=True, help="Recarrega configurações sem parar"):
                try:
                    subprocess.run(['venv/bin/python', 'run_scheduler.py', 'reload'])
                    st.success("✅ Configurações recarregadas!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
    
    st.markdown("---")
    
    # Buscar jobs configurados
    jobs = db.get_jobs_config()
    
    if not jobs:
        st.warning("Nenhum job configurado")
        return
    
    # Mostrar cada job
    for job in jobs:
        with st.expander(
            f"{'✅' if job['ativo'] else '⏸️'} {job['nome'].upper()} - {job['descricao']}",
            expanded=job['ativo']
        ):
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown("### 📊 Informações")
                st.write(f"**Status:** {'✅ Ativo' if job['ativo'] else '⏸️ Inativo'}")
                st.write(f"**Intervalo:** {job['intervalo_minutos']} minutos")
                st.write(f"**Total Execuções:** {job['total_execucoes']}")
                st.write(f"**Total Erros:** {job['total_erros']}")
                
                if job['total_execucoes'] > 0:
                    taxa_sucesso = ((job['total_execucoes'] - job['total_erros']) / job['total_execucoes']) * 100
                    st.metric("Taxa de Sucesso", f"{taxa_sucesso:.1f}%")
            
            with col_info2:
                st.markdown("### ⏰ Execuções")
                
                if job['ultima_execucao']:
                    tempo_desde = datetime.now() - job['ultima_execucao']
                    horas = int(tempo_desde.total_seconds() / 3600)
                    minutos = int((tempo_desde.total_seconds() % 3600) / 60)
                    st.write(f"**Última Execução:** {job['ultima_execucao'].strftime('%d/%m/%Y %H:%M')}")
                    st.caption(f"Há {horas}h {minutos}min")
                else:
                    st.write("**Última Execução:** Nunca executado")
                
                if job['proxima_execucao'] and job['ativo']:
                    tempo_ate = job['proxima_execucao'] - datetime.now()
                    if tempo_ate.total_seconds() > 0:
                        minutos_ate = int(tempo_ate.total_seconds() / 60)
                        st.write(f"**Próxima Execução:** {job['proxima_execucao'].strftime('%d/%m/%Y %H:%M')}")
                        st.caption(f"Em {minutos_ate} minutos")
                    else:
                        st.write("**Próxima Execução:** Em breve...")
                else:
                    st.write("**Próxima Execução:** -")
            
            # Última mensagem
            if job['ultima_mensagem']:
                st.info(f"💬 {job['ultima_mensagem']}")
            
            st.markdown("---")
            
            # Configurações
            col_config1, col_config2, col_config3 = st.columns([2, 2, 1])
            
            with col_config1:
                novo_status = st.toggle(
                    "Ativo",
                    value=job['ativo'],
                    key=f"ativo_{job['id']}"
                )
            
            with col_config2:
                novo_intervalo = st.number_input(
                    "Intervalo (minutos)",
                    min_value=1,
                    max_value=1440,
                    value=job['intervalo_minutos'],
                    step=5,
                    key=f"intervalo_{job['id']}"
                )
            
            with col_config3:
                st.write("")  # Spacer
                st.write("")  # Spacer
                if st.button("💾 Salvar", key=f"salvar_{job['id']}", use_container_width=True):
                    # Verificar se houve mudanças
                    if novo_status != job['ativo'] or novo_intervalo != job['intervalo_minutos']:
                        db.atualizar_job_config(
                            job['nome'],
                            ativo=novo_status,
                            intervalo_minutos=novo_intervalo
                        )
                        st.success("✅ Configurações salvas!")
                        
                        # Se serviço está rodando, recarregar
                        if servico_rodando:
                            try:
                                subprocess.run(['.venv/bin/python', 'scheduler_service.py', 'reload'])
                                st.info("🔄 Configurações recarregadas no serviço")
                            except:
                                st.warning("⚠️ Reinicie o serviço para aplicar as mudanças")
                        else:
                            st.warning("⚠️ Inicie o serviço para aplicar as mudanças")
                        
                        st.rerun()
                    else:
                        st.info("Nenhuma alteração detectada")
    
    # Logs
    st.markdown("---")
    st.markdown("### 📋 Logs Recentes")
    
    log_file = Path('scheduler.log')
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                # Últimas 50 linhas
                recent_lines = lines[-50:]
                log_text = ''.join(recent_lines)
            
            st.text_area(
                "Logs do Scheduler",
                value=log_text,
                height=300,
                disabled=True
            )
            
            if st.button("🔄 Atualizar Logs"):
                st.rerun()
        
        except Exception as e:
            st.error(f"Erro ao ler logs: {e}")
    else:
        st.info("Nenhum log disponível ainda")
    
    # Instruções
    with st.expander("📖 Como Usar"):
        st.markdown("""
        ### Como Funcionam os Jobs Automáticos
        
        1. **Iniciar o Serviço:** Clique em "▶️ Iniciar Serviço"
        2. **Configurar Jobs:** Ative/desative jobs e ajuste o intervalo
        3. **Salvar:** Clique em "💾 Salvar" para aplicar
        4. **Monitorar:** Acompanhe execuções e logs
        
        ### Jobs Disponíveis
        
        - **consultar_notas**: Consulta e baixa arquivos de notas fiscais
        - **enviar_api**: Envia lotes pendentes para a API
        
        ### Dicas
        
        - Intervalos menores = mais frequente, mas mais processamento
        - Recomendado: 60 minutos para consultar_notas
        - O serviço roda em background, não precisa manter o Streamlit aberto
        - Use "🔄 Recarregar" para aplicar mudanças sem parar o serviço
        
        ### Comandos Via Terminal
        
        ```bash
        # Ver status
        python scheduler_service.py status
        
        # Parar
        python scheduler_service.py stop
        
        # Recarregar
        python scheduler_service.py reload
        
        # Ver logs em tempo real
        tail -f scheduler.log
        ```
        """)


# Para testar standalone
if __name__ == "__main__":
    st.set_page_config(page_title="Jobs Automáticos", page_icon="⚙️", layout="wide")
    mostrar_painel_jobs()
