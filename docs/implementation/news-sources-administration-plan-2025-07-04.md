# News Sources Administration Implementation Plan

**Date:** 2025-07-04
**Version:** 1.0
**Status:** Planning Phase
**Estimated Duration:** 7-10 development sessions

## 🎯 Objective

Implement a complete news sources administration system with automatic validation, health monitoring, and compliance management building on the existing solid foundation while maintaining **full legal and ethical compliance**.

## 📊 Current State Analysis

### ✅ Strengths (Already Implemented)
- **Robust Data Models**: Complete NewsSource model with validation fields
- **Legal Compliance Framework**: Comprehensive implementation (🔴 CRITICAL → 🟢 LOW RISK)
- **Robots.txt Compliance**: 100% automated validation with 24-hour caching
- **GDPR Framework**: Complete privacy policy and Colombian Law 1581/2012 compliance
- **8 Sources Configured**: All sources validated and legally compliant
- **4 Operational Scrapers**: Producing 106 articles with 100% compliance rate
- **Infrastructure Ready**: PostgreSQL + FastAPI + React stack

### ❌ Missing Components
- **API Layer**: No CRUD endpoints for source management
- **Frontend Interface**: No admin panel for source configuration
- **Automated Validation**: No continuous health monitoring
- **Compliance Monitoring**: No real-time compliance dashboard

## 🛡️ Legal & Ethical Compliance Integration

### **Critical Compliance Requirements**
All new source administration features must maintain the existing legal compliance framework:

#### **1. Pre-Source Validation (MANDATORY)**
```python
# All new sources must pass compliance validation
async def validate_new_source(source_data: dict) -> bool:
    # 1. Robots.txt compliance check
    robots_compliant = await check_robots_compliance(source_data['base_url'])

    # 2. Legal contact verification
    legal_contact = await verify_legal_contact(source_data)

    # 3. Terms of service review
    tos_acceptable = await review_terms_of_service(source_data['terms_of_service_url'])

    # 4. Content type classification
    content_type = classify_content_type(source_data)

    # 5. Fair use assessment
    fair_use_basis = assess_fair_use(source_data, "academic_research")

    return all([robots_compliant, legal_contact, tos_acceptable, content_type == 'metadata_only'])
```

#### **2. Continuous Compliance Monitoring**
- **Daily robots.txt verification** for all active sources
- **Legal status tracking** with automatic alerts
- **Content type enforcement** (metadata only)
- **Fair use documentation** updates

#### **3. Audit Trail Requirements**
All source management actions must be logged in `compliance_audit_log`:
```sql
INSERT INTO compliance_audit_log (
    table_name, record_id, action, old_values, new_values,
    legal_basis, performed_by, performed_at
) VALUES (...);
```

## 🚀 Implementation Plan

### **Phase 1: Compliance-First API Layer (2-3 sessions)**

#### 1.1 Core CRUD Endpoints with Compliance Integration
```python
# services/api/routers/sources.py
@router.post("/sources/", dependencies=[Depends(verify_admin_role)])
async def create_source(source: SourceCreateRequest, current_user: User = Depends(get_current_user)):
    """Create new source with mandatory compliance validation"""
    # MANDATORY: Pre-validation compliance check
    compliance_result = await validate_source_compliance(source)
    if not compliance_result.is_compliant:
        raise HTTPException(400, f"Compliance violation: {compliance_result.error}")

    # MANDATORY: Fair use assessment
    fair_use_assessment = await assess_fair_use_basis(source, "academic_research")

    # MANDATORY: Audit logging
    await log_compliance_action("sources", "create", source.dict(), current_user.id)

    return await create_source_with_compliance(source, compliance_result, fair_use_assessment)

@router.put("/sources/{source_id}/validate")
async def validate_source_compliance(source_id: int):
    """Comprehensive compliance validation for existing source"""
    source = await get_source_by_id(source_id)

    validation_results = {
        "robots_txt_compliant": await check_robots_compliance(source.base_url),
        "legal_contact_verified": await verify_legal_contact(source),
        "terms_of_service_acceptable": await review_terms_of_service(source.terms_of_service_url),
        "content_type_compliant": source.content_type == "metadata_only",
        "fair_use_documented": bool(source.fair_use_basis),
        "retention_policy_set": bool(source.data_retention_expires_at)
    }

    # Update compliance status
    await update_source_compliance_status(source_id, validation_results)

    # Log compliance action
    await log_compliance_action("sources", "validate", validation_results, "system")

    return {"source_id": source_id, "validation_results": validation_results}
```

#### 1.2 Compliance-Specific Endpoints
```python
GET    /api/v1/sources/compliance-dashboard    # Real-time compliance status
POST   /api/v1/sources/{id}/legal-review      # Legal review workflow
GET    /api/v1/sources/audit-trail            # Complete audit history
POST   /api/v1/sources/bulk-compliance-check  # Bulk compliance validation
GET    /api/v1/sources/non-compliant          # Sources needing attention
```

### **Phase 2: Compliance-Aware Frontend Interface (3-4 sessions)**

#### 2.1 Source Management Dashboard with Compliance Indicators
```tsx
// preventia-dashboard/src/pages/admin/SourcesAdminPage.tsx
export const SourcesAdminPage: React.FC = () => {
  return (
    <div className="sources-admin-page">
      <ComplianceStatusHeader />
      <SourcesTable
        showComplianceColumns={true}
        highlightNonCompliant={true}
      />
      <ComplianceActionsPanel />
    </div>
  );
};

// Compliance status indicators
const ComplianceStatusIndicator: React.FC<{source: NewsSource}> = ({source}) => {
  const getComplianceColor = (status: string) => {
    switch(status) {
      case 'compliant': return 'green';
      case 'needs_review': return 'yellow';
      case 'violation': return 'red';
      default: return 'gray';
    }
  };

  return (
    <div className="compliance-status">
      <span className={`status-badge ${getComplianceColor(source.legal_review_status)}`}>
        {source.legal_review_status}
      </span>
      <Tooltip content={`Robots.txt: ${source.robots_txt_compliant ? '✅' : '❌'}`}>
        <Icon name="robot" />
      </Tooltip>
      <Tooltip content={`Fair Use: ${source.fair_use_basis ? '✅' : '❌'}`}>
        <Icon name="legal" />
      </Tooltip>
    </div>
  );
};
```

#### 2.2 Compliance-First Source Configuration
```tsx
// preventia-dashboard/src/components/admin/SourceConfigForm.tsx
export const SourceConfigForm: React.FC = () => {
  const [complianceValidation, setComplianceValidation] = useState(null);

  const validateCompliance = async (sourceData: Partial<NewsSource>) => {
    const result = await api.post('/sources/validate-compliance', sourceData);
    setComplianceValidation(result.data);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Standard form fields */}
      <ComplianceValidationSection
        validation={complianceValidation}
        onValidate={validateCompliance}
      />

      <LegalRequirementsSection
        required={['robots_txt_url', 'terms_of_service_url', 'legal_contact_email']}
      />

      <FairUseDocumentationSection
        basis="academic_research"
        required={true}
      />

      <button type="submit" disabled={!complianceValidation?.is_compliant}>
        Create Source (Compliance Required)
      </button>
    </form>
  );
};
```

### **Phase 3: Enhanced Compliance Monitoring (2-3 sessions)**

#### 3.1 Automated Compliance Checker
```python
# services/data/validation/compliance_monitor.py
class ComplianceMonitor:
    async def run_daily_compliance_check(self) -> ComplianceReport:
        """Daily compliance verification for all active sources"""
        sources = await get_active_sources()
        results = []

        for source in sources:
            # Check robots.txt compliance
            robots_status = await self.check_robots_compliance(source)

            # Verify legal contact availability
            legal_contact_status = await self.verify_legal_contact(source)

            # Check data retention compliance
            retention_status = await self.check_data_retention(source)

            # Validate fair use documentation
            fair_use_status = await self.validate_fair_use_docs(source)

            compliance_result = ComplianceCheckResult(
                source_id=source.id,
                robots_compliant=robots_status,
                legal_contact_verified=legal_contact_status,
                retention_compliant=retention_status,
                fair_use_documented=fair_use_status,
                overall_status='compliant' if all([robots_status, legal_contact_status, retention_status, fair_use_status]) else 'needs_review'
            )

            results.append(compliance_result)

            # Log compliance check
            await self.log_compliance_check(source.id, compliance_result)

        return ComplianceReport(results=results, generated_at=datetime.now())

    async def handle_compliance_violations(self, violations: List[ComplianceViolation]):
        """Handle compliance violations with automatic actions"""
        for violation in violations:
            if violation.severity == 'critical':
                # Automatic source deactivation
                await self.deactivate_source(violation.source_id, reason=violation.description)

                # Alert administrators
                await self.send_compliance_alert(violation)

                # Log violation
                await self.log_compliance_violation(violation)
```

#### 3.2 Real-time Compliance Dashboard
```python
# services/api/routers/compliance.py
@router.get("/compliance/dashboard")
async def get_compliance_dashboard():
    """Real-time compliance dashboard data"""
    return {
        "total_sources": await count_total_sources(),
        "compliant_sources": await count_compliant_sources(),
        "pending_review": await count_pending_review(),
        "violations": await get_recent_violations(),
        "audit_summary": await get_audit_summary(),
        "legal_actions_needed": await get_legal_actions_needed(),
        "compliance_trend": await get_compliance_trend_data()
    }
```

### **Phase 4: Legal Risk Management (1-2 sessions)**

#### 4.1 Automated Risk Assessment
```python
# services/data/legal/risk_assessment.py
class LegalRiskAssessment:
    def assess_source_risk(self, source: NewsSource) -> RiskLevel:
        """Comprehensive legal risk assessment for news source"""
        risk_factors = []

        # Copyright risk assessment
        if not source.fair_use_basis:
            risk_factors.append(RiskFactor("copyright", "high", "No fair use documentation"))

        # Robots.txt compliance risk
        if not source.robots_txt_compliant:
            risk_factors.append(RiskFactor("robots_txt", "medium", "Robots.txt non-compliant"))

        # Data retention risk
        if not source.data_retention_expires_at:
            risk_factors.append(RiskFactor("retention", "low", "No data retention policy"))

        # Legal contact risk
        if not source.legal_contact_email:
            risk_factors.append(RiskFactor("contact", "medium", "No legal contact available"))

        # Terms of service risk
        if not source.terms_of_service_url:
            risk_factors.append(RiskFactor("tos", "low", "No terms of service documented"))

        # Calculate overall risk level
        high_risk_count = sum(1 for rf in risk_factors if rf.level == "high")
        medium_risk_count = sum(1 for rf in risk_factors if rf.level == "medium")

        if high_risk_count > 0:
            return RiskLevel("high", risk_factors)
        elif medium_risk_count > 2:
            return RiskLevel("medium", risk_factors)
        else:
            return RiskLevel("low", risk_factors)
```

## 🚨 Critical Compliance Considerations

### **Mandatory Pre-Implementation Checks**
1. **Legal Framework Preservation**: All existing compliance measures must remain intact
2. **Audit Trail Continuity**: Complete logging of all source management actions
3. **University Standards**: Maintain UCOMPENSAR academic research compliance
4. **Colombian Law**: Continue Ley 1581/2012 compliance
5. **GDPR Compatibility**: Preserve EU data protection standards

### **Prohibited Actions**
- **Never bypass robots.txt validation** - System must reject non-compliant sources
- **Never store full content** - Metadata-only enforcement must be maintained
- **Never skip legal review** - All sources require legal status documentation
- **Never disable audit logging** - Complete action history required

### **Required Documentation Updates**
- Update `legal/privacy-policy-template.md` with new source management features
- Extend `legal/medical-disclaimers.md` with automated source validation disclaimers
- Document new compliance procedures in `docs/compliance/`

## 📈 Success Metrics

### **Legal Compliance Metrics**
- **Compliance Rate**: 100% (no degradation from current state)
- **Robots.txt Validation**: 100% automated compliance
- **Legal Review Coverage**: 100% of sources reviewed
- **Audit Trail Completeness**: 100% action logging

### **Technical Metrics**
- **Source Availability**: > 95% uptime
- **Validation Success Rate**: > 90%
- **API Response Time**: < 2 seconds
- **Compliance Dashboard**: Real-time updates

## 🔄 Implementation Timeline

### **Session 1-2: Compliance-First API Implementation**
- Implement source CRUD endpoints with mandatory compliance checks
- Create compliance validation endpoints
- Integrate with existing legal framework

### **Session 3-4: Frontend Compliance Interface**
- Build admin dashboard with compliance indicators
- Create compliance-aware source configuration forms
- Implement real-time compliance monitoring

### **Session 5-6: Automated Compliance Monitoring**
- Develop automated compliance checking system
- Implement violation handling and alerts
- Create compliance reporting dashboard

### **Session 7: Legal Risk Management**
- Implement automated risk assessment
- Create legal action workflows
- Finalize compliance documentation

## 📝 Next Steps

1. **Legal Review Confirmation**: Verify plan maintains existing compliance framework
2. **Technical Architecture Review**: Ensure seamless integration with existing systems
3. **Begin Phase 1**: Start with compliance-first API implementation
4. **Continuous Compliance**: Maintain 100% compliance rate throughout development

---

**⚖️ Legal Compliance Statement**: This implementation plan is designed to maintain and enhance the existing comprehensive legal compliance framework (🔴 CRITICAL → 🟢 LOW RISK status). All new features will be implemented with legal compliance as the primary consideration, ensuring continued suitability for academic research and institutional use.

**Contact**: cfernandom@ucompensar.edu.co | Legal Framework Maintained | University Standards Preserved
