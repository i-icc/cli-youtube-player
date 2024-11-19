import os

# 新しいディレクトリ作ったり確認するクラス
class DirManager:
    def __init__(self, id, base_path):
        self.target_dir = os.path.join(base_path, id)
        self.flame_dir_name = "flames"
        self.text_dir_name = "texts"
        

    def check_exit_dir(self):
        """指定されたディレクトリが存在するか確認する"""
        return os.path.exists(self.target_dir)

    def create_template_dir(self):
        """テンプレートディレクトリを作成する"""
        try:
            os.makedirs(self.target_dir, exist_ok=True)
            subdirs = [self.flame_dir_name, self.text_dir_name]
            for subdir in subdirs:
                os.makedirs(os.path.join(self.target_dir, subdir), exist_ok=True)
        except OSError as e:
            print(f"Error creating directory: {e}")
            raise e
        
    def get_target_path(self):
        return self.target_dir
    
    def get_flame_path(self):
        return f"{self.target_dir}/{self.flame_dir_name}"
    
    def get_text_path(self):
        return f"{self.target_dir}/{self.text_dir_name}"


if __name__ == "__main__":
    dm = DirManager("erbiu", "./output")
    if not dm.check_exit_dir():
        dm.create_template_dir()