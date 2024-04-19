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
    with open(output_filename, "w", encoding="utf-8", newline="") as output_file:
        # ヘッダーを書き込む
        writer = csv.writer(output_file)
        writer.writerow(["question","ground_truth","context","answer"])
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
                print("context: ", "出力が長いため表示は省略してcsv書き込みのみ実行")
                print("answer: ", answer)
                # 生成した回答と正解をcsvに書き込む
                writer.writerow([row[0], row[1], context, answer])
                


if __name__ == '__main__':
    # コマンドライン引数で評価用csvのpathを受け取る
    path = sys.argv[1]
    main(path)


