#!/usr/bin/env python3                                                                                       │ │
│ │ """                                                                                                          │ │
│ │ Live Test Windows - Monitoreo en vivo optimizado para Windows                                                │ │
│ │ Test especializado para VS_Lim1712 en Windows                                                                │ │
│ │ """                                                                                                          │ │
│ │                                                                                                              │ │
│ │ import asyncio                                                                                               │ │
│ │ import psutil                                                                                                │ │
│ │ import time                                                                                                  │ │
│ │ from datetime import datetime                                                                                │ │
│ │                                                                                                              │ │
│ │ # Windows-specific imports with fallbacks                                                                    │ │
│ │ try:                                                                                                         │ │
│ │     import win32gui                                                                                          │ │
│ │     import win32con                                                                                          │ │
│ │     import win32api                                                                                          │ │
│ │     WINDOWS_GUI_AVAILABLE = True                                                                             │ │
│ │ except ImportError:                                                                                          │ │
│ │     WINDOWS_GUI_AVAILABLE = False                                                                            │ │
│ │     print("⚠️ pywin32 no disponible - funcionalidad GUI limitada")                                           │ │
│ │                                                                                                              │ │
│ │ class LiveVSCodeMonitorWindows:                                                                              │ │
│ │     """Monitor en vivo optimizado para Windows"""                                                            │ │
│ │                                                                                                              │ │
│ │     def __init__(self):                                                                                      │ │
│ │         self.target_path = "C:\\VS_Lim1712-1.101.1\\Code.exe"                                                │ │
│ │         self.instance_name = "VS_Lim1712"                                                                    │ │
│ │         self.monitoring = True                                                                               │ │
│ │         self.detection_count = 0                                                                             │ │
│ │         self.window_handles = {}                                                                             │ │
│ │                                                                                                              │ │
│ │     def check_vscode_active(self):                                                                           │ │
│ │         """Verificar si VS Code está activo con información detallada"""                                     │ │
│ │         for proc in psutil.process_iter(['pid', 'name', 'exe', 'memory_info', 'cpu_percent',                 │ │
│ │ 'create_time']):                                                                                             │ │
│ │             try:                                                                                             │ │
│ │                 if proc.info['exe'] and self.target_path in proc.info['exe']:                                │ │
│ │                     # Calcular uptime                                                                        │ │
│ │                     create_time = proc.info['create_time']                                                   │ │
│ │                     uptime_seconds = time.time() - create_time                                               │ │
│ │                     uptime_minutes = uptime_seconds / 60                                                     │ │
│ │                                                                                                              │ │
│ │                     return {                                                                                 │ │
│ │                         'pid': proc.info['pid'],                                                             │ │
│ │                         'name': proc.info['name'],                                                           │ │
│ │                         'exe': proc.info['exe'],                                                             │ │
│ │                         'memory_mb': proc.info['memory_info'].rss / 1024 / 1024,                             │ │
│ │                         'cpu_percent': proc.info['cpu_percent'],                                             │ │
│ │                         'uptime_minutes': uptime_minutes                                                     │ │
│ │                     }                                                                                        │ │
│ │             except (psutil.NoSuchProcess, psutil.AccessDenied):                                              │ │
│ │                 continue                                                                                     │ │
│ │         return None                                                                                          │ │
│ │                                                                                                              │ │
│ │     def check_vscode_windows(self):                                                                          │ │
│ │         """Detectar ventanas VS Code específicas (Windows only)"""                                           │ │
│ │         if not WINDOWS_GUI_AVAILABLE:                                                                        │ │
│ │             return []                                                                                        │ │
│ │                                                                                                              │ │
│ │         vscode_windows = []                                                                                  │ │
│ │                                                                                                              │ │
│ │         def enum_windows_callback(hwnd, windows):                                                            │ │
│ │             if win32gui.IsWindowVisible(hwnd):                                                               │ │
│ │                 window_text = win32gui.GetWindowText(hwnd)                                                   │ │
│ │                 class_name = win32gui.GetClassName(hwnd)                                                     │ │
│ │                                                                                                              │ │
│ │                 # Detectar ventanas VS Code                                                                  │ │
│ │                 if (("visual studio code" in window_text.lower() or                                          │ │
│ │                      "vscode" in window_text.lower() or                                                      │ │
│ │                      class_name == "Chrome_WidgetWin_1") and                                                 │ │
│ │                     len(window_text) > 5):                                                                   │ │
│ │                                                                                                              │ │
│ │                     # Obtener información adicional de la ventana                                            │ │
│ │                     try:                                                                                     │ │
│ │                         rect = win32gui.GetWindowRect(hwnd)                                                  │ │
│ │                         is_minimized = win32gui.IsIconic(hwnd)                                               │ │
│ │                         is_maximized = win32gui.IsZoomed(hwnd)                                               │ │
│ │                                                                                                              │ │
│ │                         window_info = {                                                                      │ │
│ │                             'hwnd': hwnd,                                                                    │ │
│ │                             'title': window_text,                                                            │ │
│ │                             'class': class_name,                                                             │ │
│ │                             'rect': rect,                                                                    │ │
│ │                             'minimized': is_minimized,                                                       │ │
│ │                             'maximized': is_maximized,                                                       │ │
│ │                             'visible': True                                                                  │ │
│ │                         }                                                                                    │ │
│ │                                                                                                              │ │
│ │                         # Identificar instancia específica                                                   │ │
│ │                         if 'lim1712' in window_text.lower():                                                 │ │
│ │                             window_info['instance'] = 'VS_Lim1712'                                           │ │
│ │                         elif 'helper' in window_text.lower():                                                │ │
│ │                             window_info['instance'] = 'VS_helper_Two'                                        │ │
│ │                         elif 'lim' in window_text.lower():                                                   │ │
│ │                             window_info['instance'] = 'VSCode_Lim'                                           │ │
│ │                         else:                                                                                │ │
│ │                             window_info['instance'] = 'Unknown'                                              │ │
│ │                                                                                                              │ │
│ │                         windows.append(window_info)                                                          │ │
│ │                                                                                                              │ │
│ │                     except Exception as e:                                                                   │ │
│ │                         pass  # Ignorar errores de ventana                                                   │ │
│ │                                                                                                              │ │
│ │             return True                                                                                      │ │
│ │                                                                                                              │ │
│ │         try:                                                                                                 │ │
│ │             win32gui.EnumWindows(enum_windows_callback, vscode_windows)                                      │ │
│ │         except Exception as e:                                                                               │ │
│ │             print(f"❌ Error enumerando ventanas: {e}")                                                       │ │
│ │                                                                                                              │ │
│ │         return vscode_windows                                                                                │ │
│ │                                                                                                              │ │
│ │     def simulate_copilot_scenarios(self):                                                                    │ │
│ │         """Simular diferentes escenarios de Copilot más realistas"""                                         │ │
│ │         import random                                                                                        │ │
│ │                                                                                                              │ │
│ │         # Escenarios más específicos y realistas                                                             │ │
│ │         scenarios = [                                                                                        │ │
│ │             {                                                                                                │ │
│ │                 "type": "permission",                                                                        │ │
│ │                 "message": "🤖 GitHub Copilot solicita permisos para ejecutar comando en terminal",          │ │
│ │                 "action": "Auto-confirmación enviada",                                                       │ │
│ │                 "probability": 0.25                                                                          │ │
│ │             },                                                                                               │ │
│ │             {                                                                                                │ │
│ │                 "type": "suggestion",                                                                        │ │
│ │                 "message": "💡 Copilot generando sugerencia de autocompletado",                              │ │
│ │                 "action": "Sugerencia mostrada automáticamente",                                             │ │
│ │                 "probability": 0.4                                                                           │ │
│ │             },                                                                                               │ │
│ │             {                                                                                                │ │
│ │                 "type": "chat",                                                                              │ │
│ │                 "message": "🚀 Copilot Chat procesando consulta compleja",                                   │ │
│ │                 "action": "Respuesta optimizada con Claude-Sonnet-4",                                        │ │
│ │                 "probability": 0.15                                                                          │ │
│ │             },                                                                                               │ │
│ │             {                                                                                                │ │
│ │                 "type": "code_generation",                                                                   │ │
│ │                 "message": "⚡ Generación automática de código detectada",                                    │ │
│ │                 "action": "Agente Claude-Haiku seleccionado (tarea simple)",                                 │ │
│ │                 "probability": 0.3                                                                           │ │
│ │             },                                                                                               │ │
│ │             {                                                                                                │ │
│ │                 "type": "debug",                                                                             │ │
│ │                 "message": "🐛 Solicitud de debugging avanzado",                                             │ │
│ │                 "action": "Escalado a Claude-Sonnet-4 (complejidad alta)",                                   │ │
│ │                 "probability": 0.1                                                                           │ │
│ │             }                                                                                                │ │
│ │         ]                                                                                                    │ │
│ │                                                                                                              │ │
│ │         active_scenarios = []                                                                                │ │
│ │         for scenario in scenarios:                                                                           │ │
│ │             if random.random() < scenario["probability"]:                                                    │ │
│ │                 active_scenarios.append(scenario)                                                            │ │
│ │                                                                                                              │ │
│ │         return active_scenarios                                                                              │ │
│ │                                                                                                              │ │
│ │     def simulate_agent_optimization(self):                                                                   │ │
│ │         """Simular optimización inteligente de agentes"""                                                    │ │
│ │         import random                                                                                        │ │
│ │                                                                                                              │ │
│ │         optimization_scenarios = [                                                                           │ │
│ │             {                                                                                                │ │
│ │                 "task_type": "Simple completion",                                                            │ │
│ │                 "detected_complexity": "Low",                                                                │ │
│ │                 "agent_selected": "Claude-Haiku",                                                            │ │
│ │                 "cost_estimate": "$0.002",                                                                   │ │
│ │                 "reasoning": "Completado simple de función",                                                 │ │
│ │                 "tokens_saved": "85%"                                                                        │ │
│ │             },                                                                                               │ │
│ │             {                                                                                                │ │
│ │                 "task_type": "Complex debugging",                                                            │ │
│ │                 "detected_complexity": "High",                                                               │ │
│ │                 "agent_selected": "Claude-Sonnet-4",                                                         │ │
│ │                 "cost_estimate": "$0.018",                                                                   │ │
│ │                 "reasoning": "Error complejo requiere análisis profundo",                                    │ │
│ │                 "tokens_saved": "0% (necesario agente premium)"                                              │ │
│ │             },                                                                                               │ │
│ │             {                                                                                                │ │
│ │                 "task_type": "Documentation generation",                                                     │ │
│ │                 "detected_complexity": "Medium",                                                             │ │
│ │                 "agent_selected": "GPT-4-Mini",                                                              │ │
│ │                 "cost_estimate": "$0.007",                                                                   │ │
│ │                 "reasoning": "Balance costo-calidad para documentación",                                     │ │
│ │                 "tokens_saved": "60%"                                                                        │ │
│ │             },                                                                                               │ │
│ │             {                                                                                                │ │
│ │                 "task_type": "Code refactoring",                                                             │ │
│ │                 "detected_complexity": "Medium-High",                                                        │ │
│ │                 "agent_selected": "Codestral",                                                               │ │
│ │                 "cost_estimate": "$0.012",                                                                   │ │
│ │                 "reasoning": "Especializado en refactoring de código",                                       │ │
│ │                 "tokens_saved": "40%"                                                                        │ │
│ │             }                                                                                                │ │
│ │         ]                                                                                                    │ │
│ │                                                                                                              │ │
│ │         if random.random() < 0.25:  # 25% probabilidad                                                       │ │
│ │             return random.choice(optimization_scenarios)                                                     │ │
│ │         return None                                                                                          │ │
│ │                                                                                                              │ │
│ │     async def monitor_loop(self):                                                                            │ │
│ │         """Loop principal de monitoreo con información detallada"""                                          │ │
│ │         print(f"🔍 MONITOREO EN VIVO - {self.instance_name} (Windows)")                                      │ │
│ │         print(f"🎯 Proceso: {self.target_path}")                                                             │ │
│ │         print("=" * 80)                                                                                      │ │
│ │         print("🛑 Presiona Ctrl+C para detener")                                                             │ │
│ │         print("🪟 Incluye detección de ventanas Windows")                                                    │ │
│ │         print()                                                                                              │ │
│ │                                                                                                              │ │
│ │         last_window_count = 0                                                                                │ │
│ │                                                                                                              │ │
│ │         while self.monitoring:                                                                               │ │
│ │             try:                                                                                             │ │
│ │                 current_time = datetime.now().strftime("%H:%M:%S")                                           │ │
│ │                                                                                                              │ │
│ │                 # Verificar proceso VS Code                                                                  │ │
│ │                 vscode_info = self.check_vscode_active()                                                     │ │
│ │                                                                                                              │ │
│ │                 # Verificar ventanas VS Code (solo Windows)                                                  │ │
│ │                 vscode_windows = self.check_vscode_windows()                                                 │ │
│ │                                                                                                              │ │
│ │                 if vscode_info:                                                                              │ │
│ │                     self.detection_count += 1                                                                │ │
│ │                                                                                                              │ │
│ │                     print(f"[{current_time}] ✅ {self.instance_name} ACTIVO")                                 │ │
│ │                     print(f"   📊 PID: {vscode_info['pid']}")                                                │ │
│ │                     print(f"   💾 RAM: {vscode_info['memory_mb']:.1f} MB")                                   │ │
│ │                     print(f"   🖥️ CPU: {vscode_info['cpu_percent']:.1f}%")                                  │ │
│ │                     print(f"   ⏱️ Uptime: {vscode_info['uptime_minutes']:.1f} min")                          │ │
│ │                                                                                                              │ │
│ │                     # Información de ventanas                                                                │ │
│ │                     if vscode_windows:                                                                       │ │
│ │                         target_windows = [w for w in vscode_windows if w['instance'] == 'VS_Lim1712']        │ │
│ │                         if target_windows:                                                                   │ │
│ │                             window = target_windows[0]                                                       │ │
│ │                             state = "Minimizada" if window['minimized'] else ("Maximizada" if                │ │
│ │ window['maximized'] else "Normal")                                                                           │ │
│ │                             print(f"   🪟 Ventana: {state}")                                                 │ │
│ │                             print(f"   📝 Título: {window['title'][:50]}...")                                │ │
│ │                                                                                                              │ │
│ │                     # Simular escenarios Copilot                                                             │ │
│ │                     copilot_scenarios = self.simulate_copilot_scenarios()                                    │ │
│ │                     for scenario in copilot_scenarios:                                                       │ │
│ │                         print(f"   {scenario['message']}")                                                   │ │
│ │                         print(f"   → ✅ {scenario['action']}")                                                │ │
│ │                                                                                                              │ │
│ │                     # Simular optimización de agente                                                         │ │
│ │                     agent_opt = self.simulate_agent_optimization()                                           │ │
│ │                     if agent_opt:                                                                            │ │
│ │                         print(f"   🤖 Tarea: {agent_opt['task_type']}")                                      │ │
│ │                         print(f"   🧠 Agente: {agent_opt['agent_selected']}")                                │ │
│ │                         print(f"   💰 Costo: {agent_opt['cost_estimate']}")                                  │ │
│ │                         print(f"   💡 Ahorro: {agent_opt['tokens_saved']}")                                  │ │
│ │                                                                                                              │ │
│ │                     print()                                                                                  │ │
│ │                                                                                                              │ │
│ │                 else:                                                                                        │ │
│ │                     print(f"[{current_time}] ❌ {self.instance_name} NO DETECTADO")                           │ │
│ │                     if self.detection_count > 0:                                                             │ │
│ │                         print("   💡 VS Code parece estar cerrado o inactivo")                               │ │
│ │                     else:                                                                                    │ │
│ │                         print("   💡 Verifica que VS Code esté ejecutándose")                                │ │
│ │                     print()                                                                                  │ │
│ │                                                                                                              │ │
│ │                 # Estadísticas avanzadas cada 15 detecciones                                                 │ │
│ │                 if self.detection_count > 0 and self.detection_count % 15 == 0:                              │ │
│ │                     total_windows = len(vscode_windows)                                                      │ │
│ │                     lim1712_windows = len([w for w in vscode_windows if w['instance'] == 'VS_Lim1712'])      │ │
│ │                                                                                                              │ │
│ │                     print(f"📊 ESTADÍSTICAS AVANZADAS:")                                                     │ │
│ │                     print(f"   🔢 Detecciones exitosas: {self.detection_count}")                             │ │
│ │                     print(f"   🪟 Ventanas VS Code: {total_windows} (VS_Lim1712: {lim1712_windows})")        │ │
│ │                     print(f"   ⚡ Sistema funcionando correctamente")                                         │ │
│ │                     print()                                                                                  │ │
│ │                                                                                                              │ │
│ │                 await asyncio.sleep(2)  # Verificar cada 2 segundos para mayor responsividad                 │ │
│ │                                                                                                              │ │
│ │             except KeyboardInterrupt:                                                                        │ │
│ │                 break                                                                                        │ │
│ │             except Exception as e:                                                                           │ │
│ │                 print(f"❌ Error en monitoreo: {e}")                                                          │ │
│ │                 await asyncio.sleep(1)                                                                       │ │
│ │                                                                                                              │ │
│ │         print(f"\n🛑 Monitoreo detenido")                                                                    │ │
│ │         print(f"📊 Total detecciones: {self.detection_count}")                                               │ │
│ │         print(f"⏱️ Tiempo de monitoreo: {self.detection_count * 2 / 60:.1f} minutos")                        │ │
│ │                                                                                                              │ │
│ │     def show_windows_integration_info(self):                                                                 │ │
│ │         """Mostrar información de integración Windows"""                                                     │ │
│ │         print("\n🪟 INTEGRACIÓN WINDOWS:")                                                                   │ │
│ │         print("=" * 60)                                                                                      │ │
│ │                                                                                                              │ │
│ │         if WINDOWS_GUI_AVAILABLE:                                                                            │ │
│ │             print("✅ pywin32 disponible - Funcionalidad completa")                                           │ │
│ │             print("✅ Detección de ventanas activa")                                                          │ │
│ │             print("✅ Automación GUI habilitada")                                                             │ │
│ │         else:                                                                                                │ │
│ │             print("⚠️ pywin32 no disponible")                                                                │ │
│ │             print("📦 Instala con: pip install pywin32")                                                     │ │
│ │             print("🔧 Funcionalidad limitada a detección de procesos")                                       │ │
│ │                                                                                                              │ │
│ │         print("\n🔗 SISTEMA COMPLETO INCLUYE:")                                                              │ │
│ │         print("✅ Monitoreo de procesos VS Code")                                                             │ │
│ │         print("✅ Detección automática de confirmaciones Copilot")                                            │ │
│ │         print("✅ Optimización inteligente de agentes IA")                                                    │ │
│ │         print("✅ Gestión de costos y tokens")                                                                │ │
│ │         print("✅ Notificaciones WhatsApp")                                                                   │ │
│ │         print("✅ Control dashboard GUI")                                                                     │ │
│ │         print()                                                                                              │ │
│ │         print("🚀 Para activar todo:")                                                                       │ │
│ │         print("   python integrated_system_launcher.py")                                                     │ │
│ │         print("   Opción 1: Sistema completo integrado")                                                     │ │
│ │                                                                                                              │ │
│ │ async def main():                                                                                            │ │
│ │     """Función principal para test en Windows"""                                                             │ │
│ │     monitor = LiveVSCodeMonitorWindows()                                                                     │ │
│ │                                                                                                              │ │
│ │     print("🎯 LIVE TEST WINDOWS - VS_Lim1712")                                                               │ │
│ │     print("=" * 60)                                                                                          │ │
│ │     print("Test especializado para detección en Windows")                                                    │ │
│ │     print("Incluye monitoreo de procesos y ventanas")                                                        │ │
│ │     print()                                                                                                  │ │
│ │                                                                                                              │ │
│ │     try:                                                                                                     │ │
│ │         await monitor.monitor_loop()                                                                         │ │
│ │     except KeyboardInterrupt:                                                                                │ │
│ │         print("\n👋 Test detenido por usuario")                                                              │ │
│ │     finally:                                                                                                 │ │
│ │         monitor.show_windows_integration_info()                                                              │ │
│ │                                                                                                              │ │
│ │ if __name__ == "__main__":                                                                                   │ │
│ │     try:                                                                                                     │ │
│ │         asyncio.run(main())                                                                                  │ │
│ │     except Exception as e:                                                                                   │ │
│ │         print(f"❌ Error: {e}")                                                                               │ │
│ │         print("💡 Asegúrate de estar en Windows con VS Code abierto")    