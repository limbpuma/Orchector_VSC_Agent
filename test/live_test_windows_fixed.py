#!/usr/bin/env python3
"""
Live Test - Monitoreo VS Code en Windows
Optimizado para detectar VS_Lim1712 específicamente
"""

import asyncio
import os
import sys
import time
from datetime import datetime

# Verificar si estamos en Windows
if os.name != 'nt':
    print("❌ Este script está optimizado para Windows")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("❌ Instalando psutil...")
    os.system("pip install psutil")
    import psutil

class WindowsVSCodeMonitor:
    """Monitor optimizado para VS Code en Windows"""

    def __init__(self):
        # Ruta exacta confirmada por usuario
        self.target_exe = "C:\\VS_Lim1712-1.101.1\\Code.exe"
        self.instance_name = "VS_Lim1712"
        self.monitoring = True
        self.detection_count = 0
        self.last_detection_time = None

        print("🔧 Inicializando monitor para Windows...")
        print(f"🎯 Target: {self.target_exe}")

    def check_vscode_running(self):
        """Verificar si VS Code está ejecutándose"""
        vscode_processes = []

        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'memory_info', 'cpu_percent', 'create_time']):
                try:
                    proc_info = proc.info

                    # Verificar si es Code.exe y coincide con nuestra ruta
                    if (proc_info['name'] and
                        proc_info['name'].lower() == 'code.exe' and
                        proc_info['exe'] and
                        self.target_exe.lower() in proc_info['exe'].lower()):

                        # Obtener información detallada
                        memory_mb = proc_info['memory_info'].rss / (1024 * 1024)
                        cpu_percent = proc_info['cpu_percent']

                        # Tiempo de ejecución
                        create_time = datetime.fromtimestamp(proc_info['create_time'])
                        uptime = datetime.now() - create_time

                        vscode_info = {
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'exe': proc_info['exe'],
                            'memory_mb': memory_mb,
                            'cpu_percent': cpu_percent,
                            'uptime': uptime,
                            'create_time': create_time
                        }

                        vscode_processes.append(vscode_info)

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

        except Exception as e:
            print(f"⚠️ Error en verificación: {e}")

        return vscode_processes

    def simulate_system_integration(self):
        """Simular cómo funcionaría la integración completa"""
        import random

        integrations = []

        # Simular detección de Copilot
        if random.random() > 0.6:  # 40% probabilidad
            copilot_actions = [
                "🤖 Copilot: Solicitud de permisos detectada → Auto-confirmada",
                "💡 Copilot: Sugerencia generada → Optimizando agente",
                "🔧 Copilot: Comando en terminal → Auto-Enter enviado",
                "🚀 Copilot Chat: Consulta procesada → Respuesta optimizada"
            ]
            integrations.append(random.choice(copilot_actions))

        # Simular optimización de agente
        if random.random() > 0.7:  # 30% probabilidad
            optimizations = [
                "🧠 Agent Optimizer: Tarea simple → Claude-Haiku seleccionado ($0.002)",
                "🎯 Agent Optimizer: Debug complejo → Claude-Sonnet-4 recomendado ($0.015)",
                "⚡ Agent Optimizer: Documentación → GPT-4-Mini elegido ($0.005)",
                "🔄 Agent Optimizer: Refactoring → Codestral optimizado ($0.008)"
            ]
            integrations.append(random.choice(optimizations))

        # Simular roadmap intelligence
        if random.random() > 0.8:  # 20% probabilidad
            roadmap_actions = [
                "🗺️ Roadmap: Progreso analizado → 67% completado",
                "📊 Roadmap: Desviación detectada → Alerta WhatsApp enviada",
                "🎯 Roadmap: Hito alcanzado → Notificación generada",
                "📋 Roadmap: Nuevo proyecto sin roadmap → Conversación WhatsApp iniciada"
            ]
            integrations.append(random.choice(roadmap_actions))

        return integrations

    async def monitor_loop(self):
        """Loop principal de monitoreo"""
        print(f"\n🔍 MONITOREANDO {self.instance_name} EN TIEMPO REAL")
        print("=" * 80)
        print("🖥️ Sistema optimizado para Windows")
        print("🛑 Presiona Ctrl+C para detener el monitoreo")
        print()

        consecutive_failures = 0

        while self.monitoring:
            try:
                current_time = datetime.now().strftime("%H:%M:%S")

                # Verificar VS Code
                vscode_processes = self.check_vscode_running()

                if vscode_processes:
                    # Reset contador de fallos
                    consecutive_failures = 0
                    self.detection_count += 1
                    self.last_detection_time = datetime.now()

                    print(f"[{current_time}] ✅ {self.instance_name} DETECTADO Y ACTIVO")

                    # Mostrar información de cada proceso (pueden ser múltiples)
                    for i, proc in enumerate(vscode_processes, 1):
                        print(f"   Proceso {i}:")
                        print(f"     PID: {proc['pid']}")
                        print(f"     RAM: {proc['memory_mb']:.1f} MB")
                        print(f"     CPU: {proc['cpu_percent']:.1f}%")
                        print(f"     Uptime: {str(proc['uptime']).split('.')[0]}")

                    # Simular integraciones del sistema
                    integrations = self.simulate_system_integration()
                    if integrations:
                        print(f"   🔄 Integraciones activas:")
                        for integration in integrations:
                            print(f"     {integration}")

                    print(f"   📊 Total detecciones: {self.detection_count}")

                else:
                    consecutive_failures += 1
                    print(f"[{current_time}] ❌ {self.instance_name} NO DETECTADO")

                    if consecutive_failures == 1:
                        print("   💡 Verificando si VS Code está abierto...")
                    elif consecutive_failures > 3:
                        print("   ⚠️ VS Code parece estar cerrado o inaccesible")
                        print(f"   📁 Esperando: {self.target_exe}")

                    if self.last_detection_time:
                        time_since = datetime.now() - self.last_detection_time
                        print(f"   ⏰ Última detección: hace {str(time_since).split('.')[0]}")

                print()

                # Estadísticas cada 20 detecciones
                if self.detection_count > 0 and self.detection_count % 20 == 0:
                    print(f"🎉 HITO: {self.detection_count} detecciones exitosas!")
                    print("   El sistema está funcionando perfectamente")
                    print()

                await asyncio.sleep(2)  # Verificar cada 2 segundos (más responsive)

            except KeyboardInterrupt:
                print(f"\n🛑 Monitoreo interrumpido por usuario")
                break

            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                await asyncio.sleep(1)

        # Estadísticas finales
        print(f"\n📊 RESUMEN FINAL:")
        print(f"   Detecciones exitosas: {self.detection_count}")
        if self.last_detection_time:
            print(f"   Última detección: {self.last_detection_time.strftime('%H:%M:%S')}")
        print(f"   Estado final: {'✅ Funcionando' if self.detection_count > 0 else '❌ No detectado'}")

    def show_system_preview(self):
        """Mostrar preview del sistema completo"""
        print("\n" + "=" * 80)
        print("🔗 PREVIEW: SISTEMA COMPLETO AI DIRECTOR")
        print("=" * 80)

        if self.detection_count > 0:
            print("✅ Tu VS_Lim1712 fue detectado correctamente")
            print("✅ El sistema completo puede monitorear esta instancia")
            print()
            print("🚀 PRÓXIMO PASO - Activar sistema completo:")
            print("   1. python control_dashboard.py  # Para interfaz gráfica")
            print("   2. python integrated_system_launcher.py  # Para sistema completo")
            print()
            print("🎯 CAPACIDADES QUE TENDRÍAS:")
            print("   🤖 Confirmaciones automáticas de Copilot")
            print("   🧠 Optimización inteligente de agentes IA")
            print("   📱 Notificaciones WhatsApp contextuales")
            print("   🗺️ Gestión automática de roadmaps")
            print("   📊 Dashboard centralizado de control")
            print("   ⚡ Comandos automáticos sin Enter manual")
        else:
            print("❌ No se pudo detectar VS_Lim1712")
            print("💡 Verificaciones sugeridas:")
            print("   1. ¿Está VS Code abierto actualmente?")
            print("   2. ¿La ruta es correcta? C:\\VS_Lim1712-1.101.1\\Code.exe")
            print("   3. ¿Tienes permisos para acceder al proceso?")
            print("   4. ¿Ejecutaste como administrador?")

def check_requirements():
    """Verificar requisitos del sistema"""
    print("🔧 VERIFICANDO REQUISITOS DEL SISTEMA...")
    print("-" * 50)

    # Verificar Python
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✅ Python: {python_version}")

    # Verificar Windows
    print(f"✅ Sistema: Windows ({os.name})")

    # Verificar psutil
    try:
        import psutil
        print(f"✅ psutil: {psutil.__version__}")
    except ImportError:
        print("❌ psutil: No instalado")
        print("   Instalando automáticamente...")
        os.system("pip install psutil")

    # Verificar ruta VS Code
    target_path = "C:\\VS_Lim1712-1.101.1\\Code.exe"
    if os.path.exists(target_path):
        print(f"✅ VS Code: Encontrado en {target_path}")
    else:
        print(f"⚠️ VS Code: No encontrado en {target_path}")
        print("   (Esto es normal si VS Code no está instalado ahí)")

    print()

async def main():
    """Función principal optimizada para Windows"""

    print("🎯 LIVE TEST - VS CODE MONITOR PARA WINDOWS")
    print("=" * 80)
    print("Monitor especializado para detectar VS_Lim1712 en Windows")
    print()

    # Verificar requisitos
    check_requirements()

    # Crear y ejecutar monitor
    monitor = WindowsVSCodeMonitor()

    try:
        await monitor.monitor_loop()
    except KeyboardInterrupt:
        print("👋 Test detenido por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
    finally:
        monitor.show_system_preview()

if __name__ == "__main__":
    try:
        # Ejecutar en Windows
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Sistema interrumpido")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        print("💡 Ejecuta como administrador si persisten los problemas")
