const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const fs = require('fs');
const path = require('path');

// Configuração do Express para API REST
const app = express();
app.use(express.json());

// Cliente WhatsApp
let client = null;
let isReady = false;
let qrCodeData = null;

// Inicializar cliente WhatsApp
function initializeWhatsApp() {
    client = new Client({
        authStrategy: new LocalAuth({
            dataPath: './whatsapp_session'
        }),
        puppeteer: {
            headless: true,
            args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        }
    });

    // Evento: QR Code gerado
    client.on('qr', (qr) => {
        console.log('\n🔐 QR Code gerado! Escaneie com seu WhatsApp:\n');
        qrcode.generate(qr, { small: true });
        qrCodeData = qr;
        console.log('\n📱 Ou acesse: http://localhost:3000/qr para ver o QR Code\n');
    });

    // Evento: Cliente pronto
    client.on('ready', () => {
        console.log('✅ WhatsApp conectado com sucesso!');
        isReady = true;
        qrCodeData = null;
    });

    // Evento: Autenticação
    client.on('authenticated', () => {
        console.log('🔑 WhatsApp autenticado!');
    });

    // Evento: Falha de autenticação
    client.on('auth_failure', (msg) => {
        console.error('❌ Falha na autenticação:', msg);
        isReady = false;
    });

    // Evento: Desconectado
    client.on('disconnected', (reason) => {
        console.log('⚠️  WhatsApp desconectado:', reason);
        isReady = false;
        qrCodeData = null;
    });

    // Evento: Mensagem recebida (para responder automaticamente se necessário)
    client.on('message', async (message) => {
        console.log(`📨 Mensagem recebida de ${message.from}: ${message.body}`);
    });

    // Inicializar
    client.initialize();
}

// ========== API REST ENDPOINTS ==========

// Status do serviço
app.get('/status', (req, res) => {
    res.json({
        status: isReady ? 'connected' : 'disconnected',
        hasQrCode: qrCodeData !== null,
        message: isReady ? 'WhatsApp conectado e pronto' : 'WhatsApp desconectado ou aguardando autenticação'
    });
});

// Obter QR Code
app.get('/qr', (req, res) => {
    if (qrCodeData) {
        res.send(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>QR Code WhatsApp</title>
                <style>
                    body {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        margin: 0;
                        font-family: Arial, sans-serif;
                        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 20px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                    }
                    h1 {
                        color: #128C7E;
                        margin-bottom: 20px;
                    }
                    #qrcode {
                        margin: 20px 0;
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                    }
                    .instructions {
                        color: #666;
                        margin-top: 20px;
                        line-height: 1.6;
                    }
                </style>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
            </head>
            <body>
                <div class="container">
                    <h1>📱 Conectar WhatsApp</h1>
                    <div id="qrcode"></div>
                    <div class="instructions">
                        <p><strong>Como conectar:</strong></p>
                        <p>1. Abra o WhatsApp no seu celular</p>
                        <p>2. Toque em Menu ou Configurações</p>
                        <p>3. Toque em Aparelhos conectados</p>
                        <p>4. Toque em Conectar um aparelho</p>
                        <p>5. Aponte seu celular para esta tela</p>
                    </div>
                </div>
                <script>
                    new QRCode(document.getElementById("qrcode"), {
                        text: "${qrCodeData}",
                        width: 256,
                        height: 256
                    });
                    
                    // Recarregar a página a cada 5 segundos para verificar status
                    setTimeout(() => {
                        fetch('/status')
                            .then(r => r.json())
                            .then(data => {
                                if (data.status === 'connected') {
                                    document.body.innerHTML = '<div class="container"><h1>✅ Conectado com sucesso!</h1><p>Você pode fechar esta janela.</p></div>';
                                } else if (!data.hasQrCode) {
                                    location.reload();
                                }
                            });
                    }, 5000);
                </script>
            </body>
            </html>
        `);
    } else if (isReady) {
        res.send(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>WhatsApp Conectado</title>
                <style>
                    body {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        margin: 0;
                        font-family: Arial, sans-serif;
                        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 20px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        text-align: center;
                    }
                    h1 {
                        color: #128C7E;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>✅ WhatsApp já está conectado!</h1>
                    <p>O serviço está pronto para enviar mensagens.</p>
                </div>
            </body>
            </html>
        `);
    } else {
        res.status(503).json({
            error: 'QR Code ainda não foi gerado. Aguarde alguns segundos.'
        });
    }
});

// Enviar mensagem
app.post('/send', async (req, res) => {
    if (!isReady) {
        return res.status(503).json({
            success: false,
            error: 'WhatsApp não está conectado'
        });
    }

    const { number, message, media } = req.body;

    if (!number || !message) {
        return res.status(400).json({
            success: false,
            error: 'Número e mensagem são obrigatórios'
        });
    }

    try {
        // Formatar número (adicionar @c.us se necessário)
        let chatId = number.includes('@c.us') ? number : `${number}@c.us`;
        
        // Enviar mensagem
        if (media && media.path) {
            // Enviar com mídia
            const MessageMedia = require('whatsapp-web.js').MessageMedia;
            const mediaFile = MessageMedia.fromFilePath(media.path);
            await client.sendMessage(chatId, mediaFile, { caption: message });
        } else {
            // Enviar apenas texto
            await client.sendMessage(chatId, message);
        }

        console.log(`✅ Mensagem enviada para ${number}`);
        
        res.json({
            success: true,
            message: 'Mensagem enviada com sucesso',
            to: number
        });
    } catch (error) {
        console.error('❌ Erro ao enviar mensagem:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Enviar mensagem para múltiplos contatos
app.post('/send-bulk', async (req, res) => {
    if (!isReady) {
        return res.status(503).json({
            success: false,
            error: 'WhatsApp não está conectado'
        });
    }

    const { numbers, message, media, delay } = req.body;

    if (!numbers || !Array.isArray(numbers) || numbers.length === 0) {
        return res.status(400).json({
            success: false,
            error: 'Lista de números é obrigatória'
        });
    }

    if (!message) {
        return res.status(400).json({
            success: false,
            error: 'Mensagem é obrigatória'
        });
    }

    const results = [];
    const delayMs = delay || 2000; // Delay padrão de 2 segundos entre mensagens

    for (const number of numbers) {
        try {
            let chatId = number.includes('@c.us') ? number : `${number}@c.us`;
            
            if (media && media.path) {
                const MessageMedia = require('whatsapp-web.js').MessageMedia;
                const mediaFile = MessageMedia.fromFilePath(media.path);
                await client.sendMessage(chatId, mediaFile, { caption: message });
            } else {
                await client.sendMessage(chatId, message);
            }

            results.push({ number, success: true });
            console.log(`✅ Mensagem enviada para ${number}`);
            
            // Delay entre mensagens para evitar bloqueio
            await new Promise(resolve => setTimeout(resolve, delayMs));
        } catch (error) {
            results.push({ number, success: false, error: error.message });
            console.error(`❌ Erro ao enviar para ${number}:`, error.message);
        }
    }

    res.json({
        success: true,
        results,
        total: numbers.length,
        sent: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length
    });
});

// Desconectar
app.post('/disconnect', async (req, res) => {
    if (client) {
        await client.destroy();
        isReady = false;
        res.json({
            success: true,
            message: 'WhatsApp desconectado'
        });
    } else {
        res.status(400).json({
            success: false,
            error: 'WhatsApp já está desconectado'
        });
    }
});

// Informações do usuário conectado
app.get('/info', async (req, res) => {
    if (!isReady) {
        return res.status(503).json({
            success: false,
            error: 'WhatsApp não está conectado'
        });
    }

    try {
        const info = await client.info;
        res.json({
            success: true,
            info: {
                number: info.wid.user,
                name: info.pushname,
                platform: info.platform
            }
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// ========== INICIALIZAÇÃO ==========

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`
╔═══════════════════════════════════════════════════╗
║   🚀 Serviço WhatsApp Iniciado                   ║
║                                                   ║
║   📡 API REST rodando em: http://localhost:${PORT}  ║
║                                                   ║
║   📱 Endpoints disponíveis:                       ║
║   GET  /status      - Status da conexão          ║
║   GET  /qr          - Ver QR Code                ║
║   GET  /info        - Info do usuário            ║
║   POST /send        - Enviar mensagem            ║
║   POST /send-bulk   - Enviar para múltiplos      ║
║   POST /disconnect  - Desconectar                ║
╚═══════════════════════════════════════════════════╝
    `);
    
    console.log('\n⏳ Inicializando WhatsApp Web...\n');
    initializeWhatsApp();
});
