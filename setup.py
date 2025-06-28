 #!/usr/bin/env python3                                                                                       │ │
│ │ """                                                                                                          │ │
│ │ Setup Script - Instalación automática del sistema AI Director                                                │ │
│ │ Configuración completa para Windows                                                                          │ │
│ │ """                                                                                                          │ │
│ │                                                                                                              │ │
│ │ import os                                                                                                    │ │
│ │ import sys                                                                                                   │ │
│ │ import subprocess                                                                                            │ │
│ │ import platform                                                                                              │ │
│ │ from pathlib import Path                                                                                     │ │
│ │                                                                                                              │ │
│ │ class AIDirectorSetup:                                                                                       │ │
│ │     """Configurador automático del sistema AI Director"""                                                    │ │
│ │                                                                                                              │ │
│ │     def __init__(self):                                                                                      │ │
│ │         self.system_name = "AI Director + Orchestrator + Agent Optimizer"                                    │ │
│ │         self.version = "1.0.0"                                                                               │ │
│ │         self.platform = platform.system()                                                                    │ │
│ │         self.python_version = sys.version_info                                                               │ │
│ │         self.project_dir = Path.cwd()                                                                        │ │
│ │                                                                                                              │ │
│ │     def check_system_requirements(self):                                                                     │ │
│ │         """Verificar requisitos del sistema"""                                                               │ │
│ │         print("🔍 VERIFICANDO REQUISITOS DEL SISTEMA")                                                       │ │
│ │         print("=" * 50)                                                                                      │ │
│ │                                                                                                              │ │
│ │         # Verificar Python                                                                                   │ │
│ │         if self.python_version < (3, 7):                                                                     │ │
│ │             print(f"❌ Python {self.python_version.major}.{self.python_version.minor} detectado")             │ │
│ │             print("⚠️ Se requiere Python 3.7 o superior")                                                    │ │
│ │             return False                                                                                     │ │
│ │         else:                                                                                                │ │
│ │             print(f"✅ Python                                                                                 │ │
│ │ {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")                        │ │
│ │                                                                                                              │ │
│ │         # Verificar plataforma                                                                               │ │
│ │         if self.platform == "Windows":                                                                       │ │
│ │             print("✅ Windows detectado - Compatibilidad completa")                                           │ │
│ │         else:                                                                                                │ │
│ │             print(f"⚠️ {self.platform} detectado - Funcionalidad limitada")                                  │ │
│ │             print("💡 Optimizado para Windows")                                                              │ │
│ │                                                                                                              │ │
│ │         # Verificar pip                                                                                      │ │
│ │         try:                                                                                                 │ │
│ │             import pip                                                                                       │ │
│ │             print("✅ pip disponible")                                                                        │ │
│ │         except ImportError:                                                                                  │ │
│ │             print("❌ pip no encontrado")                                                                     │ │
│ │             return False                                                                                     │ │
│ │                                                                                                              │ │
│ │         print()                                                                                              │ │
│ │         return True                                                                                          │ │
│ │                                                                                                              │ │
│ │     def install_dependencies(self):                                                                          │ │
│ │         """Instalar dependencias automáticamente"""                                                          │ │
│ │         print("📦 INSTALANDO DEPENDENCIAS")                                                                  │ │
│ │         print("=" * 50)                                                                                      │ │
│ │                                                                                                              │ │
│ │         # Lista de dependencias críticas                                                                     │ │
│ │         critical_deps = [                                                                                    │ │
│ │             "psutil>=5.9.0",                                                                                 │ │
│ │             "requests>=2.28.0",                                                                              │ │
│ │             "python-dateutil>=2.8.2"                                                                         │ │
│ │         ]                                                                                                    │ │
│ │                                                                                                              │ │
│ │         # Dependencias específicas de Windows                                                                │ │
│ │         windows_deps = [                                                                                     │ │
│ │             "pywin32>=304",                                                                                  │ │
│ │             "pyautogui>=0.9.54"                                                                              │ │
│ │         ]                                                                                                    │ │
│ │                                                                                                              │ │
│ │         # Dependencias opcionales                                                                            │ │
│ │         optional_deps = [                                                                                    │ │
│ │             "twilio>=8.10.0",                                                                                │ │
│ │             "PyGithub>=1.58.0",                                                                              │ │
│ │             "pyyaml>=6.0",                                                                                   │ │
│ │             "python-dotenv>=1.0.0",                                                                          │ │
│ │             "markdown>=3.5.0"                                                                                │ │
│ │         ]                                                                                                    │ │
│ │                                                                                                              │ │
│ │         all_deps = critical_deps.copy()                                                                      │ │
│ │                                                                                                              │ │
│ │         if self.platform == "Windows":                                                                       │ │
│ │             all_deps.extend(windows_deps)                                                                    │ │
│ │                                                                                                              │ │
│ │         all_deps.extend(optional_deps)                                                                       │ │
│ │                                                                                                              │ │
│ │         # Instalar dependencias                                                                              │ │
│ │         failed_installs = []                                                                                 │ │
│ │                                                                                                              │ │
│ │         for dep in all_deps:                                                                                 │ │
│ │             try:                                                                                             │ │
│ │                 print(f"📥 Instalando {dep}...")                                                             │ │
│ │                 result = subprocess.run([                                                                    │ │
│ │                     sys.executable, "-m", "pip", "install", dep                                              │ │
│ │                 ], capture_output=True, text=True)                                                           │ │
│ │                                                                                                              │ │
│ │                 if result.returncode == 0:                                                                   │ │
│ │                     print(f"✅ {dep} instalado")                                                              │ │
│ │                 else:                                                                                        │ │
│ │                     print(f"⚠️ {dep} falló: {result.stderr.strip()}")                                        │ │
│ │                     failed_installs.append(dep)                                                              │ │
│ │                                                                                                              │ │
│ │             except Exception as e:                                                                           │ │
│ │                 print(f"❌ Error instalando {dep}: {e}")                                                      │ │
│ │                 failed_installs.append(dep)                                                                  │ │
│ │                                                                                                              │ │
│ │         print()                                                                                              │ │
│ │         if failed_installs:                                                                                  │ │
│ │             print("⚠️ DEPENDENCIAS NO INSTALADAS:")                                                          │ │
│ │             for dep in failed_installs:                                                                      │ │
│ │                 print(f"   - {dep}")                                                                         │ │
│ │             print()                                                                                          │ │
│ │             print("💡 Intenta instalar manualmente:")                                                        │ │
│ │             print(f"   pip install {' '.join(failed_installs)}")                                             │ │
│ │             print()                                                                                          │ │
│ │                                                                                                              │ │
│ │         return len(failed_installs) == 0                                                                     │ │
│ │                                                                                                              │ │
│ │     def create_config_files(self):                                                                           │ │
│ │         """Crear archivos de configuración"""                                                                │ │
│ │         print("⚙️ CREANDO CONFIGURACIÓN")                                                                    │ │
│ │         print("=" * 50)                                                                                      │ │
│ │                                                                                                              │ │
│ │         # Crear archivo .env de ejemplo                                                                      │ │
│ │         env_content = """# Configuración AI Director System                                                  │ │
│ │ # Copia este archivo como .env y completa los valores                                                        │ │
│ │                                                                                                              │ │
│ │ # GitHub Token (opcional)                                                                                    │ │
│ │ GITHUB_TOKEN=your_github_token_here                                                                          │ │
│ │                                                                                                              │ │
│ │ # Twilio para WhatsApp (opcional)                                                                            │ │
│ │ TWILIO_ACCOUNT_SID=your_twilio_sid                                                                           │ │
│ │ TWILIO_AUTH_TOKEN=your_twilio_token                                                                          │ │
│ │ TWILIO_PHONE_NUMBER=+1234567890                                                                              │ │
│ │ WHATSAPP_NUMBER=+4917645754360                                                                               │ │
│ │                                                                                                              │ │
│ │ # VS Code Instances                                                                                          │ │
│ │ VSCODE_INSTANCE_1=C:\\VS_Lim1712-1.101.1\\Code.exe                                                           │ │
│ │ VSCODE_INSTANCE_2=C:\\VS_helper_Two-1.101.1\\Code.exe                                                        │ │
│ │ VSCODE_INSTANCE_3=C:\\VSCode_Lim-1.101.1\\Code.exe                                                           │ │
│ │                                                                                                              │ │
│ │ # Agent Optimizer Settings                                                                                   │ │
│ │ DEFAULT_AGENT=claude-haiku                                                                                   │ │
│ │ ENABLE_COST_OPTIMIZATION=true                                                                                │ │
│ │ TOKEN_BUDGET_DAILY=1000                                                                                      │ │
│ │                                                                                                              │ │
│ │ # Monitoring Settings                                                                                        │ │
│ │ MONITORING_INTERVAL=30                                                                                       │ │
│ │ ENABLE_WHATSAPP_NOTIFICATIONS=false                                                                          │ │
│ │ """                                                                                                          │ │
│ │                                                                                                              │ │
│ │         try:                                                                                                 │ │
│ │             with open(".env.example", "w", encoding="utf-8") as f:                                           │ │
│ │                 f.write(env_content)                                                                         │ │
│ │             print("✅ .env.example creado")                                                                   │ │
│ │         except Exception as e:                                                                               │ │
│ │             print(f"❌ Error creando .env.example: {e}")                                                      │ │
│ │                                                                                                              │ │
│ │         # Crear script de inicio rápido                                                                      │ │
│ │         if self.platform == "Windows":                                                                       │ │
│ │             start_script = """@echo off                                                                      │ │
│ │ echo 🚀 Iniciando AI Director System...                                                                      │ │
│ │ echo.                                                                                                        │ │
│ │                                                                                                              │ │
│ │ REM Verificar que Python esté disponible                                                                     │ │
│ │ python --version >nul 2>&1                                                                                   │ │
│ │ if %errorlevel% neq 0 (                                                                                      │ │
│ │     echo ❌ Python no encontrado                                                                              │ │
│ │     echo 💡 Instala Python desde https://python.org                                                          │ │
│ │     pause                                                                                                    │ │
│ │     exit /b 1                                                                                                │ │
│ │ )                                                                                                            │ │
│ │                                                                                                              │ │
│ │ REM Verificar dependencias                                                                                   │ │
│ │ echo 📦 Verificando dependencias...                                                                          │ │
│ │ python -c "import psutil, asyncio; print('✅ Dependencias básicas OK')" >nul 2>&1                             │ │
│ │ if %errorlevel% neq 0 (                                                                                      │ │
│ │     echo ⚠️ Instalando dependencias...                                                                       │ │
│ │     pip install -r requirements.txt                                                                          │ │
│ │ )                                                                                                            │ │
│ │                                                                                                              │ │
│ │ REM Ejecutar sistema                                                                                         │ │
│ │ echo 🎯 Iniciando sistema integrado...                                                                       │ │
│ │ python integrated_system_launcher.py                                                                         │ │
│ │                                                                                                              │ │
│ │ pause                                                                                                        │ │
│ │ """                                                                                                          │ │
│ │             try:                                                                                             │ │
│ │                 with open("start_system.bat", "w", encoding="utf-8") as f:                                   │ │
│ │                     f.write(start_script)                                                                    │ │
│ │                 print("✅ start_system.bat creado")                                                           │ │
│ │             except Exception as e:                                                                           │ │
│ │                 print(f"❌ Error creando start_system.bat: {e}")                                              │ │
│ │                                                                                                              │ │
│ │         print()                                                                                              │ │
│ │                                                                                                              │ │
│ │     def verify_installation(self):                                                                           │ │
│ │         """Verificar que todo esté instalado correctamente"""                                                │ │
│ │         print("🔍 VERIFICANDO INSTALACIÓN")                                                                  │ │
│ │         print("=" * 50)                                                                                      │ │
│ │                                                                                                              │ │
│ │         required_files = [                                                                                   │ │
│ │             "ai_director_system.py",                                                                         │ │
│ │             "vscode_orchestrator.py",                                                                        │ │
│ │             "agent_optimizer_system.py",                                                                     │ │
│ │             "roadmap_intelligence.py",                                                                       │ │
│ │             "roadmap_creator_assistant.py",                                                                  │ │
│ │             "control_dashboard.py",                                                                          │ │
│ │             "integrated_system_launcher.py",                                                                 │ │
│ │             "requirements.txt"                                                                               │ │
│ │         ]                                                                                                    │ │
│ │                                                                                                              │ │
│ │         missing_files = []                                                                                   │ │
│ │         for file in required_files:                                                                          │ │
│ │             if not Path(file).exists():                                                                      │ │
│ │                 missing_files.append(file)                                                                   │ │
│ │                                                                                                              │ │
│ │         if missing_files:                                                                                    │ │
│ │             print("❌ ARCHIVOS FALTANTES:")                                                                   │ │
│ │             for file in missing_files:                                                                       │ │
│ │                 print(f"   - {file}")                                                                        │ │
│ │             print()                                                                                          │ │
│ │             print("💡 Asegúrate de tener todos los archivos del sistema")                                    │ │
│ │             return False                                                                                     │ │
│ │         else:                                                                                                │ │
│ │             print("✅ Todos los archivos del sistema presentes")                                              │ │
│ │                                                                                                              │ │
│ │         # Verificar importaciones críticas                                                                   │ │
│ │         try:                                                                                                 │ │
│ │             import psutil                                                                                    │ │
│ │             import asyncio                                                                                   │ │
│ │             print("✅ Dependencias críticas importables")                                                     │ │
│ │         except ImportError as e:                                                                             │ │
│ │             print(f"❌ Error de importación: {e}")                                                            │ │
│ │             return False                                                                                     │ │
│ │                                                                                                              │ │
│ │         print()                                                                                              │ │
│ │         return True                                                                                          │ │
│ │                                                                                                              │ │
│ │     def show_completion_info(self):                                                                          │ │
│ │         """Mostrar información de finalización"""                                                            │ │
│ │         print("🎉 INSTALACIÓN COMPLETADA")                                                                   │ │
│ │         print("=" * 60)                                                                                      │ │
│ │         print(f"✅ {self.system_name} v{self.version}")                                                       │ │
│ │         print(f"📁 Directorio: {self.project_dir}")                                                          │ │
│ │         print()                                                                                              │ │
│ │                                                                                                              │ │
│ │         print("🚀 CÓMO EJECUTAR:")                                                                           │ │
│ │         print("=" * 60)                                                                                      │ │
│ │                                                                                                              │ │
│ │         if self.platform == "Windows":                                                                       │ │
│ │             print("🖱️ OPCIÓN 1 - Script automático:")                                                       │ │
│ │             print("   Doble clic en: start_system.bat")                                                      │ │
│ │             print()                                                                                          │ │
│ │                                                                                                              │ │
│ │         print("⌨️ OPCIÓN 2 - Línea de comandos:")                                                            │ │
│ │         print("   python integrated_system_launcher.py")                                                     │ │
│ │         print()                                                                                              │ │
│ │                                                                                                              │ │
│ │         print("🎛️ OPCIÓN 3 - Solo dashboard GUI:")                                                          │ │
│ │         print("   python control_dashboard.py")                                                              │ │
│ │         print()                                                                                              │ │
│ │                                                                                                              │ │
│ │         print("📋 CONFIGURACIÓN ADICIONAL:")                                                                 │ │
│ │         print("=" * 60)                                                                                      │ │
│ │         print("1. Copia .env.example a .env")                                                                │ │
│ │         print("2. Completa tus tokens y configuración")                                                      │ │
│ │         print("3. Ajusta las rutas de VS Code si es necesario")                                              │ │
│ │         print()                                                                                              │ │
│ │                                                                                                              │ │
│ │         print("🆘 SOPORTE:")                                                                                 │ │
│ │         print("=" * 60)                                                                                      │ │
│ │         print("- 🧪 Test rápido: python quick_test.py")                                                      │ │
│ │         print("- 📊 Monitor en vivo: python live_test_windows.py")                                           │ │
│ │         print("- 📖 Documentación: README.md")                                                               │ │
│ │         print()                                                                                              │ │
│ │                                                                                                              │ │
│ │ def main():                                                                                                  │ │
│ │     """Función principal de setup"""                                                                         │ │
│ │     setup = AIDirectorSetup()                                                                                │ │
│ │                                                                                                              │ │
│ │     print("🚀 AI DIRECTOR SYSTEM - INSTALACIÓN AUTOMÁTICA")                                                  │ │
│ │     print("=" * 70)                                                                                          │ │
│ │     print(f"Sistema: {setup.system_name}")                                                                   │ │
│ │     print(f"Versión: {setup.version}")                                                                       │ │
│ │     print(f"Plataforma: {setup.platform}")                                                                   │ │
│ │     print()                                                                                                  │ │
│ │                                                                                                              │ │
│ │     # 1. Verificar requisitos                                                                                │ │
│ │     if not setup.check_system_requirements():                                                                │ │
│ │         print("❌ Requisitos no cumplidos")                                                                   │ │
│ │         sys.exit(1)                                                                                          │ │
│ │                                                                                                              │ │
│ │     # 2. Instalar dependencias                                                                               │ │
│ │     print("🔧 ¿Instalar dependencias automáticamente? (y/N): ", end="")                                      │ │
│ │     install_deps = input().strip().lower() == 'y'                                                            │ │
│ │                                                                                                              │ │
│ │     if install_deps:                                                                                         │ │
│ │         success = setup.install_dependencies()                                                               │ │
│ │         if not success:                                                                                      │ │
│ │             print("⚠️ Algunas dependencias fallaron, pero el sistema puede funcionar")                       │ │
│ │                                                                                                              │ │
│ │     # 3. Crear configuración                                                                                 │ │
│ │     setup.create_config_files()                                                                              │ │
│ │                                                                                                              │ │
│ │     # 4. Verificar instalación                                                                               │ │
│ │     if setup.verify_installation():                                                                          │ │
│ │         setup.show_completion_info()                                                                         │ │
│ │     else:                                                                                                    │ │
│ │         print("❌ Instalación incompleta")                                                                    │ │
│ │         print("💡 Verifica que tengas todos los archivos del sistema")                                       │ │
│ │         sys.exit(1)                                                                                          │ │
│ │                                                                                                              │ │
│ │ if __name__ == "__main__":                                                                                   │ │
│ │     try:                                                                                                     │ │
│ │         main()                                                                                               │ │
│ │     except KeyboardInterrupt:                                                                                │ │
│ │         print("\n👋 Instalación cancelada por el usuario")                                                   │ │
│ │     except Exception as e:                                                                                   │ │
│ │         print(f"\n❌ Error durante la instalación: {e}")                                                      │ │
│ │         sys.exit(1)                          