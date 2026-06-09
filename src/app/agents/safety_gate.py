from app.utils.config import Config

class SafetyGate:
    def __init__(self):
        self.red_flag_symptoms = Config.RED_FLAG_SYMPTOMS

    def detect_red_flags(self, user_input: str) -> tuple[bool, list[str]]:
        detected_flags = []
        user_input_lower = user_input.lower()

        for symptom in self.red_flag_symptoms:
            if symptom in user_input_lower:
                detected_flags.append(symptom)

        return len(detected_flags) > 0, detected_flags

    def get_emergency_response(self, detected_flags: list[str]) -> str:
        response = "⚠️ **紧急情况识别**\n\n"
        response += "检测到以下紧急症状：\n"
        for flag in detected_flags:
            response += f"- {flag}\n"
        response += "\n🚑 **紧急处置建议：**\n"
        response += "1. 请立即拨打急救电话120\n"
        response += "2. 在等待救护车时，请保持患者平躺\n"
        response += "3. 如果患者意识清醒，请保持其温暖舒适\n"
        response += "4. 不要给意识不清的患者喂食或喂水\n"
        response += "\n⚠️ 本建议不能替代专业医疗诊断，请立即寻求医疗帮助！"
        return response

    def should_block_processing(self, user_input: str) -> bool:
        has_flags, _ = self.detect_red_flags(user_input)
        return has_flags
