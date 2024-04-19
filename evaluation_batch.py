from approach import rag_approach
#from approach import rag_with_image_approach
import csv
import sys

import datetime
output_filename = datetime.datetime.now().strftime("evaluation_%Y%m%d%H%M%S") + ".csv"

def main(path: str):
    """
    画像以外の35問に対して、RAGアプローチで回答を生成する
    """
    with open(output_filename, "w", encoding="utf-8") as output_file:
        # ヘッダーを書き込む
        output_file.write("question,ground_truth,context,answer\n")
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            # ヘッダーをスキップ
            next(reader)
            for row in reader:
                print(row)
                question = row[0]
                ground_truth = row[1]
                print("question: ", question)
                print("ground_truth: ", ground_truth)
                context, answer = rag_approach(question)
                conetxt = context.replace("\n", " ")
                answer = answer.replace("\n", " ")
                # 生成した回答と正解をcsvに書き込む
                output_file.write(f"\"{question}\",\"{ground_truth}\",\"{context}\",\"{answer}\"\n")
                break


if __name__ == '__main__':
    # コマンドライン引数で評価用csvのpathを受け取る
    path = sys.argv[1]
    main(path)


