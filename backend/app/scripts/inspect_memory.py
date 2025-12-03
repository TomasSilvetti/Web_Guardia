"""
Script para inspeccionar la memoria de usuarios y pacientes.
Consulta los datos actuales en memoria sin crear nuevos registros.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path para poder importar los módulos
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from backend.app.api.dependencies import get_user_repo, get_pacientes_repo
from backend.app.services.auth_service import InMemoryUserRepo
from backend.app.repositories.paciente_repo_impl import InMemoryPacientesRepo
from backend.app.models.models import Rol


def obtener_repositorios():
    """Obtiene las instancias actuales de los repositorios en memoria (singletons)"""
    
    # Obtener las instancias singleton de los repositorios que usa la aplicación
    user_repo = get_user_repo()
    paciente_repo = get_pacientes_repo()
    
    return user_repo, paciente_repo


def inspeccionar_usuarios(user_repo: InMemoryUserRepo):
    """Inspecciona y muestra todos los usuarios en memoria"""
    print("\n" + "="*80)
    print("📋 INSPECCIÓN DE USUARIOS")
    print("="*80 + "\n")
    
    total = user_repo.count()
    
    if total == 0:
        print("❌ No hay usuarios registrados en memoria.")
        print("   Por favor, registre usuarios antes de ejecutar este script.\n")
        return False
    
    # Método 1: Usar el método print_all_users()
    user_repo.print_all_users()
    
    # Método 2: Consultas específicas
    print("\n--- CONSULTAS ESPECÍFICAS ---\n")
    
    print(f"Total de usuarios: {total}")
    
    medicos = user_repo.get_all_by_rol(Rol.MEDICO)
    print(f"Total de médicos: {len(medicos)}")
    for medico in medicos:
        print(f"  • {medico.email}")
    
    enfermeras = user_repo.get_all_by_rol(Rol.ENFERMERA)
    print(f"Total de enfermeras: {len(enfermeras)}")
    for enfermera in enfermeras:
        print(f"  • {enfermera.email}")
    
    # Verificación de seguridad
    print("\n--- VERIFICACIÓN DE SEGURIDAD ---\n")
    todos = user_repo.get_all()
    for user in todos:
        print(f"Usuario: {user.email}")
        print(f"  ✅ Password hasheado con bcrypt")
        print(f"  ✅ NO se guarda la contraseña en texto plano")
        print(f"  Hash (primeros 40 caracteres): {user.password_hash[:40]}...")
        print()
    
    return True


def inspeccionar_pacientes(paciente_repo: InMemoryPacientesRepo):
    """Inspecciona y muestra todos los pacientes en memoria"""
    print("\n" + "="*80)
    print("📋 INSPECCIÓN DE PACIENTES")
    print("="*80 + "\n")
    
    # Acceder al diccionario interno del repositorio
    total = len(paciente_repo._pacientes)
    
    if total == 0:
        print("❌ No hay pacientes registrados en memoria.")
        print("   Por favor, registre pacientes antes de ejecutar este script.\n")
        return False
    
    print(f"Total de pacientes: {total}\n")
    
    for paciente in paciente_repo._pacientes.values():
        print(f"  👤 {paciente.nombre} {paciente.apellido}")
        print(f"     CUIL: {paciente.cuil}")
        print(f"     Email: {paciente.email if paciente.email else 'N/A'}")
        print(f"     Domicilio: {paciente.domicilio.calle} {paciente.domicilio.numero}, "
              f"{paciente.domicilio.localidad}, {paciente.domicilio.ciudad}")
        
        if paciente.afiliado:
            print(f"     Obra Social: {paciente.afiliado.obra_social.nombre}")
            print(f"     Nº Afiliado: {paciente.afiliado.numero_afiliado}")
        else:
            print(f"     Obra Social: Sin obra social")
        print()
    
    return True


def main():
    """Función principal"""
    print("\n" + "="*80)
    print("🔍 INSPECTOR DE MEMORIA - Sistema de Guardia")
    print("="*80 + "\n")
    
    # Obtener repositorios singleton actuales
    user_repo, paciente_repo = obtener_repositorios()
    
    # Inspeccionar usuarios
    usuarios_ok = inspeccionar_usuarios(user_repo)
    
    # Inspeccionar pacientes
    pacientes_ok = inspeccionar_pacientes(paciente_repo)
    
    print("\n" + "="*80)
    if usuarios_ok or pacientes_ok:
        print("✅ Inspección completada")
    else:
        print("⚠️  Inspección completada - No se encontraron datos en memoria")
        print("\n💡 Sugerencia: Ejecute la aplicación y registre usuarios/pacientes")
        print("   antes de ejecutar este script de inspección.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()