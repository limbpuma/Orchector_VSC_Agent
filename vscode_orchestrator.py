#!/usr/bin/env python3
"""
VS Code Orchestrator - Sistema de automatización para confirmaciones Copilot
Maneja automáticamente diálogos y confirmaciones en múltiples instancias VS Code
"""

import asyncio
import ctypes
import json
import logging
import psutil
import time
from ctypes import wintypes
from datetime import datetime
from typing import Dict, List, Optional

try:
    import win32api
    import win32con
    import win32gui
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    print("⚠️ pywin32 no disponible. Funcionalidad limitada en non-Windows.")

try:
    from agent_optimizer_system import AgentOptimizerSystem
except ImportError:
    AgentOptimizerSystem = None

class VSCodeOrchestrator:
    """
    Orquestador técnico que automatiza confirmaciones y monitorea VS Code
    """

    def __init__(self):
        self.target_instances = {
            "VS_lim1712": "C:\\VS_Lim1712-1.101.1",
            "VS_helper_Two": "C:\\VS_helper_Two-1.101.1",
            "VSCode_Lim": "C:\\VSCode_Lim-1.101.1"
        }

        self.active_windows: Dict[str, int] = {}
        self.confirmation_count = 0
        self.auto_responses_enabled = True

        # Integrar Agent Optimizer
        self.agent_optimizer = None

        self.setup_logging()

    def setup_logging(self):
        """Configurar logging detallado"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [ORCHESTRATOR] - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def find_vscode_windows(self) -> Dict[str, List[int]]:
        """Encontrar todas las ventanas VS Code activas"""
        if not WINDOWS_AVAILABLE:
            return {}

        vscode_windows = {}

        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)

                # Detectar ventanas VS Code
                if ("Visual Studio Code" in window_text or
                    class_name == "Chrome_WidgetWin_1"):

                    # Intentar identificar qué instancia
                    for instance_name, path in self.target_instances.items():
                        if instance_name.lower() in window_text.lower():
                            if instance_name not in windows:
                                windows[instance_name] = []
                            windows[instance_name].append(hwnd)
                            break
                    else:
                        # Ventana VS Code genérica
                        if "generic" not in windows:
                            windows["generic"] = []
                        windows["generic"].append(hwnd)

            return True

        win32gui.EnumWindows(enum_windows_callback, vscode_windows)
        return vscode_windows

    def find_copilot_dialogs(self) -> List[Dict]:
        """Encontrar diálogos de confirmación de Copilot"""
        if not WINDOWS_AVAILABLE:
            return []

        dialogs = []

        def enum_windows_callback(hwnd, dialogs_list):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)

                # Buscar diálogos típicos de GitHub Copilot
                copilot_keywords = [
                    "GitHub Copilot",
                    "Allow Copilot",
                    "Copilot wants to",
                    "Permission",
                    "Allow access",
                    "Confirm"
                ]

                if any(keyword.lower() in window_text.lower() for keyword in copilot_keywords):
                    dialog_info = {
                        'hwnd': hwnd,
                        'title': window_text,
                        'class': class_name,
                        'timestamp': datetime.now()
                    }
                    dialogs_list.append(dialog_info)
                    self.logger.info(f"🔍 Diálogo Copilot detectado: {window_text}")

            return True

        win32gui.EnumWindows(enum_windows_callback, dialogs)
        return dialogs

    def auto_confirm_dialog(self, dialog_hwnd: int) -> bool:
        """Confirmar automáticamente un diálogo"""
        if not WINDOWS_AVAILABLE:
            return False

        try:
            # Verificar que la ventana todavía existe
            if not win32gui.IsWindow(dialog_hwnd):
                return False

            window_text = win32gui.GetWindowText(dialog_hwnd)
            self.logger.info(f"⚡ Intentando auto-confirmar: {window_text}")

            # Buscar botones de confirmación
            buttons_to_try = [
                "Allow", "Yes", "OK", "Accept", "Confirm", "Continue"
            ]

            def find_button_callback(hwnd, button_list):
                if win32gui.IsWindowVisible(hwnd):
                    button_text = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)

                    if class_name == "Button" and button_text in buttons_to_try:
                        button_list.append(hwnd)

                return True

            buttons = []
            win32gui.EnumChildWindows(dialog_hwnd, find_button_callback, buttons)

            # Intentar hacer clic en el primer botón encontrado
            if buttons:
                button_hwnd = buttons[0]
                button_text = win32gui.GetWindowText(button_hwnd)

                # Enviar click al botón
                win32gui.PostMessage(button_hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
                time.sleep(0.1)
                win32gui.PostMessage(button_hwnd, win32con.WM_LBUTTONUP, 0, 0)

                self.confirmation_count += 1
                self.logger.info(f"✅ Confirmación automática exitosa: {button_text}")

                # Integrar con Agent Optimizer si está disponible
                if self.agent_optimizer:
                    task_info = {
                        'type': 'confirmation',
                        'dialog': window_text,
                        'button': button_text,
                        'timestamp': datetime.now()
                    }
                    # Registrar la acción para optimización futura
                    asyncio.create_task(
                        self.agent_optimizer.log_task_completion(task_info)
                    )

                return True
            else:
                self.logger.warning(f"⚠️ No se encontraron botones en: {window_text}")
                return False

        except Exception as e:
            self.logger.error(f"❌ Error confirmando diálogo: {e}")
            return False

    def monitor_instances_status(self) -> Dict[str, str]:
        """Monitorear estado de instancias VS Code"""
        status = {}

        for instance_name, path in self.target_instances.items():
            is_running = False

            # Verificar si el proceso está ejecutándose
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    if proc.info['exe'] and path in proc.info['exe']:
                        is_running = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            status[instance_name] = "running" if is_running else "stopped"

        return status

    async def auto_response_cycle(self):
        """Ciclo principal de respuesta automática"""
        self.logger.info("🚀 Iniciando ciclo de respuesta automática")

        while self.auto_responses_enabled:
            try:
                # Buscar diálogos de Copilot
                dialogs = self.find_copilot_dialogs()

                if dialogs:
                    self.logger.info(f"📋 {len(dialogs)} diálogo(s) encontrado(s)")

                    for dialog in dialogs:
                        if self.auto_responses_enabled:
                            success = self.auto_confirm_dialog(dialog['hwnd'])
                            if success:
                                # Pausa breve después de confirmación exitosa
                                await asyncio.sleep(2)

                # Pausa entre verificaciones
                await asyncio.sleep(5)

            except Exception as e:
                self.logger.error(f"❌ Error en ciclo de respuesta: {e}")
                await asyncio.sleep(10)

        self.logger.info("🛑 Ciclo de respuesta automática detenido")

    async def monitoring_cycle(self):
        """Ciclo de monitoreo de instancias"""
        self.logger.info("📊 Iniciando monitoreo de instancias")

        while self.auto_responses_enabled:
            try:
                # Verificar estado de instancias
                status = self.monitor_instances_status()
                
                # Registrar cambios en estado
                for instance, state in status.items():
                    if instance not in self.active_windows or self.active_windows[instance] != state:
                        self.logger.info(f"📱 {instance}: {state}")
                        self.active_windows[instance] = state

                # Pausa entre verificaciones
                await asyncio.sleep(30)

            except Exception as e:
                self.logger.error(f"❌ Error en monitoreo: {e}")
                await asyncio.sleep(60)

        self.logger.info("🛑 Monitoreo de instancias detenido")

    async def status_report(self):
        """Generar reporte de estado"""
        vscode_windows = self.find_vscode_windows()
        instance_status = self.monitor_instances_status()

        report = {
            'timestamp': datetime.now().isoformat(),
            'confirmations_count': self.confirmation_count,
            'auto_responses_enabled': self.auto_responses_enabled,
            'vscode_windows': {k: len(v) for k, v in vscode_windows.items()},
            'instance_status': instance_status
        }

        self.logger.info(f"📊 Reporte: {json.dumps(report, indent=2)}")
        return report

    def toggle_auto_responses(self):
        """Alternar respuestas automáticas"""
        self.auto_responses_enabled = not self.auto_responses_enabled
        status = "activado" if self.auto_responses_enabled else "desactivado"
        self.logger.info(f"🔄 Auto-respuestas {status}")

    def initialize_agent_optimizer(self, whatsapp_notifier):
        """Inicializar Agent Optimizer integrado"""
        if AgentOptimizerSystem and whatsapp_notifier:
            self.agent_optimizer = AgentOptimizerSystem(whatsapp_notifier)
            self.logger.info("🤖 Agent Optimizer integrado al Orchestrator")

    async def run(self, whatsapp_notifier=None):
        """Ejecutar orchestrator principal"""
        self.logger.info("🎛️ VS Code Orchestrator iniciando...")

        # Inicializar Agent Optimizer si está disponible
        if whatsapp_notifier:
            self.initialize_agent_optimizer(whatsapp_notifier)

        # Reporte inicial
        await self.status_report()

        # Ejecutar ambos ciclos concurrentemente
        try:
            await asyncio.gather(
                self.auto_response_cycle(),
                self.monitoring_cycle()
            )
        except KeyboardInterrupt:
            self.logger.info("🛑 Deteniendo Orchestrator...")
            self.auto_responses_enabled = False

        self.logger.info("👋 Orchestrator detenido")

async def main():
    """Función principal del orchestrator"""
    print("🔧 VS Code Orchestrator")
    print("=" * 50)

    # Configurar WhatsApp si se desea
    whatsapp_notifier = None
    use_whatsapp = input("📱 ¿Usar notificaciones WhatsApp? (y/N): ").strip().lower() == 'y'
    
    if use_whatsapp:
        from roadmap_intelligence import WhatsAppNotifier
        whatsapp_notifier = WhatsAppNotifier()

    orchestrator = VSCodeOrchestrator()
    await orchestrator.run(whatsapp_notifier)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Orquestador detenido")
