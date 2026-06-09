from app.utils.config import Config

class RiskClassifier:
    def __init__(self):
        self.risk_levels = Config.RISK_LEVELS
        self.special_populations = Config.SPECIAL_POPULATIONS

    def assess_risk(self, user_info: dict) -> tuple[str, float, list[str]]:
        risk_score = 0
        factors = []

        symptoms = user_info.get("symptoms", "") or ""
        age = user_info.get("age")
        medical_history = user_info.get("medical_history", "") or ""
        special_condition = user_info.get("special_condition", "") or ""
        temperature = user_info.get("temperature") or 0

        if "发热" in symptoms or "发烧" in symptoms:
            risk_score += 10
            factors.append("发热")
        if "头痛" in symptoms:
            risk_score += 10
            factors.append("头痛")
        if "腹痛" in symptoms or "腹泻" in symptoms:
            risk_score += 10
            factors.append("消化道症状")

        if "发热" in symptoms and temperature > 39:
            risk_score += 30
            factors.append("高热(>39°C)")
        if "呼吸困难" in symptoms:
            risk_score += 40
            factors.append("呼吸困难")
        if "胸痛" in symptoms:
            risk_score += 40
            factors.append("胸痛")
        if "意识模糊" in symptoms:
            risk_score += 50
            factors.append("意识模糊")
        if "呕血" in symptoms or "黑便" in symptoms:
            risk_score += 35
            factors.append("消化道出血")

        if age is not None and age >= 65:
            risk_score *= 1.3
            factors.append("老年人(>=65岁)")
        elif age is not None and age <= 12:
            risk_score *= 1.5
            factors.append("儿童(<=12岁)")

        if "糖尿病" in medical_history:
            risk_score += 15
            factors.append("糖尿病史")
        if "高血压" in medical_history:
            risk_score += 10
            factors.append("高血压史")
        if "心脏病" in medical_history:
            risk_score += 20
            factors.append("心脏病史")

        if "孕妇" in special_condition:
            risk_score *= 1.5
            factors.append("孕妇")
        if "免疫低下" in special_condition:
            risk_score *= 1.4
            factors.append("免疫低下")

        if risk_score >= 70:
            return "A", risk_score, factors
        elif risk_score >= 50:
            return "B", risk_score, factors
        elif risk_score >= 30:
            return "C", risk_score, factors
        else:
            return "D", risk_score, factors

    def get_risk_info(self, risk_level: str) -> dict:
        return self.risk_levels.get(risk_level, {})

    def generate_risk_report(self, user_info: dict) -> dict:
        risk_level, score, factors = self.assess_risk(user_info)
        risk_info = self.get_risk_info(risk_level)

        report = {
            "risk_level": risk_level,
            "risk_name": risk_info.get("name", ""),
            "risk_description": risk_info.get("description", ""),
            "score": score,
            "factors": factors,
            "advice": self._generate_advice(risk_level)
        }

        return report

    def _generate_advice(self, risk_level: str) -> str:
        advices = {
            "A": "请立即前往急诊科就诊，不要延误！",
            "B": "建议24小时内前往医院就诊",
            "C": "建议1-3天内前往医院门诊就诊",
            "D": "可居家观察，注意休息，如症状加重请及时就医"
        }
        return advices.get(risk_level, "")
