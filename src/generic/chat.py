import os
import re
import json
import pandas as pd
from datetime import datetime

from src.generic.loader import get_env_variable


DEVELOPMENT = get_env_variable('DEVELOPMENT')


class __MessageHandler:
    # Issues with multiple instances of message handler or some shit...
    def __init__(self, environment: str):
        self.environment = environment  # i.e. "DEVELOPMENT"
        self.chats = {}
        self.chat_times = {}
    
    def get_seconds_between_datetimes(self, datetime1, datetime2):
        timedelta = datetime2 - datetime1
        seconds = timedelta.total_seconds()
        return abs(int(seconds))

    def get_seconds_since_last_message(self, ip: str):
        if ip not in self.chat_times:
            return 0
        return self.get_seconds_between_datetimes(self.chat_times[ip], datetime.now())

    def clear_chat(self, ip: str) -> None:
        if ip in self.chats and ip in self.chat_times:
            self.chats.pop(ip)
            self.chat_times.pop(ip)
        return None

    def get_nonhtml_chat(self, ip: str) -> list[str]:
        if self.get_seconds_since_last_message(ip) > 7200:
            #self.clear_chat(ip) # off for now
            return []
        if ip not in self.chats:
            return []
        chat_messages = self.chats[ip]
        chat_messages = [re.sub("\n", "<br>", message) for message in chat_messages]
        if DEVELOPMENT == 'TRUE': print("\n----------------------->")
        if DEVELOPMENT == 'TRUE': print("self.chats:")
        if DEVELOPMENT == 'TRUE': print(self.chats)
        return chat_messages

    def get_chat(self, ip: str) -> list[str]:
        if self.get_seconds_since_last_message(ip) > 7200:
            self.clear_chat(ip)
            return []
        if ip not in self.chats:
            return []
        chat_messages = self.chats[ip]
        if DEVELOPMENT == 'TRUE': print("\n----------------------->")
        if DEVELOPMENT == 'TRUE': print("self.chats:")
        if DEVELOPMENT == 'TRUE': print(self.chats)
        return chat_messages
    
    def create_empty_chat(self, ip: str):
        if ip not in self.chats:
            self.chats[ip] = []
        if ip not in self.chat_times:
            self.chat_times[ip] = datetime.now()
        return

    def add_chat_message(self, ip: str, message: str) -> None:
        if ip not in self.chats:
            self.create_empty_chat(ip)
            self.chats[ip] += [message]
            self.chat_times[ip] = datetime.now()
            return None
        self.chats[ip] += [message]
        self.chat_times[ip] = datetime.now()
        return None




class MessageHandler:
    def __init__(self, environment: str):
        self.environment = environment  # i.e. "DEVELOPMENT"
        self.chat_times = {}
        self.cwd = os.getcwd()
        self.path = ['src', 'generic', 'private_files']
        self.separator = '\\'
        if "/" in os.getcwd():
            self.separator = "/"
    
    def get_seconds_between_datetimes(self, datetime1, datetime2):
        timedelta = datetime2 - datetime1
        seconds = timedelta.total_seconds()
        return abs(int(seconds))

    def get_seconds_since_last_message(self, ip: str):
        if ip not in self.chat_times:
            return 0
        return self.get_seconds_between_datetimes(self.chat_times[ip], datetime.now())

    def get_prefix(self):
        if not self.cwd.strip():
            prefix = self.separator.join(self.path)
        else:
            prefix = self.cwd + self.separator + self.separator.join(self.path)
        return prefix
    
    def get_file_path(self, file_name):
        prefix = self.get_prefix()
        if prefix:
            file_path = prefix + self.separator + file_name
        else:
            file_path = file_name
        return file_path
    
    def read_csv(self, csv_name):
        file_path = self.get_file_path(csv_name)
        df = pd.read_csv(file_path)
        return df

    def save_csv(self, csv_name: str, df):
        file_path = self.get_file_path(csv_name)
        df.to_csv(file_path, index=False)
        return

    def to_dict(self, df):
        dd = dict(df)
        for key in dd:
            dd[key] = list(dd[key])
        return dd

    def clear_chat(self, ip: str) -> None:
        df = self.read_csv("chat_messages.csv")
        dd = self.to_dict(df)
        ddk = list(dd.keys())
        for i in range(len(dd[ddk[0]])):
            if dd["uuid"][i] == ip:
                dd["messages"][i] = json.dumps([])
                break
        self.save_csv("chat_messages.csv", pd.DataFrame(dd))
        return None
    
    def create_empty_chat(self, ip: str):
        df = self.read_csv("chat_messages.csv")
        dd = self.to_dict(df)
        if ip in dd["uuid"]:
            return
        dd["uuid"].append(ip)
        dd["messages"].append(json.dumps([]))
        self.save_csv("chat_messages.csv", pd.DataFrame(dd))
        return None

    def get_nonhtml_chat(self, ip: str) -> list[str]:
        if self.get_seconds_since_last_message(ip) > 7200:
            if DEVELOPMENT == 'TRUE': print("CLEARING CHAT")
            self.clear_chat(ip)
            return []
        df = self.read_csv("chat_messages.csv")
        dd = self.to_dict(df)
        
        ddk = list(dd.keys())
        chat_messages = []
        for i in range(len(dd[ddk[0]])):
            if dd["uuid"][i] == ip:
                chat_messages = json.loads(dd["messages"][i])
                break
        
        return chat_messages

    def get_chat(self, ip: str) -> list[str]:
        if self.get_seconds_since_last_message(ip) > 7200:
            self.clear_chat(ip)
            return []
        
        df = self.read_csv("chat_messages.csv")
        dd = self.to_dict(df)
        if ip not in dd["uuid"]:
            dd["uuid"].append(ip)
            dd["messages"].append(json.dumps([]))
        ddk = list(dd.keys())
        chat_messages = []
        for i in range(len(dd[ddk[0]])):
            if dd["uuid"][i] == ip:
                chat_messages = json.loads(dd["messages"][i])
                break
        
        chat_messages = [re.sub("\n", "<br>", message) for message in chat_messages]
        return chat_messages

    def add_chat_message(self, ip: str, message: str) -> None:
        df = self.read_csv("chat_messages.csv")
        dd = self.to_dict(df)
        if ip not in dd["uuid"]:
            dd["uuid"].append(ip)
            dd["messages"].append(json.dumps([]))
        ddk = list(dd.keys())
        for i in range(len(dd[ddk[0]])):
            if dd["uuid"][i] == ip:
                existing_messages = json.loads(dd["messages"][i])
                updated_messages_json = json.dumps(existing_messages + [message])
                dd["messages"][i] = updated_messages_json
                break
        
        self.save_csv("chat_messages.csv", pd.DataFrame(dd))
        return None

