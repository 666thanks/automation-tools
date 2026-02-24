import argparse
from pathlib import Path
import json
import time

BACKUP_FOLDER=Path(__file__).resolve().parent.parent / "backup"

def backup_mapping(mapping):
    """保存重命名前后的映射，用于回滚"""
    BACKUP_FOLDER.mkdir(parents=True,exist_ok=True)
    timestamp=time.strftime("%Y%m%d_%H%M%S")
    backup_file=BACKUP_FOLDER / f"backup_{timestamp}.json"
    
    with open(backup_file,"w",encoding="utf-8") as f:
        json.dump(mapping,f, ensure_ascii=False,indent=2)
        
    return backup_file

def batch_rename(folder:Path,prefix:str):
    files=[f for f in folder.iterdir() if f.is_file()]
    files.sort()
    
    mapping={}
    for idx, file in enumerate(files,start=1):
        ext=file.suffix
        new_name=f"{prefix}_{idx}{ext}"
        new_path=folder / new_name
        
        mapping[str(file)]=str(new_path)
        file.rename(new_path)
    
    backup_file=backup_mapping(mapping)
    print(f"重命名完成！备份文件生成：{backup_file}")
    
          
def rollback(backup_file:Path):
    """回滚重命名"""
    with open (backup_file,"r",encoding="utf-8") as f:
        mapping=json.load(f)
        
    for old, new in mapping.items():
        old_path=Path(old)
        new_path=Path(new)
        if new_path.exists():
            new_path.rename(old_path)
    
    print("回滚完成！")
    

def main():
    parser=argparse.ArgumentParser(description="批量重命名工具：支持回滚")
    parser.add_argument("--folder",required=True,help="文件夹路径")
    parser.add_argument("--prefix",help="重命名前缀")
    parser.add_argument("--rollback",help="回滚备份文件路径")
    
    args=parser.parse_args()
    
    folder=Path(args.folder)
    
    if args.rollback:
        rollback(Path(args.rollback))
    else:
        if not args.prefix:
            raise ValueError("执行重命名时必须指定--prefix")
        batch_rename(folder,args.prefix)
        
if __name__=="__main__":
    main()