
class Message_SendFormat(object):
    
    def __init__(self, action, id_type, id_value):
        self.action = action
        self.params = {}
        self.id_type = id_type
        self.id_value = id_value
        self.echo = "123"
    
    def __call__(self):
        return self.text_framework([])
    
    def text_framework(self, message_content):
        
        message_send = {}
        message_send["action"] = self.action
        
        self.params[self.id_type] = self.id_value
        self.params["message"] = message_content
        message_send["params"] = self.params
        
        message_send["echo"] = self.echo
        
        return message_send
    
    def normal_text(self, text):
        
        text_dict = {}
        
        text_dict["type"] = "text"
        text_dict["data"] = {"text": text}
        
        return text_dict
    
    def at_text(self, user_id):
        
        at_dict = {}
        
        at_dict["type"] = "at"
        at_dict["data"] = {"qq": str(user_id)}
        
        return at_dict
    
    def replay_text(self, message_id):
        
        replay_dict = {}
        
        replay_dict["type"] = "replay"
        replay_dict["data"] = {"id": str(message_id)}
        
        return replay_dict
    
    def music_text(self, music_type, music_id):
        
        music_dict = {}
        
        music_dict["type"] = "music"
        music_dict["data"] = {"type": str(music_type), "id": str(music_id)}
        
        return music_dict
    
    def face_text(self, face_id):
        
        face_dict = {}
        
        face_dict["type"] = "face"
        face_dict["data"] = {"text": str(face_id)}
        
        return face_dict
    
    def image_text(self, url):
        
        image_dict = {}
        
        image_dict["type"] = "image"
        image_dict["data"] = {"file": url}
        
        return image_dict
    
    def normal_message(self, text):
        
        text_dict = self.normal_text(text)
        message_dict = self.text_framework([text_dict])
        
        return message_dict
    
    def at_message(self, user_id, text):
        
        id_dict = self.at_text(user_id)
        text_dict = self.normal_text(" " + text)
        message_dict = self.text_framework([id_dict, text_dict])
        
        return message_dict
    
    def at_at_message(self, user_id_1, text_1, user_id_2, text_2):
        
        id_dict_1 = self.at_text(user_id_1)
        text_dict_1 = self.normal_text(" " + text_1)
        id_dict_2 = self.at_text(user_id_2)
        text_dict_2 = self.normal_text(" " + text_2)
        message_dict = self.text_framework([id_dict_1, text_dict_1, id_dict_2, text_dict_2])
        
        return message_dict
    
    def replay_message(self, message_id, user_id, text):
        
        replay_dict = self.replay_text(int(message_id))
        text_dict1 = self.normal_text(" ")
        id_dict = self.at_text(user_id)
        text_dict2 = self.normal_text(" " + text)
        message_dict = self.text_framework([replay_dict, text_dict1, id_dict, text_dict2])

        return message_dict
    
    def image_message(self, url):
        
        image_text = self.image_text(url)
        message_dict = self.text_framework([image_text])
        
        return message_dict
    
    def recall_message(self, message_id):
        
        message_dict = self.text_framework([])
        del message_dict["params"]["message"]
        del message_dict["params"]["group_id"]
        message_dict["params"]["message_id"] = int(message_id)
        
        return message_dict
    
class Parameter_Judgment(object):
    
    def parameter_judgment(self, message_dict):
        
        if message_dict["message_type"] == "group":
            return ["send_group_msg", "group_id", message_dict["group_id"]]
        else:
            return ["send_private_msg", "user_id", message_dict["user_id"]]



