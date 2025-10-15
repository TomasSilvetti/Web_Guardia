Feature: Modulo de Urgencias
    Esta feature esta relacionada al registro de ingresos de pacientes en la sala de urgencias
    respetando su nivel de prioridad y el horario de llegada.

    Background:
        Given que la siguiente enfermera esta registrada:
            | Nombre | Apellido |
            | Maria  | Lopez    |


    Scenario: Ingreso de un paciente que existe en el sistema
        Given que estan registrados los siguientes pacientes:
            | Cuil          | Apellido | Nombre | Obra Social |
            | 20-12345678-9 | Gonzalez | Juan   | OSDE        |
        When Ingresan a urgencias los siguientes pacientes:
            | Cuil          | Informe                | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 20-12345678-9 | Dolor toracico intenso | Emergencia          | 37.5        | 95                  | 20                      | 140/90           |
        Then La lista de espera esta ordenada por cuil de la siguiente manera:
            | Cuil          |
            | 20-12345678-9 |
        And el ingreso del paciente con cuil "20-12345678-9" queda registrado con estado "PENDIENTE"

    Scenario: Ingreso de un paciente que no existe en el sistema
        Given que no hay pacientes registrados en el sistema
        When se intenta ingresar a urgencias el siguiente paciente:
            | Cuil          | Apellido | Nombre | Obra Social   | Informe                     | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 27-98765432-1 | Martinez | Sofia  | Swiss Medical | Fractura de brazo izquierdo | Urgencia            | 36.8        | 88                  | 18                      | 130/85           |
        Then se muestra un mensaje de error indicando que el paciente no existe y que se debe registrar antes de proceder al ingreso
        And el paciente con cuil "27-98765432-1" es creado en el sistema con los datos del ingreso
        And La lista de espera esta ordenada por cuil de la siguiente manera:
            | Cuil          |
            | 27-98765432-1 |
        And el ingreso del paciente con cuil "27-98765432-1" queda registrado con estado "PENDIENTE"

    Scenario: Registrar ingreso omitiendo dato mandatorio
        Given que estan registrados los siguientes pacientes:
            | Cuil          | Apellido | Nombre | Obra Social |
            | 20-12345678-9 | Gonzalez | Juan   | OSDE        |
        When Ingresan a urgencias los siguientes pacientes:
            | Cuil          | apellido | nombre  | obra social | Informe                     | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 20-12345678-8 | facion   | nicolas | OSDE        |                             | Emergencia          | 37.5        | 95                  | 20                      | 140/90           |
        Then el sistema muestra el siguiente error: "El campo informe es obligatorio"

    Scenario: Registrar ingreso con valores negativos en Frecuencia Cardiaca
        Given que estan registrados los siguientes pacientes:
            | Cuil          | Apellido | Nombre | Obra Social |
            | 20-12345678-9 | Gonzalez | Juan   | OSDE        |
        When Ingresan a urgencias los siguientes pacientes:
            | Cuil          | Informe                | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 20-12345678-9 | Dolor toracico intenso | Emergencia          | 37.5        | -95                 | 20                      | 140/90           |
        Then el sistema muestra el siguiente error: "La Frecuencia Cardiaca no puede ser negativa"

    Scenario: Registrar ingreso con valores negativos en Frecuencia Respiratoria
        Given que estan registrados los siguientes pacientes:
            | Cuil          | Apellido | Nombre | Obra Social |
            | 20-12345678-9 | Gonzalez | Juan   | OSDE        |
        When Ingresan a urgencias los siguientes pacientes:
            | Cuil          | Informe                | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 20-12345678-9 | Dolor toracico intenso | Emergencia          | 37.5        | 95                  | -20                     | 140/90           |
        Then el sistema muestra el siguiente error: "La Frecuencia Respiratoria no puede ser negativa"

    Scenario: Ingreso de un paciente con mayor prioridad que otro en espera
        Given que estan registrados los siguientes pacientes:
            | Cuil          | Apellido | Nombre    | Obra Social        |
            | 20-12345678-9 | Gonzalez | Juan      | OSDE               |
            | 27-98765432-1 | Martinez | Sofia     | Swiss Medical      |
        And que hay pacientes en espera:
            | Cuil          | Informe                     | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 20-12345678-9 | Dolor leve en el tobillo    | Urgencia Menor      | 36.5        | 75                  | 16                      | 120/80           |
        When Ingresan a urgencias los siguientes pacientes:
            | Cuil          | Informe                     | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 27-98765432-1 | Dolor toracico intenso      | Emergencia          | 37.8        | 110                 | 24                      | 150/95           |
        Then La lista de espera esta ordenada por cuil de la siguiente manera:
            | Cuil          |
            | 27-98765432-1 |
            | 20-12345678-9 |


    Scenario: Ingreso de paciente con menor nivel de emergencia que un paciente en espera
        Given que hay pacientes en espera:
            | Cuil          | Nombre | Apellido | Nivel de Emergencia | Informe            | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 20-12345678-9 | Juan   | Gonzalez | Urgencia            | Dolor leve tobillo | 36.5        | 75                  | 16                      | 120/80           |

        When se ingresa a urgencias el siguiente paciente:
            | Cuil          | Nombre | Apellido | Nivel de Emergencia | Informe        | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 27-98765432-1 | Sofia  | Martinez | Emergencia             | Dolor toracico | 36.5        | 80                  | 18                      | 120/80           |

        Then La lista de espera esta ordenada por prioridad de emergencia de la siguiente manera:
            | Cuil          |
            | 27-98765432-1 |
            | 20-12345678-9 |
        And el ingreso del paciente con cuil "27-98765432-1" queda registrado con estado "PENDIENTE"


    Scenario: Ingreso de paciente con mismo nivel de emergencia que un paciente que se encuentra en espera
        Given que hay pacientes en espera:
            | Cuil          | Nombre  | Apellido | Obra Social | Nivel de Emergencia | Informe            | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 20-12345678-9 | Juan    | Gonzalez | OSDE        | Emergencia         | Dificultad respiratoria aguda | 36.5        | 100                  | 12                      | 180/80           |
        When se ingresa a urgencias el siguiente paciente con el mismo nivel de emergencia:
            | Cuil          | Nombre  | Apellido | Obra Social    | Nivel de Emergencia | Informe        | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 27-98765432-1 | Sofia   | Martinez | Swiss Medical  | Emergencia         | Dolor toracico | 36.5        | 80                  | 18                      | 120/80           |
        Then La lista de espera queda ordenada por prioridad de llegada de la siguiente manera:
            | Cuil          |
            | 20-12345678-9 |
            | 27-98765432-1 |
        And el ingreso del paciente con cuil "27-98765432-1" queda registrado con estado "PENDIENTE"
