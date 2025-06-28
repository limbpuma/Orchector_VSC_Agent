#!/usr/bin/env python3
"""
Integrated System Launcher
Lanzador unificado del sistema completo AI Director + Orchestrator + Agent Optimizer
"""

import asyncio
import sys
from pathlib import Path

# Importar todos los sistemas
try:
    from ai_director_system import AIDirector
    from vscode_orchestrator import VSCodeOrchestrator
    from roadmap_intelligence import RoadmapIntelligence, WhatsAppNotifier
    from roadmap_creator_assistant import RoadmapCreatorAssistant
    from agent_optimizer_system import AgentOptimizerSystem
    from control_dashboard import ControlDashboard

    ALL_SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importando sistemas: {e}")
    ALL_SYSTEMS_AVAILABLE = False

class IntegratedSystemLauncher:
    """Lanzador del sistema completo integrado"""

    def __init__(self):
        self.whatsapp_notifier = None
        self.ai_director = None
        self.orchestrator = None
        self.roadmap_intelligence = None
        self.roadmap_creator = None
        self.agent_optimizer = None

    async def initialize_systems(self, enable_whatsapp: bool = True, github_token: str = None):
        """Inicializar todos los sistemas integrados"""

        print("🚀 INICIANDO SISTEMA INTEGRADO")
        print("=" * 60)

        # 1. Inicializar WhatsApp si está habilitado
        if enable_whatsapp:
            print("📱 Inicializando WhatsApp Notifier...")
            self.whatsapp_notifier = WhatsAppNotifier()
            print("✅ WhatsApp Notifier listo")

        # 2. Inicializar Agent Optimizer
        if self.whatsapp_notifier:
            print("🤖 Inicializando Agent Optimizer...")
            self.agent_optimizer = AgentOptimizerSystem(self.whatsapp_notifier)
            print("✅ Agent Optimizer listo")

        # 3. Inicializar AI Director
        print("🧠 Inicializando AI Director...")
        self.ai_director = AIDirector()
        await self.ai_director.initialize(github_token, self.whatsapp_notifier)
        print("✅ AI Director listo")

        # 4. Inicializar Orchestrator
        print("🔧 Inicializando Orchestrator...")
        self.orchestrator = VSCodeOrchestrator()
        self.orchestrator.initialize_agent_optimizer(self.whatsapp_notifier)
        print("✅ Orchestrator listo")

        # 5. Inicializar Roadmap Intelligence
        print("🗺️ Inicializando Roadmap Intelligence...")
        self.roadmap_intelligence = RoadmapIntelligence()
        print("✅ Roadmap Intelligence listo")

        # 6. Inicializar Roadmap Creator
        if self.whatsapp_notifier:
            print("🛠️ Inicializando Roadmap Creator...")
            self.roadmap_creator = RoadmapCreatorAssistant(self.whatsapp_notifier)
            print("✅ Roadmap Creator listo")

        print("=" * 60)
        print("🎉 TODOS LOS SISTEMAS INICIALIZADOS")

        # Verificar proyectos sin roadmap
        if self.roadmap_creator:
            print("\n🔍 Verificando proyectos sin roadmap...")
            vscode_instances = {
                "VS_Lim1712": "C:\\VS_Lim1712-1.101.1",
                "VS_helper_Two": "C:\\VS_helper_Two-1.101.1",
                "VSCode_Lim": "C:\\VSCode_Lim-1.101.1"
            }
            await self.roadmap_creator.check_and_create_roadmaps(vscode_instances)

    async def run_integrated_system(self):
        """Ejecutar sistema integrado con todas las funcionalidades"""

        print("\n🎛️ EJECUTANDO SISTEMA INTEGRADO")
        print("Presiona Ctrl+C para detener")
        print("=" * 60)

        # Crear tareas para todos los sistemas
        tasks = []

        # AI Director monitoring
        if self.ai_director:
            tasks.append(asyncio.create_task(
                self.ai_director.run_continuous_monitoring()
            ))

        # Orchestrator automation
        if self.orchestrator:
            tasks.append(asyncio.create_task(
                self.orchestrator.auto_response_cycle()
            ))
            tasks.append(asyncio.create_task(
                self.orchestrator.monitoring_cycle()
            ))

        # Roadmap Intelligence monitoring
        if self.roadmap_intelligence:
            # Cargar roadmap de ejemplo si existe
            example_roadmap = Path("roadmap.md")
            if example_roadmap.exists():
                await self.roadmap_intelligence.load_roadmap(str(example_roadmap))
                tasks.append(asyncio.create_task(
                    self.roadmap_intelligence.start_monitoring(interval_minutes=30)
                ))

        try:
            # Ejecutar todas las tareas concurrentemente
            await asyncio.gather(*tasks)

        except KeyboardInterrupt:
            print("\n🛑 Deteniendo sistema integrado...")

            # Cancelar todas las tareas
            for task in tasks:
                task.cancel()

            # Detener monitoring específicos
            if self.roadmap_intelligence:
                self.roadmap_intelligence.stop_monitoring()

            print("👋 Sistema integrado detenido")

def show_menu():
    """Mostrar menú de opciones"""
    print("\n🎯 SISTEMA AI DIRECTOR + ORCHESTRATOR + AGENT OPTIMIZER")
    print("=" * 70)
    print("1. 🚀 Ejecutar sistema completo integrado")
    print("2. 🎛️ Abrir Control Dashboard (GUI)")
    print("3. 🧠 Solo AI Director")
    print("4. 🔧 Solo Orchestrator")
    print("5. 🗺️ Solo Roadmap Intelligence")
    print("6. 🤖 Solo Agent Optimizer (test)")
    print("7. ❌ Salir")
    print("=" * 70)

async def main():
    """Función principal con menú de opciones"""

    if not ALL_SYSTEMS_AVAILABLE:
        print("❌ No todos los sistemas están disponibles")
        print("Asegúrate de tener todos los archivos en el directorio")
        return

    while True:
        show_menu()
        choice = input("\n👉 Selecciona una opción (1-7): ").strip()

        if choice == "1":
            # Sistema completo integrado
            launcher = IntegratedSystemLauncher()

            # Configuración
            github_token = input("\n📝 GitHub Token (opcional, Enter para saltar): ").strip()
            github_token = github_token if github_token else None

            enable_whatsapp = input("📱 ¿Activar WhatsApp? (y/N): ").strip().lower() == 'y'

            # Inicializar y ejecutar
            await launcher.initialize_systems(enable_whatsapp, github_token)
            await launcher.run_integrated_system()

        elif choice == "2":
            # Control Dashboard GUI
            print("🎛️ Abriendo Control Dashboard...")
            dashboard = ControlDashboard()
            dashboard.run()

        elif choice == "3":
            # Solo AI Director
            print("🧠 Ejecutando solo AI Director...")
            from ai_director_system import main as director_main
            await director_main()

        elif choice == "4":
            # Solo Orchestrator
            print("🔧 Ejecutando solo Orchestrator...")
            from vscode_orchestrator import main as orchestrator_main
            await orchestrator_main()

        elif choice == "5":
            # Solo Roadmap Intelligence
            print("🗺️ Ejecutando solo Roadmap Intelligence...")
            from roadmap_intelligence import main as roadmap_main
            await roadmap_main()

        elif choice == "6":
            # Solo Agent Optimizer (test)
            print("🤖 Ejecutando Agent Optimizer (test)...")
            from agent_optimizer_system import main as optimizer_main
            await optimizer_main()

        elif choice == "7":
            print("👋 ¡Hasta luego!")
            break

        else:
            print("❌ Opción inválida, intenta de nuevo")

        # Pausa antes de mostrar menú de nuevo
        if choice != "7":
            input("\n⏸️ Presiona Enter para volver al menú...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Sistema interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
