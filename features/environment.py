"""
Behave environment configuration file.
Este archivo define hooks que se ejecutan en diferentes momentos del ciclo de vida de las pruebas.
"""
from behave import fixture, use_fixture


def before_scenario(context, scenario):
    """
    Hook que se ejecuta antes de cada escenario.
    Reinicializa las variables globales para asegurar que cada escenario comience con estado limpio.
    """
    import features.steps.modulo_urgencias_steps as steps_module

    # Reinicializar todas las variables globales del módulo de steps
    steps_module.enfermera = None
    steps_module.db_mockeada = None
    steps_module.servicio_urgencias = None
    steps_module.excepcion_esperada = None
    steps_module.mensaje_advertencia = None
    steps_module.datos_paciente_nuevo = None
