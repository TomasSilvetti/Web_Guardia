Feature: Modulo de Urgencias
    Esta feature esta relacionada al registro de ingresos de pacientes en la sala de urgencias
    respetando su nivel de prioridad y el horario de llegada.

    Background:
        Given que la siguiente enfermera esta registrada:
            | Nombre | Apellido |
            | Susana | Gimenez  |


    Scenario: Ingreso del primer paciente a la lista de espera de urgencias
        Given que estan registrados los siguientes pacientes:
            | Cuil         | Apellido | Nombre    | Obra Social       |
            | 23-1234567-9 | Nunez    | Marcelo   | Subsidio de Salud |
            | 27-4567890-3 | Dufour   | Alexandra | Swiss Medical     |
        When Ingresan a urgencias los siguientes pacientes:
            | Cuil         | Informe          | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 23-1234567-9 | Le agarro dengue | Emergencia          | 38          | 70                  | 15                      | 120/80           |
        Then La lista de espera esta ordenada por cuil de la siguiente manera:
            | Cuil         |
            | 23-1234567-9 |

    Scenario: Ingreso de un paciente de bajo nivel de emergencia y luego otro de alto nivel de emergencia
        Given que estan registrados los siguientes pacientes:
            | Cuil         | Apellido | Nombre    | Obra Social        |
            | 23-1234567-9 | Nunez    | Marcelo   | Subsidio de Salud  |
            | 27-4567890-3 | Dufour   | Alexandra | Swiss Medical      |
            | 23-4567899-2 | Estrella | Patricio  | Fondo de Bikini SA |
        When Ingresan a urgencias los siguientes pacientes:
            | Cuil         | Informe          | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 23-4567899-2 | Le duele el ojo  | Sin Urgencia        | 37          | 70                  | 15                      | 120/80           |
            | 23-1234567-9 | Le agarro dengue | Emergencia          | 38          | 70                  | 15                      | 120/80           |
        Then La lista de espera esta ordenada por cuil de la siguiente manera:
            | Cuil         |
            | 23-1234567-9 |
            | 23-4567899-2 |


    Scenario: Ingreso un paciente sin urgencia y dos con urgencia
        Given que estan registrados los siguientes pacientes:
            | Cuil         | Apellido | Nombre    | Obra Social        |
            | 23-1234567-9 | Nunez    | Marcelo   | Subsidio de Salud  |
            | 27-4567890-3 | Dufour   | Alexandra | Swiss Medical      |
            | 23-4567899-2 | Estrella | Patricio  | Fondo de Bikini SA |
        When Ingresan a urgencias los siguientes pacientes:
            | Cuil         | Informe             | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 27-4567890-3 | Le duele la pestana | Sin Urgencia        | 37          | 70                  | 15                      | 120/80           |
            | 23-4567899-2 | Le agarro neumonia  | Emergencia          | 37          | 70                  | 15                      | 120/80           |
            | 23-1234567-9 | Le agarro dengue    | Emergencia          | 38          | 70                  | 15                      | 120/80           |
        Then La lista de espera esta ordenada por cuil de la siguiente manera:
            | Cuil         |
            | 23-4567899-2 |
            | 23-1234567-9 |
            | 27-4567890-3 |

    Scenario: Registrar ingreso con valores negativos en Frecuencia Cardíaca
        Given que estan registrados los siguientes pacientes:
            | Cuil          | Apellido     | Nombre | Obra Social   |
            | 23-12345678-7 | Gomez Rivera | Pablo  | Swiss Medical |

        When Ingresan a urgencias los siguientes pacientes:
            | Cuil          | Informe             | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 23-12345678-7 | Le duele la pestana | Sin Urgencia        | 37          | -70                 | 15                      | 120/80           |

        Then el sistema muestra el siguiente error: "La Frecuencia Cardiaca no puede ser negativa"


    Scenario: Registrar ingreso con valores negativos en Frecuencia Respiratoria
        Given que estan registrados los siguientes pacientes:
            | Cuil          | Apellido     | Nombre | Obra Social   |
            | 23-12345678-7 | Gomez Rivera | Pablo  | Swiss Medical |

        When Ingresan a urgencias los siguientes pacientes:
            | Cuil          | Informe             | Nivel de Emergencia | Temperatura | Frecuencia Cardiaca | Frecuencia Respiratoria | Tension Arterial |
            | 23-12345678-7 | Le duele la pestana | Sin Urgencia        | 37          | 70                  | -15                     | 120/80           |

        Then el sistema muestra el siguiente error: "La Frecuencia Respiratoria no puede ser negativa"


