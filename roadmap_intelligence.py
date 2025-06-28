  #!/usr/bin/env python3
  """
  Roadmap Intelligence System
  Sistema avanzado de análisis y seguimiento de roadmaps con notificaciones WhatsApp
  """

  import asyncio
  import json
  import re
  import requests
  import yaml
  from datetime import datetime, timedelta
  from dataclasses import dataclass, asdict
  from pathlib import Path
  from typing import Dict, List, Optional, Any
  import logging
  from enum import Enum

  class TaskStatus(Enum):
      NOT_STARTED = "not_started"
      IN_PROGRESS = "in_progress"
      COMPLETED = "completed"
      DELAYED = "delayed"
      BLOCKED = "blocked"

  class Priority(Enum):
      LOW = 1
      MEDIUM = 2
      HIGH = 3
      CRITICAL = 4

  @dataclass
  class RoadmapTask:
      id: str
      title: str
      description: str
      status: TaskStatus
      priority: Priority
      estimated_hours: float
      actual_hours: float = 0.0
      start_date: Optional[datetime] = None
      due_date: Optional[datetime] = None
      completion_date: Optional[datetime] = None
      dependencies: List[str] = None
      assignee: str = ""
      tags: List[str] = None

      def __post_init__(self):
          if self.dependencies is None:
              self.dependencies = []
          if self.tags is None:
              self.tags = []

      @property
      def is_overdue(self) -> bool:
          if not self.due_date or self.status == TaskStatus.COMPLETED:
              return False
          return datetime.now() > self.due_date

      @property
      def progress_percentage(self) -> float:
          if self.status == TaskStatus.COMPLETED:
              return 100.0
          if self.estimated_hours == 0:
              return 0.0
          return min(100.0, (self.actual_hours / self.estimated_hours) * 100)

  @dataclass
  class Milestone:
      id: str
      title: str
      description: str
      due_date: datetime
      tasks: List[str]  # Task IDs
      completion_percentage: float = 0.0

      @property
      def is_overdue(self) -> bool:
          return datetime.now() > self.due_date and self.completion_percentage < 100.0

  @dataclass
  class ProjectRoadmap:
      project_name: str
      version: str
      created_date: datetime
      last_updated: datetime
      tasks: Dict[str, RoadmapTask]
      milestones: Dict[str, Milestone]

      def get_overdue_tasks(self) -> List[RoadmapTask]:
          return [task for task in self.tasks.values() if task.is_overdue]

      def get_blocked_tasks(self) -> List[RoadmapTask]:
          return [task for task in self.tasks.values() if task.status == TaskStatus.BLOCKED]

      def calculate_overall_progress(self) -> float:
          if not self.tasks:
              return 0.0

          total_weight = sum(task.estimated_hours for task in self.tasks.values())
          if total_weight == 0:
              return 0.0

          completed_weight = sum(
              task.estimated_hours for task in self.tasks.values()
              if task.status == TaskStatus.COMPLETED
          )

          return (completed_weight / total_weight) * 100

  class WhatsAppNotifier:
      """Sistema de notificaciones WhatsApp usando Twilio"""

      def __init__(self, account_sid: str = None, auth_token: str = None, from_number: str = None):
          self.account_sid = account_sid
          self.auth_token = auth_token
          self.from_number = from_number
          self.target_number = "+4917645754360"  # Tu número

          # Para testing sin Twilio real
          self.test_mode = not all([account_sid, auth_token, from_number])

          self.logger = logging.getLogger(__name__)

      async def send_message(self, message: str, urgent: bool = False) -> bool:
          """Enviar mensaje por WhatsApp"""
          try:
              if self.test_mode:
                  # Modo test - solo log
                  prefix = "🚨 URGENT" if urgent else "📱"
                  self.logger.info(f"{prefix} WhatsApp to {self.target_number}:")
                  self.logger.info(f"   {message}")
                  return True

              # Implementación real con Twilio
              try:
                  from twilio.rest import Client

                  client = Client(self.account_sid, self.auth_token)

                  whatsapp_message = client.messages.create(
                      body=message,
                      from_=f'whatsapp:{self.from_number}',
                      to=f'whatsapp:{self.target_number}'
                  )

                  self.logger.info(f"✅ WhatsApp enviado: {whatsapp_message.sid}")
                  return True
              except ImportError:
                  self.logger.warning("⚠️ Twilio no disponible, usando modo test")
                  return await self.send_message(message, urgent)

          except Exception as e:
              self.logger.error(f"❌ Error enviando WhatsApp: {e}")
              return False

      async def send_roadmap_alert(self, alert_type: str, content: Dict[str, Any]):
          """Enviar alerta específica de roadmap"""
          messages = {
              "deviation": "🚨 DESVIACIÓN DETECTADA\n\n{task_name}\nPrevisto: {expected}\nReal: {actual}\n\n💡
  Recomendación: {suggestion}",
              "overdue": "⏰ TAREA VENCIDA\n\n{task_name}\nVencía: {due_date}\nEstado: {status}\n\n🔄 Acción
  requerida",
              "milestone": "🎯 HITO COMPLETADO\n\n{milestone_name}\nCompletado: {completion_date}\nProgreso:
  {percentage}%\n\n🎉 ¡Felicitaciones!",
              "progress": "📊 REPORTE DIARIO\n\nProgreso general: {overall_progress}%\nTareas completadas:
  {completed_tasks}\nTareas pendientes: {pending_tasks}\n\n📈 Tendencia: {trend}"
          }

          template = messages.get(alert_type, "📱 Actualización de roadmap: {content}")
          message = template.format(**content)

          urgent = alert_type in ["deviation", "overdue"]
          await self.send_message(message, urgent)

  class RoadmapReader:
      """Lector universal de roadmaps en múltiples formatos"""

      def __init__(self):
          self.logger = logging.getLogger(__name__)

      def read_markdown_roadmap(self, file_path: Path) -> ProjectRoadmap:
          """Leer roadmap desde archivo Markdown"""
          try:
              content = file_path.read_text(encoding='utf-8')

              # Extraer metadatos del header
              project_name = self._extract_project_name(content)

              # Parsear tareas desde formato Markdown
              tasks = self._parse_markdown_tasks(content)
              milestones = self._parse_markdown_milestones(content)

              return ProjectRoadmap(
                  project_name=project_name,
                  version="1.0",
                  created_date=datetime.now(),
                  last_updated=datetime.now(),
                  tasks=tasks,
                  milestones=milestones
              )

          except Exception as e:
              self.logger.error(f"❌ Error leyendo roadmap MD: {e}")
              raise

      def read_json_roadmap(self, file_path: Path) -> ProjectRoadmap:
          """Leer roadmap desde archivo JSON"""
          try:
              with open(file_path, 'r', encoding='utf-8') as f:
                  data = json.load(f)

              # Convertir dates strings a datetime objects
              tasks = {}
              for task_id, task_data in data.get('tasks', {}).items():
                  task_data = self._convert_dates(task_data)
                  tasks[task_id] = RoadmapTask(**task_data)

              milestones = {}
              for milestone_id, milestone_data in data.get('milestones', {}).items():
                  milestone_data = self._convert_dates(milestone_data)
                  milestones[milestone_id] = Milestone(**milestone_data)

              return ProjectRoadmap(
                  project_name=data['project_name'],
                  version=data.get('version', '1.0'),
                  created_date=self._parse_date(data.get('created_date')),
                  last_updated=self._parse_date(data.get('last_updated')),
                  tasks=tasks,
                  milestones=milestones
              )

          except Exception as e:
              self.logger.error(f"❌ Error leyendo roadmap JSON: {e}")
              raise

      def _extract_project_name(self, content: str) -> str:
          """Extraer nombre del proyecto desde Markdown"""
          lines = content.split('\n')
          for line in lines[:10]:  # Buscar en las primeras 10 líneas
              if line.startswith('# '):
                  return line[2:].strip()
          return "Unknown Project"

      def _parse_markdown_tasks(self, content: str) -> Dict[str, RoadmapTask]:
          """Parsear tareas desde formato Markdown"""
          tasks = {}

          # Regex patterns para diferentes formatos de tareas
          patterns = [
              r'- \[([ x])\] (.+)',  # GitHub style checkboxes
              r'- \*\*(.*?)\*\*.*?(\d+h).*?(\d{4}-\d{2}-\d{2})',  # Custom format
              r'## Task: (.+)',  # Header format
          ]

          task_counter = 1
          for line in content.split('\n'):
              for pattern in patterns:
                  match = re.search(pattern, line, re.IGNORECASE)
                  if match:
                      task_id = f"task_{task_counter}"

                      # Determinar status desde checkbox
                      if len(match.groups()) > 0 and match.group(1):
                          status = TaskStatus.COMPLETED if match.group(1) == 'x' else TaskStatus.NOT_STARTED
                          title = match.group(2)
                      else:
                          status = TaskStatus.NOT_STARTED
                          title = match.group(1) if match.groups() else line.strip('- #')

                      task = RoadmapTask(
                          id=task_id,
                          title=title.strip(),
                          description="",
                          status=status,
                          priority=Priority.MEDIUM,
                          estimated_hours=8.0  # Default
                      )

                      tasks[task_id] = task
                      task_counter += 1
                      break

          return tasks

      def _parse_markdown_milestones(self, content: str) -> Dict[str, Milestone]:
          """Parsear milestones desde Markdown"""
          milestones = {}

          # Buscar secciones de milestones
          milestone_pattern = r'### Milestone: (.+)'

          milestone_counter = 1
          for line in content.split('\n'):
              match = re.search(milestone_pattern, line, re.IGNORECASE)
              if match:
                  milestone_id = f"milestone_{milestone_counter}"
                  title = match.group(1).strip()

                  milestone = Milestone(
                      id=milestone_id,
                      title=title,
                      description="",
                      due_date=datetime.now() + timedelta(days=30),  # Default
                      tasks=[]
                  )

                  milestones[milestone_id] = milestone
                  milestone_counter += 1

          return milestones

      def _convert_dates(self, data: Dict) -> Dict:
          """Convertir strings de fecha a objetos datetime"""
          date_fields = ['start_date', 'due_date', 'completion_date', 'created_date', 'last_updated']

          for field in date_fields:
              if field in data and isinstance(data[field], str):
                  data[field] = self._parse_date(data[field])

          return data

      def _parse_date(self, date_str: str) -> Optional[datetime]:
          """Parsear string de fecha a datetime"""
          if not date_str:
              return None

          formats = [
              '%Y-%m-%d',
              '%Y-%m-%d %H:%M:%S',
              '%Y-%m-%dT%H:%M:%S',
              '%d/%m/%Y'
          ]

          for fmt in formats:
              try:
                  return datetime.strptime(date_str, fmt)
              except ValueError:
                  continue

          return None

  class ProgressAnalyzer:
      """Analizador de progreso real vs planeado"""

      def __init__(self, whatsapp_notifier: WhatsAppNotifier):
          self.whatsapp = whatsapp_notifier
          self.logger = logging.getLogger(__name__)

      async def analyze_roadmap_progress(self, roadmap: ProjectRoadmap) -> Dict[str, Any]:
          """Analizar progreso completo del roadmap"""
          analysis = {
              "overall_progress": roadmap.calculate_overall_progress(),
              "overdue_tasks": roadmap.get_overdue_tasks(),
              "blocked_tasks": roadmap.get_blocked_tasks(),
              "completed_tasks": len([t for t in roadmap.tasks.values() if t.status == TaskStatus.COMPLETED]),
              "total_tasks": len(roadmap.tasks),
              "deviations": [],
              "recommendations": []
          }

          # Detectar desviaciones
          for task in roadmap.tasks.values():
              if task.is_overdue and task.status != TaskStatus.COMPLETED:
                  deviation = {
                      "task_id": task.id,
                      "task_name": task.title,
                      "type": "overdue",
                      "severity": "high" if task.priority == Priority.CRITICAL else "medium",
                      "days_overdue": (datetime.now() - task.due_date).days if task.due_date else 0
                  }
                  analysis["deviations"].append(deviation)

          # Generar recomendaciones
          analysis["recommendations"] = self._generate_recommendations(analysis)

          # Enviar alertas si hay desviaciones críticas
          await self._send_deviation_alerts(analysis)

          return analysis

      def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
          """Generar recomendaciones inteligentes"""
          recommendations = []

          if analysis["overdue_tasks"]:
              recommendations.append(f"🔥 Priorizar {len(analysis['overdue_tasks'])} tareas vencidas")

          if analysis["blocked_tasks"]:
              recommendations.append(f"🚧 Resolver {len(analysis['blocked_tasks'])} tareas bloqueadas")

          if analysis["overall_progress"] < 50:
              recommendations.append("⚡ Acelerar desarrollo - progreso bajo del 50%")

          if len(analysis["deviations"]) > 3:
              recommendations.append("📋 Revisar planning - múltiples desviaciones detectadas")

          return recommendations

      async def _send_deviation_alerts(self, analysis: Dict[str, Any]):
          """Enviar alertas de desviaciones por WhatsApp"""
          critical_deviations = [d for d in analysis["deviations"] if d["severity"] == "high"]

          if critical_deviations:
              for deviation in critical_deviations:
                  await self.whatsapp.send_roadmap_alert("deviation", {
                      "task_name": deviation["task_name"],
                      "expected": "Completada a tiempo",
                      "actual": f"{deviation['days_overdue']} días de retraso",
                      "suggestion": "Revisar recursos y replanning"
                  })

  class RoadmapIntelligence:
      """Sistema principal de inteligencia de roadmaps"""

      def __init__(self):
          self.setup_logging()

          self.whatsapp = WhatsAppNotifier()  # Modo test por defecto
          self.reader = RoadmapReader()
          self.analyzer = ProgressAnalyzer(self.whatsapp)

          self.current_roadmap: Optional[ProjectRoadmap] = None
          self.monitoring_active = False

      def setup_logging(self):
          """Configurar logging"""
          logging.basicConfig(
              level=logging.INFO,
              format='%(asctime)s - [ROADMAP AI] - %(levelname)s - %(message)s',
              handlers=[
                  logging.FileHandler('roadmap_intelligence.log'),
                  logging.StreamHandler()
              ]
          )
          self.logger = logging.getLogger(__name__)

      async def load_roadmap(self, file_path: str) -> bool:
          """Cargar roadmap desde archivo"""
          try:
              path = Path(file_path)

              if not path.exists():
                  self.logger.error(f"❌ Archivo no encontrado: {file_path}")
                  return False

              # Detectar formato y cargar
              if path.suffix.lower() == '.md':
                  self.current_roadmap = self.reader.read_markdown_roadmap(path)
              elif path.suffix.lower() == '.json':
                  self.current_roadmap = self.reader.read_json_roadmap(path)
              else:
                  self.logger.error(f"❌ Formato no soportado: {path.suffix}")
                  return False

              self.logger.info(f"✅ Roadmap cargado: {self.current_roadmap.project_name}")

              # Análisis inicial
              await self._initial_analysis()

              return True

          except Exception as e:
              self.logger.error(f"❌ Error cargando roadmap: {e}")
              return False

      async def _initial_analysis(self):
          """Análisis inicial del roadmap"""
          if not self.current_roadmap:
              return

          analysis = await self.analyzer.analyze_roadmap_progress(self.current_roadmap)

          self.logger.info("📊 ANÁLISIS INICIAL:")
          self.logger.info(f"   Progreso general: {analysis['overall_progress']:.1f}%")
          self.logger.info(f"   Tareas completadas: {analysis['completed_tasks']}/{analysis['total_tasks']}")
          self.logger.info(f"   Tareas vencidas: {len(analysis['overdue_tasks'])}")
          self.logger.info(f"   Tareas bloqueadas: {len(analysis['blocked_tasks'])}")

          # Enviar reporte inicial por WhatsApp
          await self.whatsapp.send_roadmap_alert("progress", {
              "overall_progress": f"{analysis['overall_progress']:.1f}",
              "completed_tasks": analysis['completed_tasks'],
              "pending_tasks": analysis['total_tasks'] - analysis['completed_tasks'],
              "trend": "📈 Estable" if len(analysis['deviations']) == 0 else "⚠️ Desviaciones detectadas"
          })

      async def start_monitoring(self, interval_minutes: int = 60):
          """Iniciar monitoreo continuo"""
          if not self.current_roadmap:
              self.logger.error("❌ No hay roadmap cargado para monitorear")
              return

          self.monitoring_active = True
          self.logger.info(f"🔄 Iniciando monitoreo cada {interval_minutes} minutos")

          while self.monitoring_active:
              try:
                  # Re-analizar progreso
                  analysis = await self.analyzer.analyze_roadmap_progress(self.current_roadmap)

                  # Log de estado
                  if analysis['deviations']:
                      self.logger.warning(f"⚠️ {len(analysis['deviations'])} desviaciones detectadas")

                  # Esperar hasta el siguiente ciclo
                  await asyncio.sleep(interval_minutes * 60)

              except Exception as e:
                  self.logger.error(f"❌ Error en monitoreo: {e}")
                  await asyncio.sleep(60)

      def stop_monitoring(self):
          """Detener monitoreo"""
          self.monitoring_active = False
          self.logger.info("🛑 Monitoreo detenido")

      async def generate_status_report(self) -> Dict[str, Any]:
          """Generar reporte de estado completo"""
          if not self.current_roadmap:
              return {"error": "No roadmap loaded"}

          analysis = await self.analyzer.analyze_roadmap_progress(self.current_roadmap)

          report = {
              "project_name": self.current_roadmap.project_name,
              "last_updated": self.current_roadmap.last_updated.isoformat(),
              "overall_progress": analysis["overall_progress"],
              "task_summary": {
                  "total": analysis["total_tasks"],
                  "completed": analysis["completed_tasks"],
                  "overdue": len(analysis["overdue_tasks"]),
                  "blocked": len(analysis["blocked_tasks"])
              },
              "deviations": analysis["deviations"],
              "recommendations": analysis["recommendations"],
              "next_milestones": self._get_upcoming_milestones()
          }

          return report

      def _get_upcoming_milestones(self) -> List[Dict]:
          """Obtener próximos milestones"""
          if not self.current_roadmap:
              return []

          upcoming = []
          for milestone in self.current_roadmap.milestones.values():
              if milestone.due_date > datetime.now() and milestone.completion_percentage < 100:
                  upcoming.append({
                      "title": milestone.title,
                      "due_date": milestone.due_date.strftime('%Y-%m-%d'),
                      "progress": milestone.completion_percentage
                  })

          return sorted(upcoming, key=lambda x: x["due_date"])[:3]

  # Función principal
  async def main():
      intelligence = RoadmapIntelligence()

      print("🗺️ ROADMAP INTELLIGENCE SYSTEM")
      print("=" * 50)

      # Para testing, crear un roadmap de ejemplo
      example_roadmap_path = input("Ruta del roadmap (Enter para ejemplo): ").strip()

      if not example_roadmap_path:
          # Crear ejemplo
          example_path = Path("example_roadmap.md")
          example_content = """# Proyecto AI Director

  ## Roadmap 2024

  ### Fase 1: Core System
  - [x] Implementar AI Director básico
  - [x] Crear Orchestrator de automatización
  - [ ] **Roadmap Intelligence** - 40h - 2024-01-15
  - [ ] **WhatsApp Integration** - 20h - 2024-01-20

  ### Fase 2: Advanced Features
  - [ ] **Machine Learning** - 60h - 2024-02-01
  - [ ] **API REST** - 30h - 2024-02-15

  ### Milestone: Beta Release
  Fecha objetivo: 2024-01-30
  """

          example_path.write_text(example_content)
          example_roadmap_path = str(example_path)
          print(f"📝 Creado ejemplo: {example_roadmap_path}")

      # Cargar roadmap
      success = await intelligence.load_roadmap(example_roadmap_path)

      if success:
          print("\n🎯 Opciones:")
          print("1. Generar reporte")
          print("2. Iniciar monitoreo")
          print("3. Salir")

          choice = input("\nSelección: ").strip()

          if choice == "1":
              report = await intelligence.generate_status_report()
              print(json.dumps(report, indent=2, default=str))

          elif choice == "2":
              print("🔄 Iniciando monitoreo (Ctrl+C para detener)")
              await intelligence.start_monitoring(interval_minutes=1)  # Test: cada minuto

          print("👋 Sistema detenido")

  if __name__ == "__main__":
      try:
          asyncio.run(main())
      except KeyboardInterrupt:
          print("\n👋 Roadmap Intelligence detenido")
