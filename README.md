# 🥤 Alerta de Copo de Água & Postura Inteligente

Script Python que monitoriza a tua atividade no computador e envia **notificações nativas** com piadas de programador quando estás a trabalhar sem pausa há demasiado tempo.

## Como Funciona

1. **Monitoriza** teclado e rato em background (event-driven, zero polling)
2. **Deteta** sessões longas (50 min de atividade contínua por defeito)
3. **Notifica** com uma piada/desafio de programador em português
4. **Reset automático** quando ficas inativo 5+ minutos (foste beber água!)

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
    "notification_title": "🥤 Alerta de Hidratação & Postura",
    "enabled": true
}
```

| Parâmetro | Default | Descrição |
|---|---|---|
| `activity_threshold_minutes` | 50 | Minutos de atividade antes do alerta |
| `idle_reset_minutes` | 5 | Minutos de inatividade para reset |
| `notification_title` | 🥤 Alerta... | Título da notificação |
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

## Licença

MIT
