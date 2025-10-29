"""
Script para testar a integração WhatsApp
Execute este arquivo para verificar se tudo está funcionando
"""

from whatsapp_client import WhatsAppClient
import sys

def teste_basico():
    """Teste básico de conexão"""
    print("=" * 60)
    print("🧪 TESTE DE INTEGRAÇÃO WHATSAPP")
    print("=" * 60)
    print()
    
    # Criar cliente
    print("1️⃣ Criando cliente WhatsApp...")
    whatsapp = WhatsAppClient()
    print("   ✅ Cliente criado")
    print()
    
    # Verificar status
    print("2️⃣ Verificando status do serviço...")
    status = whatsapp.get_status()
    
    if status.get("status") == "error":
        print("   ❌ ERRO: Serviço não está rodando!")
        print()
        print("   💡 Para iniciar o serviço:")
        print("      1. Execute: npm start")
        print("      2. Ou: ./start_whatsapp.sh")
        print()
        return False
    
    print(f"   Status: {status.get('status')}")
    print(f"   Mensagem: {status.get('message')}")
    print()
    
    # Verificar conexão
    if not whatsapp.is_connected():
        print("3️⃣ WhatsApp NÃO está conectado")
        print()
        print("   📱 Para conectar:")
        print("      1. Acesse: http://localhost:3000/qr")
        print("      2. Escaneie o QR Code com seu WhatsApp")
        print("      3. Aguarde a conexão")
        print()
        
        # Perguntar se quer aguardar
        resposta = input("   ⏳ Deseja aguardar a conexão? (s/n): ").strip().lower()
        
        if resposta == 's':
            print()
            print("   ⏳ Aguardando conexão (timeout: 120 segundos)...")
            print("   📱 Escaneie o QR Code agora!")
            print()
            
            if whatsapp.wait_for_connection(timeout=120):
                print("   ✅ WhatsApp conectado com sucesso!")
            else:
                print("   ❌ Timeout: WhatsApp não foi conectado")
                return False
        else:
            print("   ⚠️  Teste cancelado. Conecte o WhatsApp e tente novamente.")
            return False
    else:
        print("3️⃣ ✅ WhatsApp está CONECTADO!")
    
    print()
    
    # Obter informações
    print("4️⃣ Obtendo informações do usuário...")
    info = whatsapp.get_info()
    
    if info.get("success"):
        user_info = info.get("info", {})
        print(f"   👤 Nome: {user_info.get('name')}")
        print(f"   📱 Número: {user_info.get('number')}")
        print(f"   📲 Plataforma: {user_info.get('platform')}")
    else:
        print(f"   ⚠️  Não foi possível obter informações: {info.get('error')}")
    
    print()
    
    # Perguntar se quer testar envio
    print("5️⃣ Teste de envio")
    resposta = input("   📤 Deseja testar o envio de mensagem? (s/n): ").strip().lower()
    
    if resposta == 's':
        numero = input("   📱 Digite o número (com DDD, ex: 11999999999): ").strip()
        
        if numero:
            mensagem = """
🧪 *Teste de Integração WhatsApp*

Esta é uma mensagem de teste do sistema Disparador Email.

Se você recebeu esta mensagem, significa que a integração está funcionando corretamente! ✅

_Mensagem automática - Não responda_
            """.strip()
            
            print()
            print("   📤 Enviando mensagem...")
            
            resultado = whatsapp.send_message(numero, mensagem)
            
            if resultado.get("success"):
                print("   ✅ Mensagem enviada com sucesso!")
            else:
                print(f"   ❌ Erro ao enviar: {resultado.get('error')}")
    
    print()
    print("=" * 60)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 60)
    print()
    print("📚 Próximos passos:")
    print("   • Veja exemplos em: integracao_whatsapp_exemplo.py")
    print("   • Documentação completa: WHATSAPP_INTEGRATION.md")
    print("   • Guia rápido: WHATSAPP_QUICKSTART.md")
    print()
    
    return True


if __name__ == "__main__":
    try:
        teste_basico()
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
