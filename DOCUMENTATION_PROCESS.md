# DOCUMENTATION PROCESS - PreventIA News Analytics
*Proceso de documentación continua para mantener consistencia entre sesiones*

## FILOSOFÍA DE DOCUMENTACIÓN

**Principio:** Documentación viviente que evoluciona con el código  
**Objetivo:** Futuras instancias de Claude Code deben entender el proyecto inmediatamente  
**Método:** Actualización incremental después de cada sesión significativa

---

## ESTRUCTURA DE DOCUMENTACIÓN

### Documentos Core (OBLIGATORIOS)
1. **`CLAUDE.md`** - Guía principal para Claude Code
2. **`PROJECT_STATUS_ANALYSIS.md`** - Estado técnico actual del proyecto
3. **`SESSION_HANDOFF_TEMPLATE.md`** - Template para transferencia entre sesiones
4. **`MVP_ROADMAP.md`** - Ruta específica hacia MVP funcional

### Documentos de Apoyo (OPCIONALES)
- **`TECHNICAL_DECISIONS.md`** - Decisiones arquitecturales importantes
- **`KNOWN_ISSUES.md`** - Issues técnicos conocidos y workarounds
- **`DEPLOYMENT_GUIDE.md`** - Guía específica de deployment

---

## PROCESO DE ACTUALIZACIÓN

### Al Inicio de Cada Sesión
1. **Leer siempre:**
   - `CLAUDE.md` (contexto del proyecto)
   - `PROJECT_STATUS_ANALYSIS.md` (estado actual)
   - Último `SESSION_HANDOFF_*.md` (contexto inmediato)

2. **Verificar estado actual:**
   - Ejecutar health checks básicos
   - Verificar que el análisis previo sigue siendo válido
   - Identificar cambios desde última sesión

### Durante la Sesión
1. **Tracking de cambios importantes:**
   - Nuevas funcionalidades implementadas
   - Issues resueltos
   - Issues nuevos descubiertos
   - Decisiones técnicas tomadas

2. **Documentación en tiempo real:**
   - Comentarios en código para decisiones complejas
   - README updates para nuevos módulos
   - CLAUDE.md updates para comandos nuevos

### Al Final de Cada Sesión
1. **Actualización obligatoria:**
   - `PROJECT_STATUS_ANALYSIS.md` con nuevo estado
   - `CLAUDE.md` si hay comandos/procesos nuevos
   - Crear nuevo `SESSION_HANDOFF_YYYY-MM-DD.md`

2. **Git commit dedicado a documentación:**
   ```bash
   git add *.md
   git commit -m "docs: update project status and session handoff - YYYY-MM-DD"
   ```

---

## TEMPLATE DE ACTUALIZACIÓN

### Para PROJECT_STATUS_ANALYSIS.md
```markdown
## CAMBIOS EN ESTA SESIÓN [YYYY-MM-DD]

### Funcionalidades Implementadas
- [ ] Feature 1: Descripción y estado
- [ ] Feature 2: Descripción y estado

### Issues Resueltos
- ✅ Issue 1: Descripción de la solución
- ✅ Issue 2: Descripción de la solución

### Issues Nuevos Descubiertos
- ❌ Issue 1: Descripción y impacto
- ❌ Issue 2: Descripción y impacto

### Progreso hacia MVP
- **Estado anterior:** X% completo
- **Estado actual:** Y% completo
- **Próximos pasos críticos:** Lista de 3-5 items
```

### Para CLAUDE.md
```markdown
## ACTUALIZACIONES [YYYY-MM-DD]

### Nuevos Comandos
- `comando nuevo` - descripción de uso

### Cambios en Arquitectura
- Cambio 1: Razón y impacto
- Cambio 2: Razón y impacto

### Notas Importantes
- Nota crítica para futuras sesiones
```

---

## SESIÓN HANDOFF PROCESS

### Al Terminar una Sesión (OBLIGATORIO)
Crear archivo: `SESSION_HANDOFF_YYYY-MM-DD.md`

```markdown
# SESSION HANDOFF - [YYYY-MM-DD]

## CONTEXTO DE LA SESIÓN
**Objetivo principal:** [Lo que se quería lograr]
**Tiempo invertido:** [X horas]
**Estado al inicio:** [Breve descripción]

## TRABAJO REALIZADO

### ✅ Completado
1. Task 1 - Descripción específica
2. Task 2 - Descripción específica

### 🔄 En Progreso
1. Task 1 - Estado actual y próximos pasos
2. Task 2 - Estado actual y próximos pasos

### ❌ Bloqueado
1. Issue 1 - Descripción del bloqueo y posibles soluciones

## PRÓXIMA SESIÓN

### Prioridad Inmediata
1. Task más crítico
2. Segunda prioridad
3. Tercera prioridad

### Contexto Necesario
- Información importante que la próxima sesión debe saber
- Decisiones tomadas que afectan el trabajo futuro
- Files específicos que deben revisarse

### Comandos Útiles para Continuar
```bash
# Comando 1 para verificar estado
# Comando 2 para continuar trabajo
```

## NOTAS TÉCNICAS

### Issues Críticos
- Issue 1: Descripción y workaround temporal
- Issue 2: Descripción y workaround temporal

### Decisiones Tomadas
- Decisión 1: Razón y alternativas consideradas
- Decisión 2: Razón y alternativas consideradas
```

---

## REGLAS DE CALIDAD

### Documentación CLAUDE.md
- **Comandos:** Incluir ejemplo de uso y propósito
- **Arquitectura:** Focus en big picture, no detalles obvios
- **Actualización:** Solo agregar info no evidente del código

### Documentación PROJECT_STATUS
- **Datos duros:** Porcentajes específicos, números de tests, etc.
- **Issues concretos:** Archivos específicos, líneas de código
- **Roadmap actualizado:** Tiempos realistas basados en progreso real

### Session Handoffs
- **Específico:** Names de archivos, líneas de código, comandos exactos
- **Accionable:** Próxima sesión debe poder continuar inmediatamente
- **Contextual:** Incluir reasoning de decisiones importantes

---

## AUTOMATIZACIÓN RECOMENDADA

### Scripts Útiles
```bash
# Script para generar status report automático
./scripts/generate_status_report.sh

# Script para verificar que documentación está actualizada
./scripts/check_docs_freshness.sh

# Script para crear session handoff template
./scripts/create_session_handoff.sh
```

### Git Hooks (Recomendado)
- **Pre-commit:** Verificar que CLAUDE.md está actualizado si hay cambios arquitecturales
- **Post-commit:** Reminder para actualizar documentación si es sesión larga

---

## MÉTRICAS DE CALIDAD DE DOCUMENTACIÓN

### Indicadores de Buena Documentación
- ✅ Nueva instancia de Claude Code puede ser productiva en <10 minutos
- ✅ Status analysis refleja estado real del proyecto
- ✅ Session handoffs permiten continuidad sin pérdida de contexto
- ✅ CLAUDE.md contiene todos los comandos necesarios

### Red Flags
- ❌ Documentación desactualizada >1 semana
- ❌ Issues críticos no documentados
- ❌ Comandos en CLAUDE.md que no funcionan
- ❌ Session handoffs vagos o sin actionables

---

## RESPONSABILIDADES

### Claude Code (Durante Sesión)
- Leer documentación existente al inicio
- Mantener tracking de cambios importantes
- Actualizar docs antes de terminar sesión

### Usuario/Project Manager
- Revisar session handoffs para aprobar próximas prioridades
- Validar que el roadmap documentado sigue siendo correcto
- Proveer feedback sobre calidad de documentación

---

*Este proceso debe seguirse consistentemente para mantener la calidad y continuidad del proyecto.*