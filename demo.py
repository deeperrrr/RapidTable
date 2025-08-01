# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapidocr import EngineType, RapidOCR

from rapid_table import ModelType, RapidTable, RapidTableInput

ocr_engine = RapidOCR(
    params={
        "Det.engine_type": EngineType.TORCH,
        "Cls.engine_type": EngineType.TORCH,
        "Rec.engine_type": EngineType.TORCH,
    }
)

input_args = RapidTableInput(model_type=ModelType.UNITABLE)
table_engine = RapidTable(input_args)

img_path = "https://raw.githubusercontent.com/RapidAI/RapidTable/refs/heads/main/tests/test_files/table.jpg"

# # 使用单字识别
# ori_ocr_res = ocr_engine(img_path, return_word_box=True)
# ocr_results = [
#     [word_result[0][2], word_result[0][0], word_result[0][1]]
#     for word_result in ori_ocr_res.word_results
# ]
# ocr_results = list(zip(*ocr_results))

ori_ocr_res = ocr_engine(img_path)
ocr_results = [ori_ocr_res.boxes, ori_ocr_res.txts, ori_ocr_res.scores]
results = table_engine(img_path, ocr_results=ocr_results)
results.vis(save_dir="outputs", save_name="vis")
