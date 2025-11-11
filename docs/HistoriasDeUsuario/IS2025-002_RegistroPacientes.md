# Historia de Usuario: IS2025-002 - Registro de pacientes

## Descripción
**Como** enfermera,  
**Quiero** registrar pacientes,  
**Para** poder realizar el ingreso a urgencias o buscarlos durante un ingreso en caso de que el paciente aparezca en urgencia más de una vez.

## Notas
- La enfermera es la que da de alta los pacientes
- Los datos del paciente son:
  - **Cuil** (mandatorio, tiene que respetar el formato de CUIT)
  - **Apellido** (mandatorio, string)
  - **Nombre** (mandatorio, string)
  - **Domicilio** (mandatorio, objeto)
    - Calle (mandatorio, string)
    - Numero (mandatorio, int)
    - Localidad (mandatorio, string)
      > *Se que puede ser un objeto la localidad (como asi tambien provincia y pais) pero vamos a limitar el alcance a un simple string y suponer que todos los que van a entrar a urgencias son de Tucumán, sino se hace mas largo el TFI y realmente no es el core de nuestro sistema*
  - **Obra social** (objeto, opcional) : AFILIADO
    - Obra social (objeto mandatorio): OBRA SOCIAL
    - numeroAfiliado (string mandatorio)
      > *Notese que hay dos objetos de tipo obra social, el primero representa la afiliación del paciente a la obra social, el segundo representa la obra social propiamente dicha.*

- Cuando se crea el paciente, se debe validar que la obra social exista y que el usuario esté afiliado a la obra social.

## Criterios de Aceptación

1. **Escenario**: Registro con datos mandatorios y obra social existente  
   **Dado** que se ingresan todos los datos mandatorios  
   **Y** se incluye una obra social existente  
   **Cuando** se intenta registrar al paciente  
   **Entonces** la creación es exitosa

2. **Escenario**: Registro con datos mandatorios sin obra social  
   **Dado** que se ingresan todos los datos mandatorios  
   **Y** no se incluye obra social  
   **Cuando** se intenta registrar al paciente  
   **Entonces** la creación es exitosa

3. **Escenario**: Registro con obra social inexistente  
   **Dado** que se ingresan todos los datos mandatorios  
   **Y** se incluye una obra social que no existe en el sistema  
   **Cuando** se intenta registrar al paciente  
   **Entonces** se envía un mensaje de error notificando que no se puede registrar al paciente con una obra social inexistente

4. **Escenario**: Registro con obra social a la que no está afiliado  
   **Dado** que se ingresan todos los datos mandatorios  
   **Y** se incluye una obra social existente a la cual el paciente no está afiliado  
   **Cuando** se intenta registrar al paciente  
   **Entonces** se envía un mensaje de error notificando que no se puede registrar el paciente dado que no está afiliado a la obra social

5. **Escenario**: Registro con datos mandatorios omitidos  
   **Dado** que se omite algún dato mandatorio  
   **Cuando** se intenta registrar al paciente  
   **Entonces** se envía un mensaje de error notificando el campo específico que se omitió durante el registro
