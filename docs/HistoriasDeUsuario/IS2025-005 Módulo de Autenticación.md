# IS2025-005 Módulo de Autenticación

## Descripción

Como usuario del sistema
Quiero poder registrarme e iniciar sesión en el sistema
Para poder acceder a las actividades que me son otorgadas

## Notas

- Los datos del usuario son:
  - email: (string, mandatorio, debe respetar el formato de email)
  - contraseña (string, mandatorio, debe poseer un mínimo de 8 caracteres de largo)
  - la autoridad a la que está vinculada (médico, enfermera)

- La contraseña antes de quedar registrada debe ser **HASHEADA**, no **ENCRIPTADA**, preferentemente usar algoritmos como **ARGON2ID** o en su defecto **Bcrypt**. La justificación la dejo aquí:
  
  [Password Storage - OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

- Si durante el login, el usuario o contraseña son inválidos utilizar el mensaje de error `Usuario o contraseña inválidos`, **NUNCA** informar que un usuario no existe.

- Los siguientes usuarios pueden ver y ejecutar las siguientes historias de usuario:
  - Medico → IS2025-003 e IS2025-004
  - Enfermero → IS2025-001 e IS2025-002