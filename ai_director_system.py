#!/usr/bin/env python3
"""
AI Director System - CTO Virtual para múltiples VS Code instances
Supervisa, coordina y toma decisiones inteligentes sobre 3 proyectos simultáneos
"""

import asyncio
import json
import logging
import psutil
import requests
import time
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

try:
    from agent_optimizer_system import AgentOptimizerSystem
except ImportError:
    AgentOptimizerSystem = None

@dataclass
class VSCodeInstance:
    name: str
    path: str
    repo_url: Optional[str] = None
    priority: int = 1
    status: str = "unknown"
    last_activity: Optional[datetime] = None
    copilot_confirmations: int = 0

@dataclass
class ProjectMetrics:
    commits_today: int = 0
    issues_open: int = 0
    pull_requests: int = 0
    code_coverage: float = 0.0
    build_status: str = "unknown"
    last_deployment: Optional[datetime] = None

class AIDirector:
    """
    Director AI que supervisa y coordina múltiples proyectos VS Code
    Actúa como CTO virtual tomando decisiones inteligentes
    """

    def __init__(self):
        self.instances = {
            "VS_lim1712": VSCodeInstance(
                name="VS_lim1712",
                path="C:\\VS_Lim1712-1.101.1",
                priority=1
            ),
            "VS_helper_Two": VSCodeInstance(
                name="VS_helper_Two",
                path="C:\\VS_helper_Two-1.101.1",
                priority=2
            ),
            "VSCode_Lim": VSCodeInstance(
                name="VSCode_Lim",
                path="C:\\VSCode_Lim-1.101.1",
                priority=3
            )
        }

        self.project_metrics: Dict[str, ProjectMetrics] = {}
        self.decisions_log: List[Dict] = []
        self.github_token: Optional[str] = None

        # Integrar Agent Optimizer
        self.agent_optimizer = None

        self.setup_logging()

    def setup_logging(self):
        """Configurar logging para el Director"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [AI DIRECTOR] - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ai_director.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    async def initialize(self, github_token: str = None, whatsapp_notifier = None):
        """Inicializar el Director AI"""
        self.github_token = github_token
        self.logger.info("🧠 AI Director inicializando...")

        # Inicializar Agent Optimizer si se proporciona WhatsApp
        if whatsapp_notifier and AgentOptimizerSystem:
            self.agent_optimizer = AgentOptimizerSystem(whatsapp_notifier)
            self.logger.info("🤖 Agent Optimizer integrado")

        # Detectar repositorios GitHub de cada instancia
        await self.detect_github_repos()

        # Realizar análisis inicial
        await self.analyze_all_projects()

        self.logger.info("✅ AI Director listo para supervisar")

    async def detect_github_repos(self):
        """Detectar automáticamente los repos GitHub de cada proyecto"""
        for instance_name, instance in self.instances.items():
            try:
                # Buscar .git/config en el directorio del proyecto
                git_config_path = Path(instance.path).parent / "project" / ".git" / "config"

                if git_config_path.exists():
                    with open(git_config_path, 'r') as f:
                        content = f.read()
                        # Extraer URL del repo
                        for line in content.split('\n'):
                            if 'url =' in line and 'github.com' in line:
                                repo_url = line.split('url =')[1].strip()
                                instance.repo_url = repo_url
                                self.logger.info(f"📁 {instance_name}: {repo_url}")
                                break

            except Exception as e:
                self.logger.warning(f"⚠️ No se pudo detectar repo para {instance_name}: {e}")

    async def analyze_project_health(self, instance_name: str) -> ProjectMetrics:
        """Analizar la salud de un proyecto específico"""
        instance = self.instances[instance_name]
        metrics = ProjectMetrics()

        if not instance.repo_url or not self.github_token:
            return metrics

        try:
            # Extraer owner/repo de la URL
            repo_parts = instance.repo_url.replace('.git', '').split('/')
            owner, repo = repo_parts[-2], repo_parts[-1]

            headers = {'Authorization': f'token {self.github_token}'}

            # Obtener commits del día
            today = datetime.now().strftime('%Y-%m-%d')
            commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={today}T00:00:00Z"
            commits_resp = requests.get(commits_url, headers=headers)

            if commits_resp.status_code == 200:
                metrics.commits_today = len(commits_resp.json())

            # Obtener issues abiertas
            issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open"
            issues_resp = requests.get(issues_url, headers=headers)

            if issues_resp.status_code == 200:
                metrics.issues_open = len(issues_resp.json())

            # Obtener PRs abiertas
            prs_url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open"
            prs_resp = requests.get(prs_url, headers=headers)

            if prs_resp.status_code == 200:
                metrics.pull_requests = len(prs_resp.json())

        except Exception as e:
            self.logger.error(f"❌ Error analizando {instance_name}: {e}")

        self.project_metrics[instance_name] = metrics
        return metrics

    async def monitor_vscode_processes(self):
        """Monitorear procesos VS Code y detectar actividad"""
        for instance_name, instance in self.instances.items():
            try:
                # Buscar proceso por nombre y ruta
                for proc in psutil.process_iter(['pid', 'name', 'exe']):
                    if proc.info['name'] == 'Code.exe':
                        exe_path = proc.info.get('exe', '')
                        if instance.path in exe_path:
                            instance.status = "running"
                            instance.last_activity = datetime.now()
                            break
                else:
                    instance.status = "stopped"

            except Exception as e:
                self.logger.error(f"❌ Error monitoreando {instance_name}: {e}")
                instance.status = "error"

    async def make_intelligent_decision(self) -> Dict:
        """Tomar decisiones inteligentes basadas en métricas"""
        decision = {
            "timestamp": datetime.now().isoformat(),
            "type": "priority_adjustment",
            "reasoning": [],
            "actions": []
        }

        # Analizar métricas de todos los proyectos
        for instance_name, metrics in self.project_metrics.items():
            instance = self.instances[instance_name]

            # Lógica de decisión inteligente
            if metrics.commits_today > 5:
                decision["reasoning"].append(f"{instance_name}: Alta actividad ({metrics.commits_today} commits)")
                decision["actions"].append(f"Aumentar prioridad de {instance_name}")
                instance.priority = max(1, instance.priority - 1)

            if metrics.issues_open > 10:
                decision["reasoning"].append(f"{instance_name}: Muchas issues abiertas ({metrics.issues_open})")
                decision["actions"].append(f"Recomendar sesión de bug fixing en {instance_name}")

            if metrics.pull_requests > 3:
                decision["reasoning"].append(f"{instance_name}: PRs pendientes ({metrics.pull_requests})")
                decision["actions"].append(f"Priorizar code review en {instance_name}")

        # Detectar confirmaciones pendientes de Copilot
        copilot_issues = [name for name, inst in self.instances.items()
                          if inst.copilot_confirmations > 0]

        if copilot_issues:
            decision["reasoning"].append(f"Confirmaciones Copilot pendientes: {copilot_issues}")
            decision["actions"].append("Activar respuesta automática")

        # Generar reporte de optimización de agentes si está disponible
        if self.agent_optimizer:
            try:
                usage_report = await self.agent_optimizer.generate_usage_report()
                if usage_report["recommendations"]:
                    decision["reasoning"].append("Optimización de agentes disponible")
                    decision["actions"].extend(usage_report["recommendations"])
            except Exception as e:
                self.logger.error(f"Error en reporte de agentes: {e}")

        self.decisions_log.append(decision)
        return decision

    async def analyze_all_projects(self):
        """Analizar todos los proyectos simultáneamente"""
        tasks = []
        for instance_name in self.instances.keys():
            tasks.append(self.analyze_project_health(instance_name))

        await asyncio.gather(*tasks)

    async def generate_status_report(self) -> Dict:
        """Generar reporte de estado completo"""
        await self.monitor_vscode_processes()
        await self.analyze_all_projects()

        decision = await self.make_intelligent_decision()

        report = {
            "timestamp": datetime.now().isoformat(),
            "instances": {
                name: {
                    "status": inst.status,
                    "priority": inst.priority,
                    "last_activity": inst.last_activity.isoformat() if inst.last_activity else None,
                    "repo_url": inst.repo_url,
                    "copilot_confirmations": inst.copilot_confirmations
                }
                for name, inst in self.instances.items()
            },
            "metrics": {
                name: {
                    "commits_today": metrics.commits_today,
                    "issues_open": metrics.issues_open,
                    "pull_requests": metrics.pull_requests,
                    "build_status": metrics.build_status
                }
                for name, metrics in self.project_metrics.items()
            },
            "latest_decision": decision,
            "recommendations": self.generate_recommendations()
        }

        return report

    def generate_recommendations(self) -> List[str]:
        """Generar recomendaciones inteligentes"""
        recommendations = []

        # Analizar instancias por prioridad
        sorted_instances = sorted(
            self.instances.items(),
            key=lambda x: x[1].priority
        )

        highest_priority = sorted_instances[0]
        recommendations.append(f"🎯 Foco principal: {highest_priority[0]}")

        # Detectar instancias inactivas
        inactive = [name for name, inst in self.instances.items()
                    if inst.status != "running"]

        if inactive:
            recommendations.append(f"⚡ Iniciar instancias: {', '.join(inactive)}")

        # Sugerir based en métricas
        high_issues = [name for name, metrics in self.project_metrics.items()
                       if metrics.issues_open > 5]

        if high_issues:
            recommendations.append(f"🐛 Revisar issues en: {', '.join(high_issues)}")

        return recommendations

    async def run_continuous_monitoring(self, interval: int = 30):
        """Ejecutar monitoreo continuo"""
        self.logger.info(f"🔄 Iniciando monitoreo continuo cada {interval}s")

        while True:
            try:
                report = await self.generate_status_report()

                # Log decisiones importantes
                if report["latest_decision"]["actions"]:
                    self.logger.info("🧠 DECISIÓN AI:")
                    for action in report["latest_decision"]["actions"]:
                        self.logger.info(f"   → {action}")

                # Log recomendaciones
                for rec in report["recommendations"]:
                    self.logger.info(f"💡 {rec}")

                await asyncio.sleep(interval)

            except Exception as e:
                self.logger.error(f"❌ Error en monitoreo continuo: {e}")
                await asyncio.sleep(5)

# Función principal
async def main():
    director = AIDirector()

    # Configurar token GitHub (opcional)
    github_token = input("GitHub Token (opcional, Enter para saltar): ").strip()
    github_token = github_token if github_token else None

    # Configurar WhatsApp para Agent Optimizer (opcional)
    print("\n🤖 Agent Optimizer disponible para optimización inteligente")
    enable_optimizer = input("¿Activar Agent Optimizer? (y/N): ").strip().lower()

    whatsapp_notifier = None
    if enable_optimizer == 'y':
        try:
            from roadmap_intelligence import WhatsAppNotifier
            whatsapp_notifier = WhatsAppNotifier()
            print("✅ Agent Optimizer activado")
        except ImportError:
            print("⚠️ WhatsApp notifier no disponible")

    await director.initialize(github_token, whatsapp_notifier)

    print("\n🧠 AI DIRECTOR ACTIVO")
    print("=" * 50)
    print("Supervising:")
    for name, instance in director.instances.items():
        print(f"  • {name}: {instance.path}")
    if director.agent_optimizer:
        print("  🤖 Agent Optimizer: ACTIVO")
    print("=" * 50)

    # Iniciar monitoreo continuo
    await director.run_continuous_monitoring()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 AI Director detenido por el usuario")
