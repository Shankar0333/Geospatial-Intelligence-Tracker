from app.models.schemas import DefenseEvent, LandEvent, RiskAssessment, SeaVessel


class RiskService:
    def assess(self, alerts_count: int, defense_events: list[DefenseEvent], sea_vessels: list[SeaVessel], land_events: list[LandEvent]) -> RiskAssessment:
        rationale: list[str] = []
        score = 0.0

        if alerts_count > 25:
            score += 35
            rationale.append("High volume of alert signals in the last analysis window")
        elif alerts_count > 10:
            score += 20
            rationale.append("Moderate alert activity detected")

        defense_weight = min(len(defense_events) * 8, 24)
        if defense_weight:
            score += defense_weight
            rationale.append("Public defense activity feed indicates heightened operations")

        if len(sea_vessels) > 1:
            score += 12
            rationale.append("Sea domain shows active vessel movement near monitored routes")

        if len(land_events) > 1:
            score += 10
            rationale.append("Land mobility events suggest corridor disruptions")

        score = round(min(score, 100), 2)
        if score >= 70:
            level = "high"
        elif score >= 40:
            level = "medium"
        else:
            level = "low"

        if not rationale:
            rationale.append("No significant risk indicators above baseline")

        return RiskAssessment(overall_score=score, level=level, rationale=rationale)
