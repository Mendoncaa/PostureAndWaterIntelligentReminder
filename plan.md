# Plan — Alerta Copo de Água & Postura Inteligente

## Progresso

### Fase 1 — Fundação
- [x] **1.1** Criar estrutura de pastas e ficheiros base
- [x] **1.2** Configurar `pyproject.toml`, `requirements.txt`, `.gitignore`
- [x] **1.3** Implementar `config/settings.py` com defaults (50min/5min)
- [x] **1.4** Criar `config.json` editável pelo utilizador
- [x] **1.5** Git init + commit inicial

### Fase 2 — Monitorização de Atividade
- [ ] **2.1** `activity_tracker.py` — listeners teclado + rato via pynput
- [ ] **2.2** `idle_detector.py` — reset após 5min sem eventos
- [ ] **2.3** Testes unitários (mock de eventos)
- [ ] **2.4** Git commit

### Fase 3 — Notificações
- [ ] **3.1** `data/messages.json` — 10+ piadas/desafios em PT
- [ ] **3.2** `messages.py` — seleção aleatória sem repetição
- [ ] **3.3** `notifier.py` — envio via plyer (nativo Win/Mac/Linux)
- [ ] **3.4** Testes unitários
- [ ] **3.5** Git commit

### Fase 4 — Integração
- [ ] **4.1** `main.py` — loop principal com timer 50min
- [ ] **4.2** Lógica completa: atividade → notifica; idle 5min → reset
- [ ] **4.3** Graceful shutdown (Ctrl+C) + cleanup listeners
- [ ] **4.4** Teste integração end-to-end
- [ ] **4.5** Git commit

### Fase 5 — Entrega
- [ ] **5.1** README.md completo
- [ ] **5.2** Validação no OS atual
- [ ] **5.3** Git commit final + tag v1.0.0
