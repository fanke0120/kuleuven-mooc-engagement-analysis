import json
import os
import xml.etree.ElementTree as ET

def process_json(input_path, output_path, video_dir):
    print ("qwq1")

    # 读取原始JSON文件
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print ("qwq2")
    
    # 遍历所有顶层键
    for key in list(data.keys()):
        # 分割键获取ID
        key_parts = key.split('@')
        if len(key_parts) < 3:
            print(f"警告：跳过格式错误的键 {key}")
            continue
            
        item_id = key_parts[2]
        item_data = data[key]
        
        # 检查是否为video类别
        if item_data.get('category') == 'video':
            # 构建XML文件路径
            xml_path = os.path.join(video_dir, f"{item_id}.xml")
            
            # 验证XML文件存在性
            if not os.path.isfile(xml_path):
                raise FileNotFoundError(f"未找到视频ID {item_id} 对应的XML文件：{xml_path}")
            
            # 解析XML文件
            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()
                video_id = root [0].attrib.get('client_video_id')
                
                if not video_id:
                    raise ValueError(f"XML文件中缺失client_video_id属性：{xml_path}")
                
                video_id = video_id.removesuffix('.mp4')
                video_id = video_id.removesuffix('.mp')
                video_id = video_id.removesuffix('.m')
                
                # 更新metadata数据
                # item_data['metadata']['client_video_id'] = video_id
                item_data['metadata']['display_name'] = video_id
            except ET.ParseError:
                raise ValueError(f"XML文件解析失败：{xml_path}")
    
    # 写入新JSON文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=True, sort_keys=True)

if __name__ == "__main__":
    # 配置路径参数
    input_json = "EUROGOVx/KULeuvenX-EUROGOVx-1T2023-course_structure-prod-analytics.json"       # 原始JSON文件路径
    output_json = "EUROGOVx/rep_KULeuvenX-EUROGOVx-1T2023-course_structure-prod-analytics.json"     # 输出JSON文件路径
    video_folder = "EUROGOVx/video"          # 视频XML文件目录
    
    # 执行处理流程
    try:
        process_json(input_json, output_json, video_folder)
        print("处理成功，结果已保存至", output_json)
    except Exception as e:
        print("处理过程中发生错误:", str(e))