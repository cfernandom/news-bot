---
version: "1.0"
last_updated: "2025-07-04"
maintainer: "Claude (Technical Director)"
status: "active"
---

# Language Usage Standard

## Overview

This document establishes the standardized language usage across all PreventIA News Analytics project documentation and code to ensure consistency, maintainability, and professional collaboration.

## Language Standards

### English Usage

#### Code & Technical Implementation
- **Source code**: Variables, functions, classes, comments
- **Configuration files**: Environment variables, Docker configurations
- **CLAUDE.md**: Technical instructions for Claude Code
- **API Documentation**: All API-related documentation (`docs/api/`)
- **Technical Architecture**: System design documentation (`docs/architecture/`)
- **Development Standards**: Testing, coding standards (`docs/development/standards/`)
- **Database schemas**: Table names, column names, constraints

#### Examples
```python
# ✅ Correct - English code
class SentimentAnalyzer:
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of medical content."""
        return self._process_medical_text(text)

# ❌ Incorrect - Mixed languages
class AnalizadorSentimiento:
    def analyze_sentiment(self, texto: str) -> Dict[str, Any]:
        """Analiza el sentimiento del contenido médico."""
        return self._procesar_texto_medico(texto)
```

### Spanish Usage

#### Team Documentation & Decisions
- **ADRs (Architecture Decision Records)**: Team architectural decisions (`docs/decisions/`)
- **Implementation Results**: Project phase results (`docs/implementation/`)
- **Conversation Records**: Team discussion logs (`docs/conversations/`)
- **Main README.md**: Project overview for Spanish-speaking team
- **User-facing documentation**: End-user guides and manuals

#### Examples
```markdown
# ✅ Correct - Spanish ADRs
# ADR-004: Implementación de Análisis de Sentimientos para Contenido Médico

## Contexto y Problema
El sistema PreventIA requería capacidades de análisis de sentimientos...

## Decisión
Elegimos VADER + spaCy preprocessing con thresholds ajustados...
```

## Rationale

### Why English for Technical Content?
1. **International Standard**: English is the lingua franca of software development
2. **Future Collaboration**: Enables international developers to contribute
3. **Tool Compatibility**: Most development tools expect English
4. **Code Reusability**: Code can be shared across projects and organizations
5. **Documentation Longevity**: English technical docs have longer shelf life

### Why Spanish for Team Decisions?
1. **Team Communication**: Core team is Spanish-speaking
2. **Decision Clarity**: Complex architectural decisions communicated better in native language
3. **Stakeholder Understanding**: Business stakeholders prefer Spanish
4. **Cultural Context**: Some business concepts translate better in Spanish

## Implementation Guidelines

### File-by-File Language Assignment

```
project/
├── services/                     # 🇺🇸 English (code)
│   ├── nlp/src/sentiment.py    # 🇺🇸 English
│   └── data/models.py           # 🇺🇸 English
├── docs/
│   ├── api/                     # 🇺🇸 English (technical)
│   ├── architecture/            # 🇺🇸 English (technical)
│   ├── decisions/               # 🇪🇸 Spanish (team decisions)
│   ├── implementation/          # 🇪🇸 Spanish (results)
│   ├── conversations/           # 🇪🇸 Spanish (team logs)
│   └── development/standards/   # 🇺🇸 English (technical)
├── CLAUDE.md                    # 🇺🇸 English (Claude instructions)
├── README.md                    # 🇪🇸 Spanish (team overview)
└── requirements.txt             # 🇺🇸 English (technical)
```

### Mixed Content Guidelines

#### When Both Languages Are Acceptable
- **Code comments explaining business logic**: Can use Spanish if it improves understanding
- **Test data with real content**: Can reflect source language (medical articles)
- **Error messages for end users**: Should be in Spanish
- **Log messages**: Technical logs in English, user-facing logs in Spanish

#### Examples
```python
# ✅ Acceptable - Business logic comment in Spanish
def calculate_relevance_score(article: Article) -> float:
    # Calculamos relevancia basada en keywords de cáncer de mama
    # porque el contexto médico es específico del dominio
    keywords = extract_medical_keywords(article.content)
    return score

# ✅ Acceptable - User-facing error in Spanish
class ArticleProcessingError(Exception):
    def __init__(self, article_id: int):
        super().__init__(f"Error procesando artículo {article_id}")
```

### Documentation Structure Standards

#### English Documents Template
```markdown
# [Document Title]

## Overview
Brief description in clear, professional English.

## Technical Details
- Use bullet points
- Include code examples
- Reference external resources in English

## References
- [External Link](https://example.com)
- [Internal Reference](../other-doc.md)
```

#### Spanish Documents Template
```markdown
# [Título del Documento]

## Resumen
Descripción breve en español claro y profesional.

## Contexto y Problema
- Usar puntos clave
- Incluir ejemplos cuando sea necesario
- Referencias en contexto apropiado

## Referencias
- [Enlace Externo](https://example.com)
- [Referencia Interna](../otro-doc.md)
```

## Quality Assurance

### Language Review Checklist

#### For English Documents
- [ ] Professional, clear English
- [ ] Technical terminology consistent
- [ ] Code examples follow English naming conventions
- [ ] References to English resources when available

#### For Spanish Documents
- [ ] Clear, professional Spanish
- [ ] Technical terms properly translated or explained
- [ ] Consistent with team communication style
- [ ] Cultural context appropriate

### Common Mistakes to Avoid

#### ❌ Don't Mix Languages Within Sentences
```markdown
# Wrong
El sistema uses VADER para sentiment analysis.

# Correct
El sistema utiliza VADER para análisis de sentimientos.
# OR
The system uses VADER for sentiment analysis.
```

#### ❌ Don't Translate Technical Terms Unnecessarily
```markdown
# Wrong
Análisis de datos con algoritmos de aprendizaje de máquina

# Better
Análisis de datos con algoritmos de machine learning
```

#### ❌ Don't Use Spanish in Code Identifiers
```python
# Wrong
def analizar_sentimiento(texto: str) -> dict:
    pass

# Correct
def analyze_sentiment(text: str) -> dict:
    pass
```

## Migration Strategy

### Existing Documents
1. **Phase 1**: Identify documents that need language standardization
2. **Phase 2**: Migrate high-priority documents (API docs, architecture)
3. **Phase 3**: Update remaining documents gradually
4. **Phase 4**: Establish review process for new documents

### Legacy Content
- **Preserve**: Existing Spanish comments in code if they add value
- **Migrate**: API documentation to English
- **Maintain**: ADRs in Spanish (they represent team decisions)

## Enforcement

### New Documents
- All new technical documentation must follow this standard
- ADRs and team decisions continue in Spanish
- Code reviews should check language consistency

### Tools & Automation
- **Linting**: Configure tools to check English variable/function names
- **Templates**: Use language-specific templates for documentation
- **Review Process**: Include language standard check in PR reviews

## Exceptions

### When to Deviate
1. **External Requirements**: Client specifically requests Spanish technical docs
2. **Regulatory Compliance**: Legal documents may require Spanish
3. **User Interface**: End-user facing text should be in Spanish
4. **Business Requirements**: Stakeholder presentations may need Spanish

### Approval Process
- Exceptions must be documented with business justification
- Technical Lead approval required for deviations
- Update this standard if patterns emerge

## References

- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://docs.microsoft.com/en-us/style-guide/)
- [Real Academia Española - Tecnología](https://www.rae.es/)

---
**Effective Date**: 2025-06-28
**Last Updated**: 2025-06-28
**Next Review**: 2025-09-28
**Approved By**: Claude (Technical Director), cfernandom (Senior Engineer)
