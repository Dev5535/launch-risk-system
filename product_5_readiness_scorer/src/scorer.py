class LaunchScorer:
    def __init__(self):
        self.weights = {
            'Critical': 100, # Instant fail
            'High': 10,
            'Medium': 5,
            'Low': 1
        }
        self.max_score = 100

    def calculate(self, findings):
        """
        findings: List of dicts with 'severity' key.
        """
        score = self.max_score
        breakdown = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        
        for f in findings:
            severity = f.get('severity', 'Low') # Default to Low
            # Normalize severity strings
            sev_norm = severity.capitalize()
            if sev_norm not in breakdown:
                sev_norm = 'Low'
            
            breakdown[sev_norm] += 1
            
            # Apply deduction
            deduction = self.weights.get(sev_norm, 1)
            score -= deduction

        # Cap score at 0
        final_score = max(0, score)
        
        # Determine Status
        if breakdown['Critical'] > 0 or final_score < 70:
            status = "BLOCKED"
            color = "red"
        elif final_score < 90:
            status = "CAUTION"
            color = "yellow"
        else:
            status = "APPROVED"
            color = "green"

        return {
            'score': final_score,
            'status': status,
            'color': color,
            'breakdown': breakdown
        }
