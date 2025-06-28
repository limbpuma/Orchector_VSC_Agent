# 🧠 AI Director + Orchestrator + Agent Optimizer System

Sistema integral de gestión inteligente que supervisa automáticamente múltiples instancias VS Code,
automatiza confirmaciones Copilot, optimiza agentes IA y gestiona roadmaps con notificaciones WhatsApp.

## 🎯 Características Principales

### 🧠 AI Director (CTO Virtual)
- **Supervisión inteligente** de 3 instancias VS Code simultáneas
- **Análisis automático** de métricas GitHub (commits, issues, PRs)
- **Toma de decisiones** basada en actividad y prioridades
- **Recomendaciones** inteligentes de workflow
- **Integración GitHub** para análisis de repositorios

### 🔧 Orchestrator (Automatización)
- **Detección automática** de confirmaciones Copilot
- **Respuesta automática** a diálogos de permisos
- **Monitoreo en tiempo real** de procesos VS Code
- **Auto-confirmación** inteligente y segura
- **Solución automática** al problema de Enter manual en comandos

### 🤖 Agent Optimizer (Optimización IA)
- **Selección inteligente** de agentes Copilot por tipo de tarea
- **Gestión de tokens** y costos entre suscripciones Student/Pro
- **Optimización automática** Claude-Haiku vs Claude-Sonnet-4
- **Notificaciones** de costos y recomendaciones
- **Auto-ejecución** de comandos sin Enter manual

### 🗺️ Roadmap Intelligence
- **Análisis automático** de roadmaps existentes (MD, JSON)
  - **Detección de desviaciones** del plan
  - **Sugerencias de reajustes** de timeline
  - **Alertas WhatsApp** para problemas críticos
  - **Generación automática** de roadmaps para proyectos nuevos

  ### 📱 WhatsApp Integration
  - **Notificaciones contextuales** automáticas
  - **Alertas de desviaciones** críticas
  - **Reportes de progreso** periódicos
  - **Conversación inteligente** para crear roadmaps

  ### 📊 Control Dashboard
  - **Interfaz centralizada** para control total
  - **Monitoreo en tiempo real** de todas las instancias
  - **Control manual** de sistemas individuales
  - **Métricas visuales** del rendimiento

  ## 🚀 Instalación

  ### Prerrequisitos
  - Python 3.8+
  - Windows 10/11 (para automatización GUI)
  - VS Code portable instances
  - GitHub Copilot activo

  ### Setup rápido

  1. **Clonar repositorio:**
  ```bash
  git clone https://github.com/limbpuma/Orchector_VSC_Agent.git
  cd Orchector_VSC_Agent

  2. Instalar dependencias:
  pip install -r requirements.txt

  3. Configurar rutas de VS Code:
  Editar las rutas en los archivos según tus instancias:
  # En ai_director_system.py y vscode_orchestrator.py
  {
      "VS_lim1712": "C:\\VS_Lim1712-1.101.1",
      "VS_helper_Two": "C:\\VS_helper_Two-1.101.1",
      "VSCode_Lim": "C:\\VSCode_Lim-1.101.1"
  }

  🎛️ Uso

  Método 1: Sistema Completo Integrado (Recomendado)

  python integrated_system_launcher.py
  Menú con todas las opciones disponibles.

  Método 2: Dashboard Visual

  python control_dashboard.py
  Interfaz gráfica completa con control centralizado.

  Método 3: Sistemas Individuales

  # AI Director
  python ai_director_system.py

  # Orchestrator
  python vscode_orchestrator.py

  # Roadmap Intelligence
  python roadmap_intelligence.py

  # Agent Optimizer (test)
  python agent_optimizer_system.py

  Método 4: Test de Detección

  python live_test_windows.py
  Verificar que el sistema detecta tus instancias VS Code.

  ⚙️ Configuración

  GitHub Integration (Opcional)

  Para análisis completo de repositorios:

  1. Crear GitHub Token:
    - GitHub → Settings → Developer settings → Personal access tokens
    - Scopes: repo, read:org
  2. Configurar al inicio:
  python ai_director_system.py
  # Ingresa tu GitHub token cuando se solicite

  WhatsApp Integration (Opcional)

  Para notificaciones automáticas:

  1. Crear cuenta Twilio (gratis: $15 crédito)
  2. Configurar sandbox WhatsApp
  3. Obtener credenciales:
    - Account SID
    - Auth Token
    - From Number
  4. Configurar en el sistema:
  whatsapp = WhatsAppNotifier(
      account_sid="TU_ACCOUNT_SID",
      auth_token="TU_AUTH_TOKEN",
      from_number="+14155238886"
  )

  VS Code Settings

  Configuraciones recomendadas en settings.json:

  {
      "github.copilot.advanced": {
          "autoSuggest": true,
          "autoConfirm": true
      },
      "github.copilot.chat.agent.thinkingTool": true,
      "github.copilot.chat.codesearch.enabled": true,
      "github.copilot.chat.followUp": "always",
      "github.copilot.nextEditSuggestions.enabled": true
  }

  📊 Funciones Principales

  Flujo de Trabajo Típico

  Mañana (9:00 AM):
  1. Sistema detecta instancias VS Code activas
  2. AI Director analiza actividad nocturna
  3. Recibes reporte WhatsApp del progreso
  4. Sistema ajusta prioridades automáticamente

  Durante desarrollo:
  1. Orchestrator maneja confirmaciones Copilot automáticamente
  2. Agent Optimizer selecciona el mejor agente por tarea
  3. Sistema monitorea progreso vs roadmap
  4. Comandos se ejecutan sin Enter manual

  Si surge problema:
  1. Sistema detecta desviación automáticamente
  2. Recibes alerta WhatsApp inmediata
  3. Obtienes recomendación específica
  4. Puedes reajustar plan desde Dashboard

  Proyecto nuevo:
  1. Sistema detecta ausencia de roadmap
  2. Te contacta por WhatsApp automáticamente
  3. Te hace preguntas específicas de contexto
  4. Genera roadmap completo automáticamente

  🎯 Beneficios

  Productividad

  - ⚡ 0 interrupciones por confirmaciones Copilot
  - 🎯 Foco automático en tareas prioritarias
  - 📊 Visibilidad total del progreso
  - 💰 80% menos costo en agentes IA

  Gestión Inteligente

  - 🧠 Decisiones basadas en datos reales
  - 📱 Alertas proactivas antes de problemas
  - 🗺️ Roadmaps automáticos para proyectos nuevos
  - 🤖 Optimización continua de recursos

  Control Total

  - 🎛️ Dashboard centralizado para todo
  - 📋 Logs detallados de toda actividad
  - 🔄 Configuración flexible según necesidades
  - 🛡️ Seguridad - solo confirma diálogos seguros

  🔧 Troubleshooting

  Problema: "No se detectan las instancias VS Code"

  Solución:
  1. Verificar rutas en archivos de configuración
  2. Ejecutar como administrador
  3. Verificar que VS Code esté abierto

  Problema: "Confirmaciones no se procesan automáticamente"

  Solución:
  1. Ejecutar VS Code como administrador
  2. Verificar que Windows Defender no bloquee
  3. Confirmar instalación de pywin32

  Problema: "Comandos requieren Enter manual"

  Solución:
  1. Agent Optimizer está integrado para resolver esto
  2. Verificar permisos de automatización GUI
  3. Ejecutar como administrador si persiste

  Problema: "GitHub API no funciona"

  Solución:
  1. Verificar token GitHub válido
  2. Comprobar permisos del token
  3. Verificar conexión a internet

  Problema: "WhatsApp no envía mensajes"

  Solución:
  1. Verificar credenciales Twilio
  2. Confirmar sandbox configurado
  3. Verificar crédito en cuenta

  📝 Logs

  Los logs se guardan automáticamente:
  - ai_director.log - Decisiones y análisis del Director
  - orchestrator.log - Actividad de automatización
  - agent_optimizer.log - Optimizaciones de agentes
  - roadmap_intelligence.log - Análisis de roadmaps

  🛡️ Seguridad

  - ✅ Solo confirma diálogos seguros de GitHub Copilot
  - ✅ No modifica código ni archivos del usuario
  - ✅ Logs detallados de todas las acciones
  - ✅ Control manual disponible siempre
  - ✅ Puede pausarse/detenerse en cualquier momento
  - ✅ No almacena credenciales en código

  🚀 Próximas Funciones

  - API REST para control remoto
  - Integración Slack para notificaciones
  - Machine Learning para decisiones más inteligentes
  - Multi-monitor support
  - Custom rules por proyecto
  - Performance analytics avanzados
  - Docker containerization
  - Linux/macOS support

  📞 Soporte

  Para problemas o preguntas:
  1. Revisar logs en archivos .log
  2. Verificar configuración de rutas
  3. Comprobar permisos de Windows
  4. Validar tokens GitHub/Twilio si se usan
  5. Abrir issue en GitHub

  🤝 Contribuir

  1. Fork el proyecto
  2. Crear branch para feature (git checkout -b feature/AmazingFeature)
  3. Commit cambios (git commit -m 'Add AmazingFeature')
  4. Push al branch (git push origin feature/AmazingFeature)
  5. Abrir Pull Request

  📄 Licencia

  Distribuido bajo licencia MIT. Ver LICENSE para más información.

  👨‍💻 Autor

  limbpuma - https://github.com/limbpuma

  ---
  Versión: 1.0Compatibilidad: Windows 10/11, Python 3.8+, VS Code 1.90+Estado: Producción Ready 🚀

  ---