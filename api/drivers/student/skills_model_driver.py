from typing import Dict
from api.models.student.skill_model import SkillsModel
from typing import Dict

class Skills:

    async def add_skills(self,info: Dict):
        skills = SkillsModel(**info)

        db_response = await SkillsModel.save(skills)
        if db_response:
            return True

        return False


    async def delete_skills(self, info: Dict):
        skills = await SkillsModel.find_one(SkillsModel.skill_id == info["skill_id"])

        if skills is None:
            return False

        db_response = await skills.delete()

        if db_response:
            return True

        return False


        #TODO: Add other functions