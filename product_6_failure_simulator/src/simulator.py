import datetime
import random

class FailureSimulator:
    def __init__(self):
        self.scenarios = {
            "Service Outage": {
                "desc": "Complete unavailability of a core service component.",
                "primary_impact_base": "Immediate loss of functionality for dependent features.",
                "recovery_time_base_minutes": 45
            },
            "Configuration Error": {
                "desc": "Misconfiguration in deployment descriptors or environment variables.",
                "primary_impact_base": "Application instability or startup failure.",
                "recovery_time_base_minutes": 15
            },
            "Human Mistake": {
                "desc": "Accidental deletion of data or incorrect manual command execution.",
                "primary_impact_base": "Data integrity issues or service interruption.",
                "recovery_time_base_minutes": 60
            },
            "Traffic Spike": {
                "desc": "Sudden 300%+ increase in incoming requests.",
                "primary_impact_base": "Latency degradation and potential timeout errors.",
                "recovery_time_base_minutes": 30
            },
            "Dependency Failure": {
                "desc": "External API or database becomes unreachable.",
                "primary_impact_base": "Feature degradation in connected modules.",
                "recovery_time_base_minutes": 90
            },
            "Compliance Slip": {
                "desc": "Logging failure or encryption protocol mismatch.",
                "primary_impact_base": "Audit trail gaps and regulatory exposure.",
                "recovery_time_base_minutes": 120
            }
        }
        
        # Stage 2: Cascading Effects Map
        self.cascading_rules = {
            "Database": ["Authentication Service", "Reporting Module", "User Dashboard"],
            "Auth Service": ["All Protected Routes", "API Gateway"],
            "Payment Gateway": ["Checkout Flow", "Financial Reporting"],
            "CDN": ["Static Assets", "Frontend Performance"],
            "Logging Service": ["Compliance Dashboard", "Security Alerts"]
        }

    def simulate(self, scenario_type, component, redundancy_level="None"):
        """
        Stage 1 & 2: Core Simulation Logic & Impact Modeling
        """
        if scenario_type not in self.scenarios:
            return {"error": "Unknown scenario type"}

        base_data = self.scenarios[scenario_type]
        
        # Calculate Impacts
        primary_impact = f"{base_data['primary_impact_base']} (Component: {component})"
        
        # Cascading Logic
        secondary_impacts = []
        affected_systems = self.cascading_rules.get(component, ["General System Stability"])
        for sys in affected_systems:
            secondary_impacts.append(f"Degradation in {sys}")
            
        # Time to Recovery Calculation (based on redundancy)
        ttr = base_data['recovery_time_base_minutes']
        if redundancy_level == "High (Active-Active)":
            ttr = ttr * 0.1 # 90% faster
        elif redundancy_level == "Medium (Active-Passive)":
            ttr = ttr * 0.5 # 50% faster
        
        # Blast Radius Calculation
        blast_radius_score = len(secondary_impacts) * 20 + (ttr / 10)
        blast_radius_level = "Critical" if blast_radius_score > 80 else "High" if blast_radius_score > 50 else "Moderate"
        
        # Stage 3: Confidence Scoring
        # Lower confidence if TTR is high and blast radius is wide
        confidence_score = max(0, 100 - (ttr * 0.5) - (len(secondary_impacts) * 5))
        
        return {
            "scenario": scenario_type,
            "component": component,
            "redundancy": redundancy_level,
            "primary_impact": primary_impact,
            "secondary_impacts": secondary_impacts,
            "ttr_estimate_mins": int(ttr),
            "blast_radius_level": blast_radius_level,
            "confidence_score": int(confidence_score),
            "timestamp": datetime.datetime.now().isoformat()
        }

    def generate_brief(self, result, mode="Executive"):
        """
        Stage 3 & 4: Decision Brief Generation (Executive vs Policy Mode)
        """
        ttr = result['ttr_estimate_mins']
        conf = result['confidence_score']
        
        if mode == "Executive":
            # Concise, bottom-line focused
            recommendation = "PROCEED" if conf > 80 else "DELAY LAUNCH" if conf < 50 else "PROCEED WITH CAUTION"
            
            return f"""
**DECISION BRIEF (Executive Mode)**
------------------------------------------------
**Scenario:** {result['scenario']} on {result['component']}
**Outcome:** {result['blast_radius_level']} Impact
**Est. Recovery:** {ttr} minutes

**BOTTOM LINE:**
{recommendation} (Confidence: {conf}/100)

**CRITICAL IMPACT:**
{result['primary_impact']}
{', '.join(result['secondary_impacts'][:2])}

**ASSUMPTION:**
Simulation assumes {result['redundancy']} redundancy is fully operational.
"""
        elif mode == "Policy":
            # Formal, audit-friendly, methodology-focused
            return f"""
**SIMULATION REPORT (Policy & Compliance Mode)**
------------------------------------------------
**Reference ID:** SIM-{random.randint(1000, 9999)}
**Timestamp:** {result['timestamp']}
**Methodology:** Deterministic Dependency Modeling (Non-Intrusive)

**SCENARIO PARAMETERS:**
- Type: {result['scenario']}
- Target: {result['component']}
- Redundancy State: {result['redundancy']}

**IMPACT ANALYSIS:**
- Primary Vector: {result['primary_impact']}
- Cascading Scope: {', '.join(result['secondary_impacts'])}
- Recovery Time Objective (Est): {ttr} minutes

**RISK ASSESSMENT:**
- Blast Radius Classification: {result['blast_radius_level'].upper()}
- Readiness Confidence Score: {conf}/100

**AUDIT CONCLUSION:**
This simulation indicates a {result['blast_radius_level']} risk exposure. 
Controls are {'sufficient' if conf > 75 else 'insufficient'} to meet standard SLAs.
Recommended Action: {'Approve' if conf > 75 else 'Review Mitigations'}.
"""
        else:
            return "Invalid Mode Selected"
