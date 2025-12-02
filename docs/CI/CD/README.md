# Documentación CI/CD - Backend

Bienvenido a la documentación del pipeline de CI/CD para el backend del proyecto Web_guardia.

## 📚 Documentos Disponibles

### 1. [Guía de Implementación Completa](./guia-implementacion-cicd.md)
**Descripción**: Guía detallada paso a paso sobre cómo implementar y entender el pipeline de CI/CD.

**Contenido**:
- Introducción a CI/CD
- Explicación detallada del workflow
- Cómo ejecutar tests localmente
- Troubleshooting
- Mejores prácticas
- Próximos pasos

**Ideal para**: Desarrolladores que quieren entender a fondo el sistema.

---

### 2. [Resumen Ejecutivo](./resumen-ejecutivo.md)
**Descripción**: Referencia rápida con comandos y verificaciones esenciales.

**Contenido**:
- Comandos rápidos
- Checklist de implementación
- Troubleshooting rápido
- Links útiles

**Ideal para**: Consulta rápida durante el desarrollo.

---

### 3. [Configuración de Branch Protection](./configuracion-branch-protection.md)
**Descripción**: Guía completa para configurar reglas de protección de rama en GitHub.

**Contenido**:
- Paso a paso de configuración
- Reglas recomendadas
- Casos especiales
- Mejores prácticas

**Ideal para**: Administradores del repositorio.

---

## 🚀 Inicio Rápido

### Para Desarrolladores

1. **Ejecutar tests localmente**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m pytest app/test/ -v
```

2. **Crear un Pull Request**:
```powershell
git checkout -b feature/mi-feature
# Hacer cambios
git add .
git commit -m "feat: Mi nueva feature"
git push origin feature/mi-feature
```

3. **Verificar el workflow**: Ve a GitHub → Actions → Backend Tests

### Para Administradores

1. **Configurar branch protection**: Sigue la [guía de configuración](./configuracion-branch-protection.md)
2. **Monitorear workflows**: GitHub → Actions
3. **Revisar logs**: Clic en cualquier workflow para ver detalles

---

## 📊 Estado Actual

### Workflow Configurado
- ✅ **Nombre**: Backend Tests
- ✅ **Archivo**: `.github/workflows/backend-tests.yml`
- ✅ **Triggers**: PR a main, push a main, manual

### Tests Incluidos
- ✅ **Total**: 27 tests
- ✅ **Archivos**: 4 archivos de test
- ✅ **Cobertura**: ~95%

### Tiempo de Ejecución
- ⏱️ **Promedio**: 2-3 minutos
- ⚡ **Con caché**: ~1-2 minutos

---

## 🔗 Links Útiles

- [Workflow File](../../../.github/workflows/backend-tests.yml)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Pytest Docs](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

## 📞 Soporte

Si tienes problemas:

1. **Consulta la documentación**: Empieza con el [Resumen Ejecutivo](./resumen-ejecutivo.md)
2. **Revisa los logs**: GitHub → Actions → Workflow fallido → Logs
3. **Ejecuta localmente**: Verifica que los tests pasen en tu máquina
4. **Consulta troubleshooting**: Sección en la [Guía Completa](./guia-implementacion-cicd.md#troubleshooting)

---

## 🎯 Próximos Pasos Sugeridos

1. [ ] Configurar branch protection rules
2. [ ] Agregar linting (flake8, black)
3. [ ] Agregar type checking (mypy)
4. [ ] Agregar security scanning (bandit)
5. [ ] Agregar badge de estado al README principal
6. [ ] Configurar notificaciones (Slack/Discord)

---

*Última actualización: Diciembre 2024*  
*Versión: 1.0*

