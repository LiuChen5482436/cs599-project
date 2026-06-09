from app.agents.followup_agent import FollowupAgent

class TestFollowupAgent:
    def setup_method(self):
        self.agent = FollowupAgent()
    
    def test_identify_missing_fields(self):
        conversation = [
            {"content": "我头痛已经2天了"},
        ]
        missing = self.agent.identify_missing_fields(conversation)
        assert "症状" not in missing
        assert "部位" not in missing
        assert "持续时间" not in missing
    
    def test_identify_all_missing(self):
        conversation = [
            {"content": "我不舒服"},
        ]
        missing = self.agent.identify_missing_fields(conversation)
        assert len(missing) > 0
    
    def test_generate_followup_question(self):
        missing = ["部位", "持续时间"]
        question = self.agent.generate_followup_question(missing)
        assert question is not None
        assert len(question) > 0
