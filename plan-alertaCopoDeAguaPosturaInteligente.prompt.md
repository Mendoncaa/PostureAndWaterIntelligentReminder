## Plan: Alerta Copo de Água & Postura Inteligente

Script Python standalone que monitoriza atividade de teclado/rato, deteta sessões longas (50min+) e envia notificações nativas com piadas de programador. Reset automático após 5min de inatividade.

---

### 1. Tech Stack

| Componente | Tecnologia | Justificação |
|---|---|---|
| Linguagem | **Python 3.10+** | Ecossistema maduro para system-level monitoring |
| Input Monitoring | **`pynput`** | Cross-platform (Win/Mac/Linux), event-driven, baixo consumo |
| Notificações | **`plyer`** | Notificações nativas OS sem dependências pesadas |
| Configuração | `json` stdlib | Zero dependências extra |
| Timers | `threading` stdlib | Sem overhead adicional |
| Testing | `pytest` | Standard com mocking para input events |

**Porquê esta stack?** O `pynput` usa hooks nativos do OS — só consome CPU quando há eventos reais (não faz polling). Alternativas Node.js (iohook) estão descontinuadas. O consumo de recursos é mínimo: ~15MB RAM, CPU negligível.

---

### 2. Arquitetura de Pastas

```
IntelligentReminder/
├── src/
│   ├── main.py                  # Entry point + orquestração
│   ├── monitor/
│   │   ├── activity_tracker.py  # Listeners teclado/rato
│   │   └── idle_detector.py     # Deteção inatividade (5min = reset)
│   ├── notifications/
│   │   ├── notifier.py          # Notificação nativa cross-platform
│   │   └── messages.py          # Loader de piadas/desafios
│   └── config/
│       └── settings.py          # Gestão de configuração
├── tests/
│   ├── test_activity_tracker.py
│   ├── test_idle_detector.py
│   ├── test_notifier.py
│   └── test_integration.py
├── data/
│   └── messages.json            # Banco de piadas PT
├── config.json                  # Config do utilizador
├── pyproject.toml
├── requirements.txt
├── plan.md                      # Tracking de progresso
└── .gitignore
```

---

### 3. Roadmap (Micro-etapas)

#### Fase 1 — Fundação
| Etapa | Descrição | Depende de |
|---|---|---|
| 1.1 | Criar estrutura de pastas e ficheiros base | — |
| 1.2 | Configurar `pyproject.toml`, `requirements.txt`, `.gitignore` | 1.1 |
| 1.3 | Implementar `config/settings.py` com defaults (50min/5min) | 1.1 |
| 1.4 | Criar `config.json` editável pelo utilizador | 1.3 |
| 1.5 | Git init + commit inicial | 1.4 |

#### Fase 2 — Monitorização de Atividade
| Etapa | Descrição | Depende de |
|---|---|---|
| 2.1 | `activity_tracker.py` — listeners teclado + rato via pynput | Fase 1 |
| 2.2 | `idle_detector.py` — reset após 5min sem eventos | 2.1 |
| 2.3 | Testes unitários (mock de eventos) | 2.2 |
| 2.4 | Git commit | 2.3 ✓ |

#### Fase 3 — Notificações
| Etapa | Descrição | Depende de |
|---|---|---|
| 3.1 | `data/messages.json` — 10+ piadas/desafios em PT | — *(paralelo com Fase 2)* |
| 3.2 | `messages.py` — seleção aleatória sem repetição | 3.1 |
| 3.3 | `notifier.py` — envio via plyer (nativo Win/Mac/Linux) | 3.2 |
| 3.4 | Testes unitários | 3.3 |
| 3.5 | Git commit | 3.4 ✓ |

#### Fase 4 — Integração
| Etapa | Descrição | Depende de |
|---|---|---|
| 4.1 | `main.py` — loop principal com timer 50min | Fase 2 + 3 |
| 4.2 | Lógica completa: atividade → notifica; idle 5min → reset | 4.1 |
| 4.3 | Graceful shutdown (Ctrl+C) + cleanup listeners | 4.2 |
| 4.4 | Teste integração end-to-end | 4.3 |
| 4.5 | Git commit | 4.4 ✓ |

#### Fase 5 — Entrega
| Etapa | Descrição | Depende de |
|---|---|---|
| 5.1 | README.md completo | Fase 4 |
| 5.2 | Validação no OS atual | 5.1 |
| 5.3 | Git commit final + tag v1.0.0 | 5.2 ✓ |

---

### Decisões

- **Event-driven, não polling** — zero CPU quando idle
- **Sem IA/ML em v1** — heurística simples (threshold de tempo). IA (padrões de fadiga) fica para v2
- **Excluído do scope v1:** UI gráfica, tray icon, estatísticas, integração direta com VS Code

---

### Verificação

1. `pytest tests/` — todos passam
2. `python src/main.py` — listeners arrancam sem erro
3. Simular 50min atividade (timer acelerado) — notificação aparece
4. Parar input 5min (simulado) — timer reset
5. Ctrl+C — shutdown limpo
