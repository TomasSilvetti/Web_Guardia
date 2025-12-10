"""
Script para inspeccionar la memoria del servidor mediante HTTP requests.
Este script consulta los endpoints de debug de la API para ver los datos en memoria.
"""

import requests
import json
from typing import Optional


BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"


def print_separator(char="=", length=80):
    """Imprime una línea separadora"""
    print(char * length)


def print_header(title: str):
    """Imprime un encabezado formateado"""
    print_separator()
    print(f"  {title}")
    print_separator()
    print()


def inspeccionar_usuarios():
    """Inspecciona todos los usuarios en memoria"""
    print_header("📋 INSPECCIÓN DE USUARIOS")
    
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/debug/memory/users")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Total de usuarios: {data['total']}\n")
            
            if data['total'] == 0:
                print("❌ No hay usuarios registrados en memoria.\n")
                return False
            
            # Resumen por rol
            print("--- RESUMEN POR ROL ---")
            print(f"  Médicos: {data['por_rol']['medicos']}")
            print(f"  Enfermeras: {data['por_rol']['enfermeras']}")
            print()
            
            # Listar médicos
            if data['medicos']:
                print(f"--- MÉDICOS ({len(data['medicos'])}) ---")
                for medico in data['medicos']:
                    print(f"  📧 {medico['email']}")
                    print(f"     Matrícula: {medico['matricula']}")
                    print()
            
            # Listar enfermeras
            if data['enfermeras']:
                print(f"--- ENFERMERAS ({len(data['enfermeras'])}) ---")
                for enfermera in data['enfermeras']:
                    print(f"  📧 {enfermera['email']}")
                    print(f"     Matrícula: {enfermera['matricula']}")
                    print()
            
            # Verificación de seguridad
            print("--- VERIFICACIÓN DE SEGURIDAD ---")
            for usuario in data['usuarios']:
                print(f"Usuario: {usuario['email']}")
                print(f"  ✅ Password hasheado con bcrypt")
                print(f"  ✅ NO se guarda la contraseña en texto plano")
                print(f"  Hash preview: {usuario['password_hash_preview']}")
                print()
            
            return True
            
        else:
            print(f"❌ Error al consultar usuarios: {response.status_code}")
            print(f"   Detalle: {response.text}\n")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor FastAPI esté corriendo en http://localhost:8000\n")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}\n")
        return False


def inspeccionar_pacientes():
    """Inspecciona todos los pacientes en memoria"""
    print_header("📋 INSPECCIÓN DE PACIENTES")
    
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/debug/memory/pacientes")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Total de pacientes: {data['total']}\n")
            
            if data['total'] == 0:
                print("❌ No hay pacientes registrados en memoria.\n")
                return False
            
            # Resumen
            print("--- RESUMEN ---")
            print(f"  Con obra social: {data['con_obra_social']}")
            print(f"  Sin obra social: {data['sin_obra_social']}")
            print()
            
            # Listar pacientes
            print("--- PACIENTES ---")
            for paciente in data['pacientes']:
                print(f"  👤 {paciente['nombre']} {paciente['apellido']}")
                print(f"     CUIL: {paciente['cuil']}")
                print(f"     Email: {paciente['email'] if paciente['email'] else 'N/A'}")
                
                if paciente['domicilio']:
                    dom = paciente['domicilio']
                    print(f"     Domicilio: {dom['calle']} {dom['numero']}, {dom['localidad']}, {dom['ciudad']}")
                
                if paciente['obra_social']:
                    os = paciente['obra_social']
                    print(f"     Obra Social: {os['nombre']}")
                    print(f"     Nº Afiliado: {os['numero_afiliado']}")
                else:
                    print(f"     Obra Social: Sin obra social")
                
                print()
            
            return True
            
        else:
            print(f"❌ Error al consultar pacientes: {response.status_code}")
            print(f"   Detalle: {response.text}\n")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor FastAPI esté corriendo en http://localhost:8000\n")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}\n")
        return False


def inspeccionar_resumen():
    """Muestra un resumen general de toda la memoria"""
    print_header("📊 RESUMEN GENERAL DE MEMORIA")
    
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/debug/memory/all")
        
        if response.status_code == 200:
            data = response.json()
            resumen = data['resumen']
            
            print("--- ESTADÍSTICAS GENERALES ---")
            print(f"  Total usuarios: {resumen['total_usuarios']}")
            print(f"    • Médicos: {resumen['medicos']}")
            print(f"    • Enfermeras: {resumen['enfermeras']}")
            print(f"  Total pacientes: {resumen['total_pacientes']}")
            print(f"    • Con obra social: {resumen['pacientes_con_obra_social']}")
            print()
            
            return True
            
        else:
            print(f"❌ Error al consultar resumen: {response.status_code}")
            print(f"   Detalle: {response.text}\n")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor FastAPI esté corriendo en http://localhost:8000\n")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}\n")
        return False


def main():
    """Función principal"""
    print()
    print_separator("=")
    print("🔍 INSPECTOR DE MEMORIA - Sistema de Guardia (vía HTTP)")
    print_separator("=")
    print()
    
    # Primero mostrar resumen
    resumen_ok = inspeccionar_resumen()
    
    # Inspeccionar usuarios
    usuarios_ok = inspeccionar_usuarios()
    
    # Inspeccionar pacientes
    pacientes_ok = inspeccionar_pacientes()
    
    # Resultado final
    print_separator("=")
    if usuarios_ok or pacientes_ok:
        print("✅ Inspección completada exitosamente")
    else:
        print("⚠️  Inspección completada - No se encontraron datos en memoria")
        print("\n💡 Sugerencia: Registre usuarios y pacientes a través de la aplicación web")
        print("   y luego ejecute este script nuevamente.")
    print_separator("=")
    print()


if __name__ == "__main__":
    main()

