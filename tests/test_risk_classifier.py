from app.agents.risk_classifier import RiskClassifier

class TestRiskClassifier:
    def setup_method(self):
        self.classifier = RiskClassifier()
    
    def test_low_risk_common_symptoms(self):
        user_info = {
            "symptoms": "轻微咳嗽，有点痰",
            "age": 30,
            "medical_history": "无",
            "special_condition": ""
        }
        risk_level, score, factors = self.classifier.assess_risk(user_info)
        assert risk_level == "D"
        assert score < 30
    
    def test_high_risk_chest_pain(self):
        user_info = {
            "symptoms": "胸痛，呼吸困难",
            "age": 50,
            "medical_history": "高血压",
            "special_condition": ""
        }
        risk_level, score, factors = self.classifier.assess_risk(user_info)
        assert risk_level in ["A", "B"]
        assert "胸痛" in factors
    
    def test_elderly_increased_risk(self):
        user_info_young = {"symptoms": "发热", "age": 30, "medical_history": ""}
        _, score_young, _ = self.classifier.assess_risk(user_info_young)
        
        user_info_elderly = {"symptoms": "发热", "age": 70, "medical_history": ""}
        _, score_elderly, _ = self.classifier.assess_risk(user_info_elderly)
        
        assert score_elderly > score_young
    
    def test_diabetes_increases_risk(self):
        user_info_no = {"symptoms": "发热", "age": 40, "medical_history": ""}
        _, score_no, _ = self.classifier.assess_risk(user_info_no)
        
        user_info_diab = {"symptoms": "发热", "age": 40, "medical_history": "糖尿病"}
        _, score_diab, _ = self.classifier.assess_risk(user_info_diab)
        
        assert score_diab > score_no
    
    def test_pregnancy_increases_risk(self):
        user_info_no = {"symptoms": "头痛", "age": 30, "medical_history": ""}
        _, score_no, _ = self.classifier.assess_risk(user_info_no)
        
        user_info_preg = {"symptoms": "头痛", "age": 30, "medical_history": "", "special_condition": "孕妇"}
        _, score_preg, _ = self.classifier.assess_risk(user_info_preg)
        
        assert score_preg > score_no
    
    def test_generate_risk_report(self):
        user_info = {
            "symptoms": "胸痛",
            "age": 60,
            "medical_history": "心脏病",
            "special_condition": ""
        }
        report = self.classifier.generate_risk_report(user_info)
        
        assert "risk_level" in report
        assert "risk_name" in report
        assert "advice" in report
        assert "factors" in report
