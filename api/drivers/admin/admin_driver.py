from typing import Dict

from api.models.admin.admin_model import AdminModel
from passlib.hash import pbkdf2_sha256


class Admin:

    def __init__(self):
        self.predefined_scopes = [
            "student", "admin", "company", "events",
            "stories", "placements", "news", "visitors",
            "people", "home", "postings", "about", "all"
        ]

    async def add_admin(self, info: Dict):
        admin = AdminModel(**info)

        admin.password = pbkdf2_sha256.hash(str(admin.password))

        db_response = await AdminModel.insert_one(admin)

        if db_response:
            return True
        
        return False
    

    async def update_admin_password(self, info: Dict):
        admin = await AdminModel.find(
            AdminModel.admin_id == info["admin_id"]
        )

        if admin is None:
            return False

        admin.password = pbkdf2_sha256.hash(str(info["password"]))

        db_response = await AdminModel.save(admin)

        if db_response:
            return True
        
        return False

    async def check_scope(self, admin_id, scope) -> bool:
        admin = await AdminModel.find(
            AdminModel.admin_id == admin_id
        )

        if admin is None:
            return False
        
        if scope in admin.scopes or "all" in admin.scopes:
            return True
        
        return False
    
    async def update_admin_scope(self, info: Dict):
        is_scope_present = self.check_scope(info["admin_id"], "admin")

        if not is_scope_present:
            return False
        
        admin = await AdminModel.find(
            AdminModel.admin_id == info["uadmin_id"]
        )

        counter = 0

        for scope in info["scopes"]:
            if scope in self.predefined_scopes:
                admin.scopes.append(scope)
            else:
                counter += 1
            
        if counter == len(info["scopes"]):
            return False

        db_response = await AdminModel.save(admin)

        if db_response:
            return True
        
        return False
        