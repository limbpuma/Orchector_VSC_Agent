#!/usr/bin/env python3
"""
Script para verificar dependencias del AI Director System
"""

import sys

def check_dependency(module_name, install_name=None):
    """Verificar si una dependencia está disponible"""
    if install_name is None:
        install_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {module_name}: Instalado")
        return True
    except ImportError:
        print(f"❌ {module_name}: NO instalado - Necesitas: pip install {install_name}")
        return False

def main():
    print("🔍 VERIFICANDO DEPENDENCIAS DEL AI DIRECTOR SYSTEM")
    print("=" * 60)
    
    # Dependencias críticas (obligatorias)
    critical_deps = [
        ("asyncio", None),  # Incluido en Python estándar
        ("psutil", "psutil"),
        ("requests", "requests"),
        ("json", None),  # Incluido en Python estándar
        ("logging", None),  # Incluido en Python estándar
        ("tkinter", None),  # Incluido en Python estándar (en la mayoría de instalaciones)
    ]
    
    # Dependencias de Windows
    windows_deps = [
        ("win32api", "pywin32"),
        ("win32con", "pywin32"),
        ("win32gui", "pywin32"),
    ]
    
    # Dependencias opcionales
    optional_deps = [
        ("yaml", "pyyaml"),
        ("twilio", "twilio"),
        ("github", "PyGithub"),
        ("dotenv", "python-dotenv"),
        ("markdown", "markdown"),
        ("sklearn", "scikit-learn"),
        ("numpy", "numpy"),
    ]
    
    print("\n📋 DEPENDENCIAS CRÍTICAS:")
    critical_missing = 0
    for module, install in critical_deps:
        if not check_dependency(module, install):
            critical_missing += 1
    
    print(f"\n🖥️ DEPENDENCIAS DE WINDOWS:")
    windows_missing = 0
    for module, install in windows_deps:
        if not check_dependency(module, install):
            windows_missing += 1
    
    print(f"\n🔧 DEPENDENCIAS OPCIONALES:")
    optional_missing = 0
    for module, install in optional_deps:
        if not check_dependency(module, install):
            optional_missing += 1
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    
    if critical_missing == 0:
        print("✅ Todas las dependencias críticas están instaladas")
    else:
        print(f"❌ Faltan {critical_missing} dependencias críticas")
    
    if windows_missing == 0:
        print("✅ Dependencias de Windows OK")
    else:
        print(f"⚠️ Faltan {windows_missing} dependencias de Windows (pywin32)")
    
    print(f"📝 Dependencias opcionales faltantes: {optional_missing}")
    
    print("\n🚀 COMANDOS DE INSTALACIÓN:")
    print("pip install -r requirements.txt")
    
    if critical_missing > 0 or windows_missing > 0:
        print("\n❗ SISTEMA NO PUEDE EJECUTARSE - Instala las dependencias críticas primero")
        return False
    else:
        print("\n✅ SISTEMA LISTO PARA EJECUTAR")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
