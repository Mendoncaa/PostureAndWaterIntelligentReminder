# 🥤 Alerta de Copo de Água & Postura Inteligente

Script Python que monitoriza a tua atividade no computador e envia **notificações nativas** com piadas de programador quando estás a trabalhar sem pausa há demasiado tempo.

## Como Funciona

1. **Monitoriza** teclado e rato em background (event-driven, zero polling)
2. **Deteta** sessões longas (50 min de atividade contínua por defeito)
3. **Notifica** com uma piada/desafio de programador em português
4. **Repete** lembretes a cada 10 min se ignorares (progressivo)
5. **Reset automático** quando ficas inativo 5+ minutos (foste beber água!)
6. **System tray** — ícone com pause/resume/quit (minimizado)

## Instalação

```bash
# Clonar o repositório
git clone <url-do-repo>
cd IntelligentReminder

# Instalar dependências
pip install -r requirements.txt
```

## Utilização

```bash
python -m src.main
```

Output esperado:
```
✅ IntelligentReminder ativo!
   ⏱️  Alerta após 50 min de atividade contínua
   😴 Reset após 5 min de inatividade
   📝 15 mensagens carregadas
   Ctrl+C para sair
```

## Configuração

Edita `config.json` na raiz do projeto:

```json
{
    "activity_threshold_minutes": 50,
    "idle_reset_minutes": 5,
    "repeat_interval_minutes": 10,
    "notification_title": "🥤 Alerta de Hidratação & Postura",
    "show_tray_icon": true,
    "enabled": true
}
```

| Parâmetro | Default | Descrição |
|---|---|---|
| `activity_threshold_minutes` | 50 | Minutos de atividade antes do alerta |
| `idle_reset_minutes` | 5 | Minutos de inatividade para reset |
| `repeat_interval_minutes` | 10 | Repete lembrete a cada N min se ignorado |
| `notification_title` | 🥤 Alerta... | Título da notificação |
| `show_tray_icon` | true | Mostra ícone no system tray |
| `enabled` | true | Ativar/desativar |

## Testes

```bash
python -m pytest tests/ -v
```

## Tech Stack

- **Python 3.10+**
- **pynput** — Monitorização cross-platform de teclado/rato
- **plyer** — Notificações nativas do OS
- **pytest** — Testes

## Estrutura

```
src/
├── main.py                 # Entry point + orquestração
├── monitor/
│   ├── activity_tracker.py # Listeners teclado/rato
│   └── idle_detector.py    # Deteção de inatividade
├── notifications/
│   ├── notifier.py         # Notificações nativas
│   └── messages.py         # Loader de piadas
└── config/
    └── settings.py         # Gestão de configuração
```

## Privacidade

Este programa usa um keyboard hook global (via `pynput`), mas **NÃO captura nem armazena o conteúdo das teclas**.
Apenas regista o *timestamp* do último evento para calcular duração de atividade.
Nenhum dado sai da máquina — sem telemetria, sem rede, sem logs de input.

## Licença

MIT
