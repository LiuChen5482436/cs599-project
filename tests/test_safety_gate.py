from app.agents.safety_gate import SafetyGate
import pytest

class TestSafetyGate:
    def setup_method(self):
        self.safety_gate = SafetyGate()
    
    def test_detect_chest_pain(self):
        has_flags, flags = self.safety_gate.detect_red_flags("我感到胸痛和胸闷")
        assert has_flags is True
        assert "胸痛" in flags
        assert "胸闷" in flags
    
    def test_detect_breathing_difficulty(self):
        has_flags, flags = self.safety_gate.detect_red_flags("呼吸困难，感觉喘不上气")
        assert has_flags is True
        assert "呼吸困难" in flags
    
    def test_detect_fainting(self):
        has_flags, flags = self.safety_gate.detect_red_flags("刚才晕倒了，意识模糊")
        assert has_flags is True
        assert "晕厥" in flags or "意识模糊" in flags
    
    def test_no_red_flags(self):
        has_flags, flags = self.safety_gate.detect_red_flags("轻微咳嗽，有一点痰")
        assert has_flags is False
        assert len(flags) == 0
    
    def test_emergency_response(self):
        flags = ["胸痛", "呼吸困难"]
        response = self.safety_gate.get_emergency_response(flags)
        assert "紧急情况" in response
        assert "胸痛" in response
        assert "120" in response
    
    def test_should_block_processing(self):
        assert self.safety_gate.should_block_processing("胸痛") is True
        assert self.safety_gate.should_block_processing("轻微咳嗽") is False
