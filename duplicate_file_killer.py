import os
import hashlib
import logging


class duplicate_file_killer:
    """删除重复文件
    """
    file_hash_list = []

    def __init__(self, Dir: str):
        self._get_file_hash_list(Dir)

    def _file_hash(self, file_path: str, hash_method=hashlib.md5()) -> str:
        "生成文件hash"
        if not os.path.isfile(file_path):
            logging.warning("文件不存在，路径：{}".format(file_path))
            return ""
        h = hash_method
        with open(file_path, 'rb')as fp:
            while b := fp.read(8192):
                h.update(b)
        return h.hexdigest()

    def _get_file_hash_list(self,Dir):
        """获取文件夹内所有文件的MD5值，并以此为特征，计算重复值
        return 
        List[
            Dict{
                file_hash:str
                file_name:str
                file_path_list:List[str]
                file_path_list_len:int
            },
            {}
        ...]

        """
        file_hash_dict = {}
        for root, dirs, files in os.walk(Dir):
            for f in files:
                file_path = os.path.join(root, f)
                file_md5 = self._file_hash(file_path, hashlib.md5())
                if file_md5 not in file_hash_dict:
                    file_hash_dict[file_md5] = {
                        'file_hash': None,
                        'file_name_list': [],
                        'file_path_list': [],
                        'file_path_list_len': 0,
                    }
                file_hash_dict[file_md5]['file_hash'] = file_md5
                file_hash_dict[file_md5]['file_name_list'].append(f)
                file_hash_dict[file_md5]['file_path_list'].append(file_path)
                file_hash_dict[file_md5]['file_path_list_len'] += 1
        file_hash_list = []

        for file_md5 in file_hash_dict:
            file_hash_list.append(file_hash_dict[file_md5])

        def sort_key(data):
            return data['file_path_list_len']
        file_hash_list.sort(key=sort_key, reverse=True)
        self.file_hash_list = file_hash_list

    def list_info(self,num: int):
        "列出重复量大于等于num的文件"
        file_hash_list=self.file_hash_list
        print(
                "{:<5s}".format('num'),
                "{:<35s}".format('file_hash'),
                "{:<4s}".format('file_num'),
                "{:{chr}<32.29s}".format('file_name',chr = chr(12288)),
                
                # "{file_path:<4s}".format(**data),
                )
        for i in range(len(file_hash_list)):
            data =  {
                    'num':i+1,
                    'file_hash':file_hash_list[i]['file_hash'],
                    'file_name':file_hash_list[i]['file_name_list'][0],
                    'file_num':file_hash_list[i]['file_path_list_len'],
                    'file_path':str(file_hash_list[i]['file_path_list']),
                }

            
        
            if file_hash_list[i]['file_path_list_len'] >= num:
                print(
                        "{num:<5d}".format(**data),
                        "{file_hash:<35s}".format(**data),
                        "{file_num:<4d}".format(**data),
                        "{file_name:{chr}<32.29s}".format(chr = chr(12288),**data),
                        
                        # "{file_path:<4s}".format(**data),

                )
   
    def file_killer(self,num:int,killer_type:int)->None:
        """
        删除重复值大于等于num的文件
        killer_type:
            0:完全删除，一个都不保留
            1:保留一个，删除其他的
            
        """
        file_hash_list=self.file_hash_list
        if killer_type==1:
            '删除重复文件,但保留1个'
            for i in range(len(file_hash_list)):
                if file_hash_list[i]['file_path_list_len'] >= num:
                    for index,file_path in enumerate(file_hash_list[i]['file_path_list']):
                        if index==0:continue
                        self._delete_file(file_path)

        if killer_type==0:
            '完全删除重复文件'
            for i in range(len(file_hash_list)):
                if file_hash_list[i]['file_path_list_len'] >= num:
                    for file_path in file_hash_list[i]['file_path_list']:
                         self._delete_file(file_path)
    
    def _delete_file(self, dic):
        if os.path.exists(dic):
            os.remove(dic)
        else:
            print("The file does not exist")

