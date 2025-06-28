#!/usr/bin/env python3
"""
Control Dashboard - Interfaz centralizada para AI Director + Orchestrator
Panel de control unificado para supervisar y controlar todo el sistema
"""

import asyncio
import json
import subprocess
import threading
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from typing import Dict, Any

# Importar sistemas integrados
try:
    from agent_optimizer_system import AgentOptimizerSystem
    from roadmap_intelligence import WhatsAppNotifier
    AGENT_OPTIMIZER_AVAILABLE = True
except ImportError:
    AGENT_OPTIMIZER_AVAILABLE = False

class ControlDashboard:
    """
    Dashboard centralizado para controlar AI Director y Orchestrator
    """

    def __init__(self):
        self.root = Tk()
        self.setup_ui()

        # Estado del sistema
        self.ai_director_running = False
        self.orchestrator_running = False
        self.roadmap_creator_running = False
        self.agent_optimizer_enabled = False
        self.system_status = {}
        self.last_update = None

        # Procesos
        self.ai_director_process = None
        self.orchestrator_process = None
        self.roadmap_creator_process = None

        # Agent Optimizer integrado
        self.agent_optimizer = None
        if AGENT_OPTIMIZER_AVAILABLE:
            self.whatsapp_notifier = WhatsAppNotifier()
            self.agent_optimizer = AgentOptimizerSystem(self.whatsapp_notifier)

        # Auto-refresh
        self.auto_refresh = True
        self.refresh_interval = 5  # segundos

    def setup_ui(self):
        """Configurar interfaz de usuario"""
        self.root.title("🧠 AI Director + Orchestrator Control Panel")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Status.TLabel', font=('Arial', 10))

        self.create_header()
        self.create_control_panel()
        self.create_status_panel()
        self.create_instances_panel()
        self.create_logs_panel()
        self.create_footer()

    def create_header(self):
        """Crear header principal"""
        header_frame = Frame(self.root, bg='#1e1e1e', height=80)
        header_frame.pack(fill=X, padx=10, pady=5)

        title_label = Label(
            header_frame,
            text="🧠 AI DIRECTOR + ORCHESTRATOR + AGENT OPTIMIZER",
            font=('Arial', 18, 'bold'),
            fg='#00ff88',
            bg='#1e1e1e'
        )
        title_label.pack(pady=10)

        subtitle_label = Label(
            header_frame,
            text="Sistema de gestión inteligente para múltiples VS Code instances",
            font=('Arial', 10),
            fg='#888888',
            bg='#1e1e1e'
        )
        subtitle_label.pack()

    def create_control_panel(self):
        """Panel de control principal"""
        control_frame = LabelFrame(
            self.root,
            text="🎛️ CONTROL PANEL",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        control_frame.pack(fill=X, padx=10, pady=5)

        # Botones principales
        buttons_frame = Frame(control_frame, bg='#2b2b2b')
        buttons_frame.pack(fill=X, padx=10, pady=10)

        # AI Director controls
        director_frame = Frame(buttons_frame, bg='#2b2b2b')
        director_frame.pack(side=LEFT, fill=X, expand=True)

        Label(director_frame, text="AI Director", font=('Arial', 10, 'bold'),
              fg='#00ff88', bg='#2b2b2b').pack()

        self.director_status_label = Label(
            director_frame, text="⭕ Stopped",
            fg='#ff4444', bg='#2b2b2b'
        )
        self.director_status_label.pack()

        self.start_director_btn = Button(
            director_frame,
            text="🚀 Start AI Director",
            command=self.start_ai_director,
            bg='#00aa44',
            fg='white',
            font=('Arial', 9, 'bold')
        )
        self.start_director_btn.pack(pady=2)

        self.stop_director_btn = Button(
            director_frame,
            text="⏹️ Stop AI Director",
            command=self.stop_ai_director,
            bg='#aa4400',
            fg='white',
            font=('Arial', 9, 'bold'),
            state=DISABLED
        )
        self.stop_director_btn.pack(pady=2)

        # Orchestrator controls
        orch_frame = Frame(buttons_frame, bg='#2b2b2b')
        orch_frame.pack(side=LEFT, fill=X, expand=True)

        Label(orch_frame, text="Orchestrator", font=('Arial', 10, 'bold'),
              fg='#0088ff', bg='#2b2b2b').pack()

        self.orch_status_label = Label(
            orch_frame, text="⭕ Stopped",
            fg='#ff4444', bg='#2b2b2b'
        )
        self.orch_status_label.pack()

        self.start_orch_btn = Button(
            orch_frame,
            text="🚀 Start Orchestrator",
            command=self.start_orchestrator,
            bg='#0066aa',
            fg='white',
            font=('Arial', 9, 'bold')
        )
        self.start_orch_btn.pack(pady=2)

        self.stop_orch_btn = Button(
            orch_frame,
            text="⏹️ Stop Orchestrator",
            command=self.stop_orchestrator,
            bg='#aa4400',
            fg='white',
            font=('Arial', 9, 'bold'),
            state=DISABLED
        )
        self.stop_orch_btn.pack(pady=2)

        # Agent Optimizer controls
        optimizer_frame = Frame(buttons_frame, bg='#2b2b2b')
        optimizer_frame.pack(side=LEFT, fill=X, expand=True)

        Label(optimizer_frame, text="Agent Optimizer", font=('Arial', 10, 'bold'),
              fg='#ff8800', bg='#2b2b2b').pack()

        self.optimizer_status_label = Label(
            optimizer_frame,
            text="🟢 Ready" if AGENT_OPTIMIZER_AVAILABLE else "❌ Not Available",
            fg='#00ff88' if AGENT_OPTIMIZER_AVAILABLE else '#ff4444',
            bg='#2b2b2b'
        )
        self.optimizer_status_label.pack()

        if AGENT_OPTIMIZER_AVAILABLE:
            self.optimizer_toggle_btn = Button(
                optimizer_frame,
                text="🤖 Enable Optimization",
                command=self.toggle_agent_optimizer,
                bg='#ff8800',
                fg='white',
                font=('Arial', 9, 'bold')
            )
            self.optimizer_toggle_btn.pack(pady=2)

        # Controles generales
        general_frame = Frame(buttons_frame, bg='#2b2b2b')
        general_frame.pack(side=LEFT, fill=X, expand=True)

        Label(general_frame, text="General", font=('Arial', 10, 'bold'),
              fg='#ffaa00', bg='#2b2b2b').pack()

        Button(
            general_frame,
            text="🚀 Start All",
            command=self.start_all,
            bg='#008844',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=2)

        Button(
            general_frame,
            text="⏹️ Stop All",
            command=self.stop_all,
            bg='#884400',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=2)

        Button(
            general_frame,
            text="🔄 Refresh",
            command=self.refresh_status,
            bg='#444444',
            fg='white',
            font=('Arial', 9, 'bold')
        ).pack(pady=2)

    def create_status_panel(self):
        """Panel de estado del sistema"""
        status_frame = LabelFrame(
            self.root,
            text="📊 SYSTEM STATUS",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        status_frame.pack(fill=X, padx=10, pady=5)

        # Métricas en tiempo real
        metrics_frame = Frame(status_frame, bg='#2b2b2b')
        metrics_frame.pack(fill=X, padx=10, pady=10)

        # Auto confirmations
        self.confirmations_label = Label(
            metrics_frame,
            text="✅ Confirmations: 0",
            font=('Arial', 10, 'bold'),
            fg='#00ff88',
            bg='#2b2b2b'
        )
        self.confirmations_label.pack(side=LEFT, padx=20)

        # Decisions made
        self.decisions_label = Label(
            metrics_frame,
            text="🧠 AI Decisions: 0",
            font=('Arial', 10, 'bold'),
            fg='#0088ff',
            bg='#2b2b2b'
        )
        self.decisions_label.pack(side=LEFT, padx=20)

        # Agent optimization
        self.optimization_label = Label(
            metrics_frame,
            text="🤖 Agent Optimizations: 0",
            font=('Arial', 10, 'bold'),
            fg='#ff8800',
            bg='#2b2b2b'
        )
        self.optimization_label.pack(side=LEFT, padx=20)

        # Last update
        self.update_label = Label(
            metrics_frame,
            text="🕐 Last Update: Never",
            font=('Arial', 10),
            fg='#888888',
            bg='#2b2b2b'
        )
        self.update_label.pack(side=RIGHT, padx=20)

    def create_instances_panel(self):
        """Panel de instancias VS Code"""
        instances_frame = LabelFrame(
            self.root,
            text="🖥️ VS CODE INSTANCES",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        instances_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Tabla de instancias
        columns = ('Instance', 'Status', 'Priority', 'Commits Today', 'Issues', 'PRs', 'Agent', 'Token Usage')
        self.instances_tree = ttk.Treeview(instances_frame, columns=columns, show='headings')

        for col in columns:
            self.instances_tree.heading(col, text=col)
            self.instances_tree.column(col, width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(instances_frame, orient=VERTICAL, command=self.instances_tree.yview)
        self.instances_tree.configure(yscrollcommand=scrollbar.set)

        self.instances_tree.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=RIGHT, fill=Y, pady=10)

        # Datos iniciales
        self.update_instances_display()

    def create_logs_panel(self):
        """Panel de logs"""
        logs_frame = LabelFrame(
            self.root,
            text="📋 ACTIVITY LOGS",
            font=('Arial', 12, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        logs_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Text area para logs
        self.logs_text = Text(
            logs_frame,
            height=10,
            bg='#1e1e1e',
            fg='#ffffff',
            font=('Consolas', 9),
            wrap=WORD
        )

        logs_scrollbar = Scrollbar(logs_frame, orient=VERTICAL, command=self.logs_text.yview)
        self.logs_text.configure(yscrollcommand=logs_scrollbar.set)

        self.logs_text.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        logs_scrollbar.pack(side=RIGHT, fill=Y, pady=10)

        self.log_message("🚀 Dashboard iniciado - Listo para supervisar")

    def create_footer(self):
        """Footer con información adicional"""
        footer_frame = Frame(self.root, bg='#1e1e1e', height=30)
        footer_frame.pack(fill=X, padx=10, pady=5)

        status_label = Label(
            footer_frame,
            text="Sistema de Control AI Director + Orchestrator + Agent Optimizer v1.0",
            font=('Arial', 8),
            fg='#666666',
            bg='#1e1e1e'
        )
        status_label.pack(side=LEFT, pady=5)

        # Toggle auto-refresh
        self.auto_refresh_var = BooleanVar(value=True)
        auto_refresh_check = Checkbutton(
            footer_frame,
            text="Auto-refresh",
            variable=self.auto_refresh_var,
            command=self.toggle_auto_refresh,
            fg='#666666',
            bg='#1e1e1e',
            selectcolor='#2b2b2b'
        )
        auto_refresh_check.pack(side=RIGHT, pady=5)

    def start_ai_director(self):
        """Iniciar AI Director"""
        try:
            import sys
            import os

            # Construir comando con path completo de Python
            python_exe = sys.executable
            script_path = os.path.join(os.path.dirname(__file__), "ai_director_system.py")

            # Verificar que el script existe
            if not os.path.exists(script_path):
                messagebox.showerror("Error", f"Script no encontrado: {script_path}")
                return

            self.ai_director_process = subprocess.Popen([
                python_exe, script_path
            ], creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0)

            self.ai_director_running = True
            self.director_status_label.config(text="🟢 Running", fg='#00ff88')
            self.start_director_btn.config(state=DISABLED)
            self.stop_director_btn.config(state=NORMAL)

            self.log_message("🧠 AI Director iniciado")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar AI Director: {e}")
            self.log_message(f"❌ Error iniciando AI Director: {e}")

    def stop_ai_director(self):
        """Detener AI Director"""
        try:
            if self.ai_director_process:
                self.ai_director_process.terminate()
                self.ai_director_process = None

            self.ai_director_running = False
            self.director_status_label.config(text="⭕ Stopped", fg='#ff4444')
            self.start_director_btn.config(state=NORMAL)
            self.stop_director_btn.config(state=DISABLED)

            self.log_message("🛑 AI Director detenido")

        except Exception as e:
            self.log_message(f"❌ Error deteniendo AI Director: {e}")

    def start_orchestrator(self):
        """Iniciar Orchestrator"""
        try:
            import sys
            import os

            python_exe = sys.executable
            script_path = os.path.join(os.path.dirname(__file__), "vscode_orchestrator.py")

            if not os.path.exists(script_path):
                messagebox.showerror("Error", f"Script no encontrado: {script_path}")
                return

            self.orchestrator_process = subprocess.Popen([
                python_exe, script_path
            ], creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0)

            self.orchestrator_running = True
            self.orch_status_label.config(text="🟢 Running", fg='#00ff88')
            self.start_orch_btn.config(state=DISABLED)
            self.stop_orch_btn.config(state=NORMAL)

            self.log_message("🔧 Orchestrator iniciado")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar Orchestrator: {e}")
            self.log_message(f"❌ Error iniciando Orchestrator: {e}")

    def stop_orchestrator(self):
        """Detener Orchestrator"""
        try:
            if self.orchestrator_process:
                self.orchestrator_process.terminate()
                self.orchestrator_process = None

            self.orchestrator_running = False
            self.orch_status_label.config(text="⭕ Stopped", fg='#ff4444')
            self.start_orch_btn.config(state=NORMAL)
            self.stop_orch_btn.config(state=DISABLED)

            self.log_message("🛑 Orchestrator detenido")

        except Exception as e:
            self.log_message(f"❌ Error deteniendo Orchestrator: {e}")

    def start_all(self):
        """Iniciar todos los sistemas"""
        self.log_message("🚀 Iniciando todos los sistemas...")
        self.start_ai_director()
        time.sleep(1)
        self.start_orchestrator()

    def toggle_agent_optimizer(self):
        """Toggle Agent Optimizer"""
        if AGENT_OPTIMIZER_AVAILABLE and self.agent_optimizer:
            self.agent_optimizer_enabled = not self.agent_optimizer_enabled

            if self.agent_optimizer_enabled:
                self.optimizer_status_label.config(text="🟢 Active", fg='#00ff88')
                self.optimizer_toggle_btn.config(text="🛑 Disable Optimization")
                self.log_message("🤖 Agent Optimizer activado")
            else:
                self.optimizer_status_label.config(text="⭕ Inactive", fg='#ffaa00')
                self.optimizer_toggle_btn.config(text="🤖 Enable Optimization")
                self.log_message("🛑 Agent Optimizer desactivado")

    def stop_all(self):
        """Detener todos los sistemas"""
        self.log_message("🛑 Deteniendo todos los sistemas...")
        self.stop_ai_director()
        self.stop_orchestrator()

    def toggle_auto_refresh(self):
        """Toggle auto-refresh"""
        self.auto_refresh = self.auto_refresh_var.get()
        status = "activado" if self.auto_refresh else "desactivado"
        self.log_message(f"🔄 Auto-refresh {status}")

    def refresh_status(self):
        """Actualizar estado del sistema"""
        self.last_update = datetime.now()
        self.update_label.config(text=f"🕐 Last Update: {self.last_update.strftime('%H:%M:%S')}")

        # Simular actualización de métricas
        self.confirmations_label.config(text="✅ Confirmations: 127")
        self.decisions_label.config(text="🧠 AI Decisions: 8")
        self.optimization_label.config(text="🤖 Agent Optimizations: 15")

        self.update_instances_display()
        self.log_message("🔄 Estado actualizado")

    def update_instances_display(self):
        """Actualizar display de instancias"""
        # Limpiar tabla
        for item in self.instances_tree.get_children():
            self.instances_tree.delete(item)

        # Datos de ejemplo con Agent Optimizer info
        instances_data = [
            ("VS_lim1712", "🟢 Running", "1", "12", "3", "1", "Claude-Haiku", "67%"),
            ("VS_helper_Two", "🟢 Running", "2", "7", "1", "2", "Claude-Sonnet", "23%"),
            ("VSCode_Lim", "🔴 Stopped", "3", "0", "2", "0", "N/A", "N/A")
        ]

        for data in instances_data:
            self.instances_tree.insert('', 'end', values=data)

    def log_message(self, message: str):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"

        self.logs_text.insert(END, log_entry)
        self.logs_text.see(END)

        # Limitar logs a 100 líneas
        if int(self.logs_text.index('end-1c').split('.')[0]) > 100:
            self.logs_text.delete('1.0', '10.0')

    def auto_refresh_loop(self):
        """Loop de auto-refresh"""
        while True:
            if self.auto_refresh:
                self.root.after(0, self.refresh_status)
            time.sleep(self.refresh_interval)

    def on_closing(self):
        """Manejar cierre de la aplicación"""
        try:
            # Detener todos los procesos
            self.stop_all()

            # Esperar un momento
            time.sleep(1)

            # Cerrar aplicación
            self.root.destroy()

        except Exception as e:
            print(f"Error cerrando aplicación: {e}")
            self.root.destroy()

    def run(self):
        """Ejecutar dashboard"""
        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Iniciar auto-refresh en thread separado
        refresh_thread = threading.Thread(target=self.auto_refresh_loop, daemon=True)
        refresh_thread.start()

        # Mensaje inicial
        self.log_message("🎛️ Control Dashboard listo")
        self.log_message("💡 Use los botones para controlar AI Director y Orchestrator")

        if AGENT_OPTIMIZER_AVAILABLE:
            self.log_message("🤖 Agent Optimizer disponible")
        else:
            self.log_message("⚠️ Agent Optimizer no disponible - instalar dependencias")

        # Iniciar GUI
        self.root.mainloop()

# Función principal
def main():
    try:
        dashboard = ControlDashboard()
        dashboard.run()
    except Exception as e:
        print(f"❌ Error ejecutando dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
