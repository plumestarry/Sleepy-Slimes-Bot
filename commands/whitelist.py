from commands.method.database import OnebotDatabase

class WhiteList(object):

    @staticmethod
    def special_manage() -> dict[str, list[int]]:
    
        manage_dict = {}
        
        database = OnebotDatabase("database/data")
        con, cur = database("special_manage.db")
        
        manage_dict["special"] = []
        
        for group_id in database.get_data(con, cur, "group_id", "special"):
            manage_dict["special"].append(group_id[0])
            
        
        manage_dict["private"] = []
        
        for user_id in database.get_data(con, cur, "user_id", "private"):
            manage_dict["private"].append(user_id[0])
            
        database.close(con, cur)
        
        return manage_dict
    