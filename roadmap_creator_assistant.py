  #!/usr/bin/env python3
  """
  Roadmap Creator Assistant
  Sistema que detecta proyectos sin roadmap y genera uno mediante conversación WhatsApp
  """

  import asyncio
  import json
  import re
  from datetime import datetime, timedelta
  from pathlib import Path
  from typing import Dict, List, Optional, Any
  import logging

  class ProjectAnalyzer:
      """Analizador de estructura y tecnologías de proyecto"""

      def __init__(self):
          self.logger = logging.getLogger(__name__)

      def analyze_project_structure(self, project_path: str) -> Dict[str, Any]:
          """Analizar estructura del proyecto y detectar tecnologías"""
          path = Path(project_path)

          if not path.exists():
              return {"error": f"Path no existe: {project_path}"}

          analysis = {
              "path_relative": self._get_relative_path(project_path),
              "technology": self._detect_technology(path),
              "vsc_tag": self._extract_vsc_tag(project_path),
              "has_roadmap": self._check_roadmap_exists(path),
              "project_type": self._detect_project_type(path),
              "file_structure": self._analyze_file_structure(path),
              "dependencies": self._analyze_dependencies(path)
          }

          return analysis

      def _get_relative_path(self, full_path: str) -> str:
          """Obtener path relativo abreviado"""
          path = Path(full_path)

          # Buscar carpeta de proyecto común
          parts = path.parts

          # Buscar indicadores de proyecto
          project_indicators = ['src', 'project', 'workspace', 'code', 'dev']

          for i, part in enumerate(parts):
              if any(indicator in part.lower() for indicator in project_indicators):
                  return str(Path(*parts[i:]))

          # Fallback: últimas 2 carpetas
          return str(Path(*parts[-2:]) if len(parts) > 1 else path.name)

      def _detect_technology(self, path: Path) -> str:
          """Detectar tecnología principal del proyecto"""
          tech_indicators = {
              'React': ['package.json', 'src/App.jsx', 'src/App.js', 'public/index.html'],
              'Vue': ['package.json', 'src/App.vue', 'vue.config.js'],
              'Angular': ['package.json', 'angular.json', 'src/app'],
              'Node.js': ['package.json', 'server.js', 'app.js'],
              'Python': ['requirements.txt', 'setup.py', '*.py', 'main.py'],
              'Java': ['pom.xml', 'build.gradle', 'src/main/java'],
              'C#': ['*.csproj', '*.sln', 'Program.cs'],
              'PHP': ['composer.json', 'index.php', '*.php'],
              'Go': ['go.mod', 'main.go', '*.go'],
              'Rust': ['Cargo.toml', 'src/main.rs'],
              'Flutter': ['pubspec.yaml', 'lib/main.dart'],
              'Unity': ['Assets/', '*.unity', 'ProjectSettings/']
          }

          detected_techs = []

          for tech, indicators in tech_indicators.items():
              score = 0
              for indicator in indicators:
                  if '*' in indicator:
                      # Glob pattern
                      pattern = indicator.replace('*', '**/*')
                      if list(path.glob(pattern)):
                          score += 1
                  else:
                      # File/folder específico
                      if (path / indicator).exists():
                          score += 2

              if score > 0:
                  detected_techs.append((tech, score))

          if detected_techs:
              # Retornar tecnología con mayor score
              return max(detected_techs, key=lambda x: x[1])[0]

          return "Unknown"

      def _extract_vsc_tag(self, project_path: str) -> str:
          """Extraer tag de VS Code desde el path"""
          path_str = str(project_path).lower()

          # Buscar patrones comunes de VS Code portable
          vsc_patterns = [
              r'vs[_-]?(\w+)',
              r'vscode[_-]?(\w+)',
              r'code[_-]?(\w+)'
          ]

          for pattern in vsc_patterns:
              match = re.search(pattern, path_str)
              if match:
                  return match.group(1).title()

          # Fallback: usar parte del path
          parts = Path(project_path).parts
          for part in reversed(parts):
              if 'vs' in part.lower() or 'code' in part.lower():
                  return part.split('-')[0].replace('_', '').title()

          return "Unknown"

      def _check_roadmap_exists(self, path: Path) -> Dict[str, bool]:
          """Verificar si existe roadmap en el proyecto"""
          roadmap_files = [
              'roadmap.md', 'ROADMAP.md', 'roadmap.json',
              'todo.md', 'TODO.md', 'CHANGELOG.md',
              'project-plan.md', 'plan.md', 'milestones.md'
          ]

          found_files = {}
          for filename in roadmap_files:
              found_files[filename] = (path / filename).exists()

          return {
              "has_any_roadmap": any(found_files.values()),
              "files_found": [f for f, exists in found_files.items() if exists],
              "missing_files": [f for f, exists in found_files.items() if not exists]
          }

      def _detect_project_type(self, path: Path) -> str:
          """Detectar tipo de proyecto"""
          type_indicators = {
              'Web App': ['public/', 'src/', 'package.json'],
              'API/Backend': ['api/', 'server/', 'controllers/', 'routes/'],
              'Mobile App': ['ios/', 'android/', 'lib/', 'pubspec.yaml'],
              'Desktop App': ['electron/', 'main.js', '*.exe', 'desktop/'],
              'Library/Package': ['lib/', 'setup.py', 'package.json', 'Cargo.toml'],
              'Game': ['Assets/', 'Scenes/', 'unity', 'game/'],
              'Data Science': ['notebooks/', '*.ipynb', 'data/', 'models/'],
              'DevOps/Scripts': ['scripts/', 'deploy/', 'docker/', 'Dockerfile']
          }

          scores = {}
          for project_type, indicators in type_indicators.items():
              score = 0
              for indicator in indicators:
                  if (path / indicator).exists():
                      score += 1
              scores[project_type] = score

          if scores:
              return max(scores, key=scores.get)

          return "Generic Project"

      def _analyze_file_structure(self, path: Path) -> Dict[str, int]:
          """Analizar estructura de archivos"""
          try:
              structure = {
                  "total_files": 0,
                  "code_files": 0,
                  "config_files": 0,
                  "doc_files": 0,
                  "directories": 0
              }

              code_extensions = {'.js', '.ts', '.py', '.java', '.cs', '.php', '.go', '.rs', '.cpp', '.c',
  '.vue', '.jsx', '.tsx'}
              config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.env'}
              doc_extensions = {'.md', '.txt', '.rst', '.pdf', '.doc', '.docx'}

              for item in path.rglob('*'):
                  if item.is_file():
                      structure["total_files"] += 1

                      if item.suffix in code_extensions:
                          structure["code_files"] += 1
                      elif item.suffix in config_extensions:
                          structure["config_files"] += 1
                      elif item.suffix in doc_extensions:
                          structure["doc_files"] += 1

                  elif item.is_dir():
                      structure["directories"] += 1

              return structure

          except Exception as e:
              self.logger.error(f"Error analizando estructura: {e}")
              return {"error": str(e)}

      def _analyze_dependencies(self, path: Path) -> List[str]:
          """Analizar dependencias del proyecto"""
          dependencies = []

          # package.json (Node.js)
          package_json = path / 'package.json'
          if package_json.exists():
              try:
                  with open(package_json) as f:
                      data = json.load(f)
                      deps = list(data.get('dependencies', {}).keys())
                      dependencies.extend(deps[:5])  # Top 5
              except Exception:
                  pass

          # requirements.txt (Python)
          requirements = path / 'requirements.txt'
          if requirements.exists():
              try:
                  with open(requirements) as f:
                      deps = [line.split('==')[0].strip() for line in f if line.strip()]
                      dependencies.extend(deps[:5])
              except Exception:
                  pass

          return dependencies

  class WhatsAppConversation:
      """Sistema de conversación WhatsApp para recopilar contexto de roadmap"""

      def __init__(self, whatsapp_notifier):
          self.whatsapp = whatsapp_notifier
          self.logger = logging.getLogger(__name__)
          self.conversation_state = {}

      async def start_roadmap_conversation(self, project_analysis: Dict[str, Any]) -> Dict[str, Any]:
          """Iniciar conversación para recopilar contexto del roadmap"""

          # Mensaje inicial con información del proyecto
          abbreviation =
  f"{project_analysis['path_relative']}-{project_analysis['technology']}-{project_analysis['vsc_tag']}"

          initial_message = f"""🔍 PROYECTO SIN ROADMAP DETECTADO

  📁 {abbreviation}
  🛠️ Tecnología: {project_analysis['technology']}
  📋 Tipo: {project_analysis['project_type']}

  ❌ No encuentro roadmap.md o roadmap por fases

  🤖 ¿Quieres que creemos un roadmap automáticamente?

  Responde:
  • SÍ - Para empezar
  • NO - Para saltar
  • INFO - Para más detalles"""

          await self.whatsapp.send_message(initial_message, urgent=True)

          # Inicializar estado de conversación
          conversation_id = f"roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
          self.conversation_state[conversation_id] = {
              "project_analysis": project_analysis,
              "stage": "awaiting_confirmation",
              "collected_data": {},
              "start_time": datetime.now()
          }

          return {"conversation_id": conversation_id, "status": "started"}

      async def process_user_response(self, conversation_id: str, response: str) -> Dict[str, Any]:
          """Procesar respuesta del usuario y continuar conversación"""

          if conversation_id not in self.conversation_state:
              return {"error": "Conversación no encontrada"}

          state = self.conversation_state[conversation_id]
          response = response.strip().upper()

          if state["stage"] == "awaiting_confirmation":
              if response == "SÍ" or response == "SI" or response == "YES":
                  return await self._start_context_questions(conversation_id)
              elif response == "NO":
                  await self.whatsapp.send_message("👌 Entendido. No se creará roadmap automáticamente.")
                  return {"status": "cancelled"}
              elif response == "INFO":
                  return await self._send_project_details(conversation_id)

          elif state["stage"] == "collecting_context":
              return await self._handle_context_response(conversation_id, response)

          return {"status": "waiting", "stage": state["stage"]}

      async def _start_context_questions(self, conversation_id: str) -> Dict[str, Any]:
          """Iniciar secuencia de preguntas de contexto"""

          questions_message = """✅ Perfecto! Necesito contexto para crear el roadmap.

  Responde las siguientes preguntas (una por mensaje):

  1️⃣ **OBJETIVO PRINCIPAL**
  ¿Cuál es el objetivo principal de este proyecto?
  Ejemplo: "Sistema de automatización para WhatsApp"

  Envía tu respuesta ahora 👇"""

          await self.whatsapp.send_message(questions_message)

          self.conversation_state[conversation_id]["stage"] = "collecting_context"
          self.conversation_state[conversation_id]["current_question"] = 1

          return {"status": "collecting", "question": 1}

      async def _handle_context_response(self, conversation_id: str, response: str) -> Dict[str, Any]:
          """Manejar respuestas a preguntas de contexto"""

          state = self.conversation_state[conversation_id]
          question_num = state["current_question"]

          # Guardar respuesta
          question_keys = [
              "objective",
              "timeline",
              "similar_projects",
              "company_context",
              "key_features",
              "resources"
          ]

          if question_num <= len(question_keys):
              state["collected_data"][question_keys[question_num - 1]] = response

          # Siguiente pregunta
          next_questions = {
              1: """2️⃣ **TIMELINE DESEADO**
  ¿En cuánto tiempo quieres completar el proyecto?
  Ejemplo: "3 meses", "6 semanas", "1 año"

  Envía tu respuesta 👇""",

              2: """3️⃣ **PROYECTOS SIMILARES**
  ¿Conoces algún proyecto/web similar como referencia?
  Ejemplo: "Como Zapier", "Similar a Discord bots", "Estilo Notion"

  Envía tu respuesta 👇""",

              3: """4️⃣ **CONTEXTO EMPRESA/PERSONAL**
  ¿Es para empresa, proyecto personal, cliente?
  ¿Algún dato importante del contexto?
  Ejemplo: "Startup fintech", "Proyecto personal", "Cliente e-commerce"

  Envía tu respuesta 👇""",

              4: """5️⃣ **FUNCIONALIDADES CLAVE**
  ¿Cuáles son las 3-5 funcionalidades más importantes?
  Ejemplo: "Login, Chat, Pagos, Reportes, API"

  Envía tu respuesta 👇""",

              5: """6️⃣ **RECURSOS DISPONIBLES**
  ¿Cuántas personas trabajarán? ¿Qué experiencia tienen?
  Ejemplo: "Solo yo, intermedio", "Equipo de 3, seniors"

  Envía tu respuesta 👇"""
          }

          if question_num < 6:
              # Enviar siguiente pregunta
              next_question = next_questions[question_num]
              await self.whatsapp.send_message(next_question)
              state["current_question"] = question_num + 1
              return {"status": "collecting", "question": question_num + 1}

          else:
              # Todas las preguntas respondidas, generar roadmap
              return await self._finalize_context_collection(conversation_id)

      async def _finalize_context_collection(self, conversation_id: str) -> Dict[str, Any]:
          """Finalizar recolección de contexto y generar roadmap"""

          completion_message = """✅ ¡Perfecto! Información recopilada.

  🤖 Generando roadmap personalizado por etapas...
  📋 Incluirá: fases, tareas, timelines, hitos
  ⏱️ Esto tomará unos segundos...

  Te enviaré el roadmap cuando esté listo 📨"""

          await self.whatsapp.send_message(completion_message)

          state = self.conversation_state[conversation_id]
          state["stage"] = "generating_roadmap"

          return {
              "status": "ready_to_generate",
              "collected_data": state["collected_data"],
              "project_analysis": state["project_analysis"]
          }

      async def _send_project_details(self, conversation_id: str) -> Dict[str, Any]:
          """Enviar detalles adicionales del proyecto"""

          state = self.conversation_state[conversation_id]
          analysis = state["project_analysis"]

          details = f"""📊 DETALLES DEL PROYECTO

  📁 Path: {analysis['path_relative']}
  🛠️ Tecnología: {analysis['technology']}
  🏷️ VS Code Tag: {analysis['vsc_tag']}
  📋 Tipo: {analysis['project_type']}

  📈 Estructura:
  • Archivos código: {analysis.get('file_structure', {}).get('code_files', 'N/A')}
  • Archivos config: {analysis.get('file_structure', {}).get('config_files', 'N/A')}
  • Directorios: {analysis.get('file_structure', {}).get('directories', 'N/A')}

  🔗 Dependencias principales:
  {', '.join(analysis.get('dependencies', [])[:3]) or 'Ninguna detectada'}

  ¿Quieres crear el roadmap? (SÍ/NO)"""

          await self.whatsapp.send_message(details)
          return {"status": "info_sent"}

  class RoadmapGenerator:
      """Generador automático de roadmaps por etapas"""

      def __init__(self):
          self.logger = logging.getLogger(__name__)

      def generate_roadmap(self, project_analysis: Dict[str, Any], context_data: Dict[str, Any]) -> str:
          """Generar roadmap completo en formato Markdown"""

          try:
              # Extraer información
              tech = project_analysis['technology']
              project_type = project_analysis['project_type']
              objective = context_data.get('objective', 'No especificado')
              timeline = context_data.get('timeline', '3 meses')
              features = context_data.get('key_features', '').split(',')

              # Generar roadmap por etapas
              roadmap_md = self._create_roadmap_template(
                  project_analysis, context_data, tech, project_type,
                  objective, timeline, features
              )

              return roadmap_md

          except Exception as e:
              self.logger.error(f"Error generando roadmap: {e}")
              return self._create_basic_template(project_analysis, context_data)

      def _create_roadmap_template(self, analysis, context, tech, project_type, objective, timeline, features):
          """Crear template de roadmap personalizado"""

          project_name = analysis.get('path_relative', 'Proyecto').replace('/', ' ')

          # Calcular fases basadas en timeline
          phases = self._calculate_phases(timeline, features)

          roadmap = f"""# {project_name} - Roadmap

  ## 📋 Información del Proyecto

  **Objetivo:** {objective}
  **Tecnología:** {tech}
  **Tipo:** {project_type}
  **Timeline:** {timeline}
  **Última actualización:** {datetime.now().strftime('%Y-%m-%d')}

  ## 🎯 Contexto

  **Proyectos similares:** {context.get('similar_projects', 'No especificado')}
  **Contexto:** {context.get('company_context', 'No especificado')}
  **Recursos:** {context.get('resources', 'No especificado')}

  ## 🗺️ Roadmap por Fases

  """

          # Generar fases
          for i, phase in enumerate(phases, 1):
              roadmap += f"""### Fase {i}: {phase['name']}
  **Duración estimada:** {phase['duration']}
  **Objetivo:** {phase['objective']}

  #### Tareas principales:
  """
              for task in phase['tasks']:
                  status = "[ ]"  # Todas empiezan como pendientes
                  roadmap += f"- {status} **{task['name']}** - {task['hours']}h - {task['due_date']}\n"

              roadmap += f"\n#### Hito: {phase['milestone']}\n\n"

          # Agregar sección de seguimiento
          roadmap += """## 📊 Seguimiento

  ### Métricas de progreso
  - [ ] Fase 1 completada (0%)
  - [ ] Fase 2 completada (0%)
  - [ ] Fase 3 completada (0%)

  ### Riesgos identificados
  - Complejidad técnica en integración
  - Dependencias externas
  - Recursos limitados

  ### Próximos pasos
  1. Revisar y aprobar este roadmap
  2. Configurar entorno de desarrollo
  3. Iniciar Fase 1

  ---
  *Roadmap generado automáticamente por AI Director System*
  """

          return roadmap

      def _calculate_phases(self, timeline: str, features: List[str]) -> List[Dict]:
          """Calcular fases basadas en timeline y features"""

          # Parsear timeline a días
          timeline_days = self._parse_timeline_to_days(timeline)

          # Fases estándar para la mayoría de proyectos
          base_phases = [
              {
                  "name": "Setup & Foundation",
                  "percentage": 0.25,
                  "objective": "Configuración inicial y arquitectura base"
              },
              {
                  "name": "Core Development",
                  "percentage": 0.50,
                  "objective": "Desarrollo de funcionalidades principales"
              },
              {
                  "name": "Integration & Testing",
                  "percentage": 0.15,
                  "objective": "Integración, testing y optimización"
              },
              {
                  "name": "Deployment & Polish",
                  "percentage": 0.10,
                  "objective": "Deploy, documentación y ajustes finales"
              }
          ]

          phases = []
          current_date = datetime.now()

          for i, phase in enumerate(base_phases):
              phase_days = int(timeline_days * phase["percentage"])
              phase_start = current_date + timedelta(days=sum(p["duration_days"] for p in phases))

              phase_data = {
                  "name": phase["name"],
                  "duration": f"{phase_days} días",
                  "duration_days": phase_days,
                  "objective": phase["objective"],
                  "tasks": self._generate_phase_tasks(phase["name"], features, phase_start, phase_days),
                  "milestone": f"Hito {i+1}: {phase['name']} completada"
              }

              phases.append(phase_data)

          return phases

      def _parse_timeline_to_days(self, timeline: str) -> int:
          """Convertir timeline a días"""
          timeline = timeline.lower()

          if 'día' in timeline or 'day' in timeline:
              return int(re.search(r'\d+', timeline).group())
          elif 'semana' in timeline or 'week' in timeline:
              return int(re.search(r'\d+', timeline).group()) * 7
          elif 'mes' in timeline or 'month' in timeline:
              return int(re.search(r'\d+', timeline).group()) * 30
          elif 'año' in timeline or 'year' in timeline:
              return int(re.search(r'\d+', timeline).group()) * 365

          # Default: 90 días (3 meses)
          return 90

      def _generate_phase_tasks(self, phase_name: str, features: List[str], start_date: datetime,
  duration_days: int) -> List[Dict]:
          """Generar tareas para cada fase"""

          task_templates = {
              "Setup & Foundation": [
                  {"name": "Configurar entorno de desarrollo", "hours": 4},
                  {"name": "Crear estructura de proyecto", "hours": 6},
                  {"name": "Configurar control de versiones", "hours": 2},
                  {"name": "Definir arquitectura base", "hours": 8}
              ],
              "Core Development": [
                  {"name": "Implementar funcionalidad principal", "hours": 20},
                  {"name": "Desarrollar interfaz de usuario", "hours": 16},
                  {"name": "Crear sistema de datos", "hours": 12},
                  {"name": "Integrar APIs externas", "hours": 8}
              ],
              "Integration & Testing": [
                  {"name": "Testing unitario", "hours": 8},
                  {"name": "Testing de integración", "hours": 6},
                  {"name": "Optimización de rendimiento", "hours": 4},
                  {"name": "Corrección de bugs", "hours": 6}
              ],
              "Deployment & Polish": [
                  {"name": "Configurar deployment", "hours": 4},
                  {"name": "Documentación", "hours": 6},
                  {"name": "Testing final", "hours": 3},
                  {"name": "Launch y monitoreo", "hours": 3}
              ]
          }

          template_tasks = task_templates.get(phase_name, [])
          tasks = []

          task_interval = duration_days // len(template_tasks) if template_tasks else 1

          for i, task_template in enumerate(template_tasks):
              task_date = start_date + timedelta(days=i * task_interval)

              tasks.append({
                  "name": task_template["name"],
                  "hours": task_template["hours"],
                  "due_date": task_date.strftime('%Y-%m-%d')
              })

          return tasks

      def _create_basic_template(self, analysis: Dict, context: Dict) -> str:
          """Template básico en caso de error"""
          return f"""# Roadmap Básico

  ## Proyecto: {analysis.get('path_relative', 'Unknown')}
  ## Tecnología: {analysis.get('technology', 'Unknown')}

  ### Fase 1: Setup (1-2 semanas)
  - [ ] Configurar entorno
  - [ ] Planificar arquitectura

  ### Fase 2: Desarrollo (4-6 semanas)
  - [ ] Implementar funcionalidades principales
  - [ ] Testing básico

  ### Fase 3: Finalización (1-2 semanas)
  - [ ] Deploy y documentación

  *Roadmap generado automáticamente*
  """

  class RoadmapCreatorAssistant:
      """Sistema principal que orquesta la creación de roadmaps"""

      def __init__(self, whatsapp_notifier):
          self.analyzer = ProjectAnalyzer()
          self.conversation = WhatsAppConversation(whatsapp_notifier)
          self.generator = RoadmapGenerator()

          self.setup_logging()

      def setup_logging(self):
          logging.basicConfig(
              level=logging.INFO,
              format='%(asctime)s - [ROADMAP CREATOR] - %(levelname)s - %(message)s',
              handlers=[
                  logging.FileHandler('roadmap_creator.log'),
                  logging.StreamHandler()
              ]
          )
          self.logger = logging.getLogger(__name__)

      async def check_and_create_roadmaps(self, vscode_instances: Dict[str, str]) -> Dict[str, Any]:
          """Verificar proyectos y crear roadmaps si es necesario"""

          results = {}

          for instance_name, instance_path in vscode_instances.items():
              try:
                  # Buscar directorio de proyecto asociado
                  project_path = self._find_project_directory(instance_path)

                  if not project_path:
                      self.logger.warning(f"No se encontró directorio de proyecto para {instance_name}")
                      continue

                  # Analizar proyecto
                  analysis = self.analyzer.analyze_project_structure(project_path)

                  # Verificar si necesita roadmap
                  if not analysis.get("has_roadmap", {}).get("has_any_roadmap", False):
                      self.logger.info(f"🔍 Proyecto sin roadmap: {instance_name}")

                      # Iniciar conversación
                      conversation_result = await self.conversation.start_roadmap_conversation(analysis)
                      results[instance_name] = {
                          "status": "conversation_started",
                          "analysis": analysis,
                          "conversation_id": conversation_result.get("conversation_id")
                      }
                  else:
                      self.logger.info(f"✅ Proyecto con roadmap: {instance_name}")
                      results[instance_name] = {
                          "status": "roadmap_exists",
                          "analysis": analysis
                      }

              except Exception as e:
                  self.logger.error(f"Error analizando {instance_name}: {e}")
                  results[instance_name] = {"status": "error", "error": str(e)}

          return results

      def _find_project_directory(self, vscode_path: str) -> Optional[str]:
          """Encontrar directorio de proyecto asociado a VS Code instance"""

          # Buscar directorios comunes relativos al VS Code
          base_path = Path(vscode_path).parent

          search_patterns = [
              "project", "workspace", "src", "code", "dev",
              "app", "main", "client", "server"
          ]

          # Buscar en directorio padre
          for pattern in search_patterns:
              potential_path = base_path / pattern
              if potential_path.exists() and potential_path.is_dir():
                  return str(potential_path)

          # Buscar subdirectorios con archivos de proyecto
          for subdir in base_path.iterdir():
              if subdir.is_dir():
                  # Verificar si tiene archivos de proyecto típicos
                  project_files = [
                      'package.json', 'requirements.txt', 'pom.xml',
                      '*.py', '*.js', '*.java', 'src/'
                  ]

                  for pattern in project_files:
                      if list(subdir.glob(pattern)):
                          return str(subdir)

          # Fallback: usar el directorio padre del VS Code
          return str(base_path)

      async def handle_user_response(self, conversation_id: str, response: str) -> Dict[str, Any]:
          """Manejar respuesta del usuario en conversación"""

          result = await self.conversation.process_user_response(conversation_id, response)

          # Si está listo para generar, crear el roadmap
          if result.get("status") == "ready_to_generate":
              return await self._generate_and_save_roadmap(
                  result["project_analysis"],
                  result["collected_data"]
              )

          return result

      async def _generate_and_save_roadmap(self, project_analysis: Dict, context_data: Dict) -> Dict[str, Any]:
          """Generar y guardar roadmap automáticamente"""

          try:
              # Generar contenido del roadmap
              roadmap_content = self.generator.generate_roadmap(project_analysis, context_data)

              # Encontrar directorio del proyecto para guardar
              project_path = self._find_project_directory(
                  f"C:\\{project_analysis['vsc_tag']}-1.101.1"  # Reconstruir path
              )

              if project_path:
                  roadmap_file = Path(project_path) / "roadmap.md"
                  roadmap_file.write_text(roadmap_content, encoding='utf-8')

                  # Notificar por WhatsApp
                  success_message = f"""✅ ¡ROADMAP CREADO!

  📁 Guardado en: {roadmap_file}
  📋 {len(roadmap_content.split('###'))-1} fases generadas
  🎯 Personalizado para tu proyecto

  🔄 El AI Director ya puede empezar a monitorearlo automáticamente.

  ¡Revísalo y ajústalo según necesites! 🚀"""

                  await self.conversation.whatsapp.send_message(success_message)

                  return {
                      "status": "roadmap_created",
                      "file_path": str(roadmap_file),
                      "content_preview": roadmap_content[:200] + "..."
                  }

              else:
                  return {"status": "error", "error": "No se pudo determinar directorio del proyecto"}

          except Exception as e:
              self.logger.error(f"Error generando roadmap: {e}")
              return {"status": "error", "error": str(e)}

  # Función principal para testing
  async def main():
      # Mock WhatsApp notifier para testing
      class MockWhatsApp:
          async def send_message(self, message, urgent=False):
              print(f"📱 WhatsApp: {message}")

      # Crear assistant
      assistant = RoadmapCreatorAssistant(MockWhatsApp())

      # Simular instancias VS Code
      vscode_instances = {
          "VS_lim1712": "C:\\VS_Lim1712-1.101.1",
          "VS_helper_Two": "C:\\VS_helper_Two-1.101.1",
          "VSCode_Lim": "C:\\VSCode_Lim-1.101.1"
      }

      print("🤖 ROADMAP CREATOR ASSISTANT")
      print("=" * 50)

      # Verificar proyectos
      results = await assistant.check_and_create_roadmaps(vscode_instances)

      for instance, result in results.items():
          print(f"\n📁 {instance}:")
          print(f"   Status: {result['status']}")
          if 'analysis' in result:
              analysis = result['analysis']
              print(f"   Tech: {analysis.get('technology', 'Unknown')}")
              print(f"   Type: {analysis.get('project_type', 'Unknown')}")

  if __name__ == "__main__":
      try:
          asyncio.run(main())
      except KeyboardInterrupt:
          print("\n👋 Assistant detenido")