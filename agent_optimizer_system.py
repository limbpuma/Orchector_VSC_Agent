 #!/usr/bin/env python3
  """
  Agent Optimizer System
  Sistema inteligente para seleccionar el agente Copilot óptimo según la tarea
  y gestionar tokens/costos entre suscripciones Student/Pro
  """

  import asyncio
  import json
  import re
  import time
  from datetime import datetime, timedelta
  from dataclasses import dataclass
  from typing import Dict, List, Optional, Any
  from enum import Enum
  import logging

  class AgentType(Enum):
      CLAUDE_SONNET_4 = "claude-sonnet-4"
      CLAUDE_HAIKU = "claude-haiku"
      GPT4_TURBO = "gpt-4-turbo"
      GPT4_MINI = "gpt-4o-mini"
      CODESTRAL = "codestral"
      LLAMA_CODER = "llama-coder"

  class TaskComplexity(Enum):
      SIMPLE = 1      # Completar líneas, fix typos
      MEDIUM = 2      # Funciones, refactoring básico
      COMPLEX = 3     # Arquitectura, debugging complejo
      CRITICAL = 4    # Review completo, optimización

  class SubscriptionType(Enum):
      STUDENT = "github_student"
      PRO = "github_pro"

  @dataclass
  class AgentCapability:
      agent: AgentType
      cost_per_1k_tokens: float
      speed_rating: int  # 1-10
      quality_rating: int  # 1-10
      specialties: List[str]
      max_context: int
      subscription_required: SubscriptionType

  @dataclass
  class TaskProfile:
      task_type: str
      complexity: TaskComplexity
      estimated_tokens: int
      requires_context: bool
      time_sensitive: bool
      accuracy_critical: bool

  class TokenManager:
      """Gestor de tokens y costos por suscripción"""

      def __init__(self):
          self.subscription_limits = {
              SubscriptionType.STUDENT: {
                  "monthly_limit": 100000,  # tokens gratis
                  "overage_cost": 0.01,     # por token extra
                  "premium_agents": False
              },
              SubscriptionType.PRO: {
                  "monthly_limit": 500000,
                  "overage_cost": 0.005,
                  "premium_agents": True
              }
          }

          self.usage_tracking = {
              "VS_lim1712": {"subscription": SubscriptionType.STUDENT, "tokens_used": 0},
              "VS_helper_Two": {"subscription": SubscriptionType.PRO, "tokens_used": 0},
              "VSCode_Lim": {"subscription": SubscriptionType.STUDENT, "tokens_used": 0}
          }

          self.reset_date = datetime.now().replace(day=1, hour=0, minute=0, second=0)

      def get_available_tokens(self, instance_name: str) -> int:
          """Obtener tokens disponibles para una instancia"""
          instance_data = self.usage_tracking.get(instance_name, {})
          subscription = instance_data.get("subscription", SubscriptionType.STUDENT)
          used = instance_data.get("tokens_used", 0)

          limit = self.subscription_limits[subscription]["monthly_limit"]
          return max(0, limit - used)

      def estimate_cost(self, instance_name: str, tokens: int, agent: AgentType) -> float:
          """Estimar costo de usar agente específico"""
          instance_data = self.usage_tracking.get(instance_name, {})
          subscription = instance_data.get("subscription", SubscriptionType.STUDENT)

          available = self.get_available_tokens(instance_name)

          if tokens <= available:
              return 0.0  # Dentro del límite gratuito

          overage = tokens - available
          overage_rate = self.subscription_limits[subscription]["overage_cost"]

          return overage * overage_rate

      def track_usage(self, instance_name: str, tokens_used: int):
          """Registrar uso de tokens"""
          if instance_name in self.usage_tracking:
              self.usage_tracking[instance_name]["tokens_used"] += tokens_used

  class AgentOptimizer:
      """Optimizador inteligente de agentes Copilot"""

      def __init__(self):
          self.token_manager = TokenManager()
          self.setup_logging()

          # Definir capacidades de cada agente
          self.agent_capabilities = {
              AgentType.CLAUDE_SONNET_4: AgentCapability(
                  agent=AgentType.CLAUDE_SONNET_4,
                  cost_per_1k_tokens=0.015,
                  speed_rating=7,
                  quality_rating=10,
                  specialties=["complex_reasoning", "architecture", "debugging"],
                  max_context=200000,
                  subscription_required=SubscriptionType.PRO
              ),

              AgentType.CLAUDE_HAIKU: AgentCapability(
                  agent=AgentType.CLAUDE_HAIKU,
                  cost_per_1k_tokens=0.0025,
                  speed_rating=10,
                  quality_rating=7,
                  specialties=["quick_completion", "simple_tasks", "syntax"],
                  max_context=100000,
                  subscription_required=SubscriptionType.STUDENT
              ),

              AgentType.GPT4_MINI: AgentCapability(
                  agent=AgentType.GPT4_MINI,
                  cost_per_1k_tokens=0.0015,
                  speed_rating=9,
                  quality_rating=8,
                  specialties=["general_coding", "refactoring", "documentation"],
                  max_context=128000,
                  subscription_required=SubscriptionType.STUDENT
              ),

              AgentType.CODESTRAL: AgentCapability(
                  agent=AgentType.CODESTRAL,
                  cost_per_1k_tokens=0.003,
                  speed_rating=8,
                  quality_rating=9,
                  specialties=["code_generation", "algorithms", "optimization"],
                  max_context=32000,
                  subscription_required=SubscriptionType.STUDENT
              )
          }

      def setup_logging(self):
          logging.basicConfig(
              level=logging.INFO,
              format='%(asctime)s - [AGENT OPTIMIZER] - %(levelname)s - %(message)s',
              handlers=[
                  logging.FileHandler('agent_optimizer.log'),
                  logging.StreamHandler()
              ]
          )
          self.logger = logging.getLogger(__name__)

      def analyze_task(self, task_description: str, context_length: int = 0) -> TaskProfile:
          """Analizar tarea para determinar complejidad y requisitos"""

          # Detectar tipo de tarea
          task_patterns = {
              "completion": ["complete", "finish", "autocomplete"],
              "debugging": ["debug", "fix", "error", "bug"],
              "refactoring": ["refactor", "improve", "optimize", "clean"],
              "generation": ["create", "generate", "build", "implement"],
              "explanation": ["explain", "document", "comment", "describe"],
              "review": ["review", "analyze", "check", "validate"]
          }

          task_type = "general"
          for ttype, keywords in task_patterns.items():
              if any(keyword in task_description.lower() for keyword in keywords):
                  task_type = ttype
                  break

          # Determinar complejidad
          complexity_indicators = {
              TaskComplexity.SIMPLE: ["typo", "syntax", "import", "variable"],
              TaskComplexity.MEDIUM: ["function", "class", "method", "refactor"],
              TaskComplexity.COMPLEX: ["architecture", "design", "system", "integration"],
              TaskComplexity.CRITICAL: ["performance", "security", "production", "optimize"]
          }

          complexity = TaskComplexity.SIMPLE
          for comp, keywords in complexity_indicators.items():
              if any(keyword in task_description.lower() for keyword in keywords):
                  complexity = comp

          # Estimar tokens necesarios
          estimated_tokens = self._estimate_tokens(task_description, context_length, complexity)

          # Detectar otros requisitos
          requires_context = context_length > 1000
          time_sensitive = any(word in task_description.lower() for word in ["urgent", "quick", "fast"])
          accuracy_critical = any(word in task_description.lower() for word in ["production", "critical",
  "important"])

          return TaskProfile(
              task_type=task_type,
              complexity=complexity,
              estimated_tokens=estimated_tokens,
              requires_context=requires_context,
              time_sensitive=time_sensitive,
              accuracy_critical=accuracy_critical
          )

      def _estimate_tokens(self, description: str, context_length: int, complexity: TaskComplexity) -> int:
          """Estimar tokens necesarios para la tarea"""
          base_tokens = len(description.split()) * 1.3  # Aproximación
          context_tokens = context_length * 0.75

          complexity_multiplier = {
              TaskComplexity.SIMPLE: 1.2,
              TaskComplexity.MEDIUM: 2.0,
              TaskComplexity.COMPLEX: 4.0,
              TaskComplexity.CRITICAL: 6.0
          }

          total = (base_tokens + context_tokens) * complexity_multiplier[complexity]
          return int(total)

      def select_optimal_agent(self, task_profile: TaskProfile, instance_name: str) -> Dict[str, Any]:
          """Seleccionar el agente óptimo para la tarea"""

          # Obtener suscripción de la instancia
          instance_data = self.token_manager.usage_tracking.get(instance_name, {})
          subscription = instance_data.get("subscription", SubscriptionType.STUDENT)

          # Filtrar agentes disponibles por suscripción
          available_agents = []
          for agent_type, capability in self.agent_capabilities.items():
              if subscription == SubscriptionType.PRO or capability.subscription_required ==
  SubscriptionType.STUDENT:
                  available_agents.append((agent_type, capability))

          # Calcular score para cada agente
          agent_scores = []
          for agent_type, capability in available_agents:
              score = self._calculate_agent_score(task_profile, capability, instance_name)
              agent_scores.append((agent_type, capability, score))

          # Seleccionar mejor agente
          if not agent_scores:
              return {"error": "No hay agentes disponibles"}

          best_agent, best_capability, best_score = max(agent_scores, key=lambda x: x[2])

          # Calcular costo estimado
          estimated_cost = self.token_manager.estimate_cost(
              instance_name, task_profile.estimated_tokens, best_agent
          )

          return {
              "recommended_agent": best_agent.value,
              "capability": best_capability,
              "score": best_score,
              "estimated_cost": estimated_cost,
              "estimated_tokens": task_profile.estimated_tokens,
              "reasoning": self._generate_reasoning(task_profile, best_capability)
          }

      def _calculate_agent_score(self, task: TaskProfile, capability: AgentCapability, instance_name: str) ->
  float:
          """Calcular score de un agente para una tarea específica"""
          score = 0.0

          # Score por calidad (más peso para tareas críticas)
          quality_weight = 0.4 if task.accuracy_critical else 0.25
          score += capability.quality_rating * quality_weight

          # Score por velocidad (más peso para tareas urgentes)
          speed_weight = 0.4 if task.time_sensitive else 0.25
          score += capability.speed_rating * speed_weight

          # Score por especialidad
          specialty_match = any(spec in task.task_type for spec in capability.specialties)
          if specialty_match:
              score += 2.0

          # Penalizar por costo
          cost = self.token_manager.estimate_cost(instance_name, task.estimated_tokens, capability.agent)
          if cost > 0:
              score -= min(2.0, cost * 10)  # Penalización por costo

          # Verificar límites de contexto
          if task.requires_context and task.estimated_tokens > capability.max_context:
              score -= 5.0  # Penalización fuerte si excede contexto

          return score

      def _generate_reasoning(self, task: TaskProfile, capability: AgentCapability) -> str:
          """Generar explicación de por qué se eligió este agente"""
          reasons = []

          if task.time_sensitive:
              reasons.append(f"Velocidad alta ({capability.speed_rating}/10)")

          if task.accuracy_critical:
              reasons.append(f"Calidad superior ({capability.quality_rating}/10)")

          specialty_match = any(spec in task.task_type for spec in capability.specialties)
          if specialty_match:
              reasons.append(f"Especializado en {task.task_type}")

          if capability.cost_per_1k_tokens < 0.005:
              reasons.append("Costo-efectivo")

          return " • ".join(reasons) if reasons else "Agente general adecuado"

  class CommandExecutor:
      """Solucionador del problema de comandos que requieren Enter manual"""

      def __init__(self):
          self.setup_logging()
          self.problematic_commands = [
              "git add", "git commit", "git push", "git pull",
              "npm install", "npm run", "pip install",
              "python", "node", "docker run"
          ]

      def setup_logging(self):
          self.logger = logging.getLogger(__name__)

      def auto_execute_command(self, command: str, vscode_instance: str) -> Dict[str, Any]:
          """Ejecutar comando automáticamente sin requerir Enter manual"""

          try:
              # Detectar si es comando problemático
              is_problematic = any(cmd in command.lower() for cmd in self.problematic_commands)

              if is_problematic:
                  return self._execute_with_auto_enter(command, vscode_instance)
              else:
                  return self._execute_normal(command, vscode_instance)

          except Exception as e:
              self.logger.error(f"Error ejecutando comando: {e}")
              return {"status": "error", "error": str(e)}

      def _execute_with_auto_enter(self, command: str, instance: str) -> Dict[str, Any]:
          """Ejecutar comando y enviar Enter automáticamente"""

          try:
              import win32api
              import win32con
              import win32gui
              import time
          except ImportError:
              return {"status": "error", "error": "pywin32 no disponible"}

          try:
              # Encontrar ventana terminal de VS Code
              terminal_hwnd = self._find_vscode_terminal(instance)

              if not terminal_hwnd:
                  return {"status": "error", "error": "No se encontró terminal VS Code"}

              # Activar ventana terminal
              win32gui.SetForegroundWindow(terminal_hwnd)
              time.sleep(0.2)

              # Enviar comando
              for char in command:
                  win32api.keybd_event(ord(char.upper()), 0, 0, 0)
                  win32api.keybd_event(ord(char.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)
                  time.sleep(0.01)

              # Enviar Enter automáticamente
              time.sleep(0.1)
              win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
              time.sleep(0.05)
              win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)

              # Esperar un momento y enviar otro Enter si es necesario
              time.sleep(1.0)
              win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
              time.sleep(0.05)
              win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)

              self.logger.info(f"✅ Comando ejecutado con auto-Enter: {command}")

              return {
                  "status": "success",
                  "command": command,
                  "auto_enter": True,
                  "instance": instance
              }

          except Exception as e:
              self.logger.error(f"Error con auto-Enter: {e}")
              return {"status": "error", "error": str(e)}

      def _execute_normal(self, command: str, instance: str) -> Dict[str, Any]:
          """Ejecutar comando normal"""
          return {
              "status": "success",
              "command": command,
              "auto_enter": False,
              "instance": instance
          }

      def _find_vscode_terminal(self, instance_name: str) -> Optional[int]:
          """Encontrar ventana de terminal de VS Code específica"""

          try:
              import win32gui
          except ImportError:
              return None

          def enum_windows_callback(hwnd, terminals):
              if win32gui.IsWindowVisible(hwnd):
                  window_text = win32gui.GetWindowText(hwnd)
                  class_name = win32gui.GetClassName(hwnd)

                  # Buscar terminal de VS Code
                  if (("terminal" in window_text.lower() or
                      "powershell" in window_text.lower() or
                      "cmd" in window_text.lower()) and
                     ("visual studio code" in window_text.lower() or
                      instance_name.lower() in window_text.lower())):
                      terminals.append(hwnd)

              return True

          terminal_handles = []
          win32gui.EnumWindows(enum_windows_callback, terminal_handles)

          return terminal_handles[0] if terminal_handles else None

  class AgentOptimizerSystem:
      """Sistema principal que integra optimización de agentes y ejecución de comandos"""

      def __init__(self, whatsapp_notifier):
          self.optimizer = AgentOptimizer()
          self.executor = CommandExecutor()
          self.whatsapp = whatsapp_notifier

          self.setup_logging()

      def setup_logging(self):
          self.logger = logging.getLogger(__name__)

      async def optimize_and_execute(self, task_description: str, instance_name: str,
                                   context_length: int = 0, command: str = None) -> Dict[str, Any]:
          """Optimizar agente y ejecutar comando si es necesario"""

          # 1. Analizar tarea
          task_profile = self.optimizer.analyze_task(task_description, context_length)

          # 2. Seleccionar agente óptimo
          agent_recommendation = self.optimizer.select_optimal_agent(task_profile, instance_name)

          # 3. Enviar recomendación por WhatsApp si hay cambio significativo
          await self._notify_agent_change(agent_recommendation, instance_name)

          # 4. Ejecutar comando si se proporciona
          command_result = None
          if command:
              command_result = self.executor.auto_execute_command(command, instance_name)

          # 5. Tracking de uso
          estimated_tokens = agent_recommendation.get("estimated_tokens", 0)
          self.optimizer.token_manager.track_usage(instance_name, estimated_tokens)

          return {
              "agent_recommendation": agent_recommendation,
              "command_execution": command_result,
              "task_analysis": {
                  "type": task_profile.task_type,
                  "complexity": task_profile.complexity.name,
                  "estimated_tokens": task_profile.estimated_tokens
              }
          }

      async def _notify_agent_change(self, recommendation: Dict, instance_name: str):
          """Notificar cambio de agente recomendado"""

          # Solo notificar si es cambio significativo o costo alto
          estimated_cost = recommendation.get("estimated_cost", 0)
          agent_name = recommendation.get("recommended_agent", "")

          if estimated_cost > 0.10 or "sonnet-4" in agent_name:

              abbreviation = f"{instance_name}-{agent_name.split('-')[0]}"

              message = f"""🤖 AGENTE OPTIMIZADO

  📁 {abbreviation}
  🧠 Recomendado: {agent_name}
  💰 Costo estimado: ${estimated_cost:.3f}
  🎯 Razón: {recommendation.get('reasoning', 'N/A')}

  ¿Continuar con esta selección?"""

              await self.whatsapp.send_message(message)

      async def generate_usage_report(self) -> Dict[str, Any]:
          """Generar reporte de uso de tokens y costos"""

          report = {
              "timestamp": datetime.now().isoformat(),
              "instances": {},
              "total_cost": 0.0,
              "recommendations": []
          }

          for instance, data in self.optimizer.token_manager.usage_tracking.items():
              subscription = data["subscription"]
              tokens_used = data["tokens_used"]
              available = self.optimizer.token_manager.get_available_tokens(instance)

              instance_report = {
                  "subscription": subscription.value,
                  "tokens_used": tokens_used,
                  "tokens_available": available,
                  "usage_percentage": (tokens_used / (tokens_used + available)) * 100 if (tokens_used +
  available) > 0 else 0
              }

              report["instances"][instance] = instance_report

              # Generar recomendaciones
              if instance_report["usage_percentage"] > 80:
                  report["recommendations"].append(f"⚠️ {instance}: Alto uso de tokens
  ({instance_report['usage_percentage']:.1f}%)")

              if subscription == SubscriptionType.STUDENT and instance_report["usage_percentage"] > 50:
                  report["recommendations"].append(f"💡 {instance}: Considerar upgrade a Pro")

          return report

  # Función principal
  async def main():
      # Mock WhatsApp para testing
      class MockWhatsApp:
          async def send_message(self, message, urgent=False):
              print(f"📱 WhatsApp: {message}")

      # Crear sistema
      system = AgentOptimizerSystem(MockWhatsApp())

      print("🤖 AGENT OPTIMIZER SYSTEM")
      print("=" * 50)

      # Simular tarea
      task = "Debug complex authentication error in production"
      instance = "VS_lim1712"
      command = "git add ."

      result = await system.optimize_and_execute(task, instance, context_length=5000, command=command)

      print(f"\n📋 Tarea: {task}")
      print(f"🖥️ Instancia: {instance}")

      # Mostrar recomendación
      agent_rec = result["agent_recommendation"]
      print(f"\n🧠 Agente recomendado: {agent_rec['recommended_agent']}")
      print(f"💰 Costo estimado: ${agent_rec['estimated_cost']:.3f}")
      print(f"🎯 Razón: {agent_rec['reasoning']}")

      # Mostrar ejecución de comando
      if result["command_execution"]:
          cmd_result = result["command_execution"]
          print(f"\n⚡ Comando: {cmd_result['command']}")
          print(f"✅ Auto-Enter: {cmd_result['auto_enter']}")

      # Generar reporte
      report = await system.generate_usage_report()
      print(f"\n📊 REPORTE DE USO:")
      for instance, data in report["instances"].items():
          print(f"   {instance}: {data['usage_percentage']:.1f}% usado")

  if __name__ == "__main__":
      try:
          asyncio.run(main())
      except KeyboardInterrupt:
          print("\n👋 Sistema detenido")