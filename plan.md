# Plan — Alerta Copo de Água & Postura Inteligente

## Progresso

### Fase 1 — Fundação
- [x] **1.1** Criar estrutura de pastas e ficheiros base
- [x] **1.2** Configurar `pyproject.toml`, `requirements.txt`, `.gitignore`
- [x] **1.3** Implementar `config/settings.py` com defaults (50min/5min)
- [x] **1.4** Criar `config.json` editável pelo utilizador
- [x] **1.5** Git init + commit inicial

### Fase 2 — Monitorização de Atividade
- [x] **2.1** `activity_tracker.py` — listeners teclado + rato via pynput
- [x] **2.2** `idle_detector.py` — reset após 5min sem eventos
- [x] **2.3** Testes unitários (mock de eventos) — 17 testes
- [x] **2.4** Git commit

### Fase 3 — Notificações
- [x] **3.1** `data/messages.json` — 15 piadas/desafios em PT
- [x] **3.2** `messages.py` — seleção aleatória sem repetição
- [x] **3.3** `notifier.py` — envio via plyer (nativo Win/Mac/Linux)
- [x] **3.4** Testes unitários — 9 testes
- [x] **3.5** Git commit

### Fase 4 — Integração
- [x] **4.1** `main.py` — loop principal com timer 50min
- [x] **4.2** Lógica completa: atividade → notifica; idle 5min → reset
- [x] **4.3** Graceful shutdown (Ctrl+C) + cleanup listeners
- [x] **4.4** Teste integração end-to-end — 5 testes
- [x] **4.5** Git commit

### Fase 5 — Entrega
- [x] **5.1** README.md completo
- [x] **5.2** Validação no OS atual (Windows, 31 testes passam)
- [x] **5.3** Git commit final + tag v1.0.0

### Fase 6 — Correções & Melhorias (v1.1)
- [x] **6.1** Throttle mouse move events (1 evento/segundo máx) — fix CPU spike
- [x] **6.2** Mover notificação para fora do lock — fix potencial deadlock
- [x] **6.3** Remover `on_release` do keyboard (duplicação desnecessária)
- [x] **6.4** Logging com `logging` module (substituir prints)
- [x] **6.5** Validação de config (clamp valores a ranges seguros)
- [x] **6.6** Estatísticas básicas (notificações enviadas, uptime)
- [x] **6.7** Testes atualizados — 39 testes passam
- [x] **6.8** Git commit + push

### Fase 7 — System Tray + Lembretes Progressivos (v2.0)
- [x] **7.1** Adicionar pystray + Pillow às dependências
- [x] **7.2** Implementar `src/tray.py` — ícone com pause/resume/quit
- [x] **7.3** Integrar tray com main.py (start/stop lifecycle)
- [x] **7.4** Lembretes progressivos — repetir a cada N min se ignorado
- [x] **7.5** Config: `repeat_interval_minutes`, `show_tray_icon`
- [x] **7.6** Testes para pause/resume/progressive — 42 testes passam
- [x] **7.7** Git commit + push + tag v2.0.0
