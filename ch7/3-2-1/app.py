import load_pdf
import csv
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FuncFormatter
def write_to_csv(billing_data):
    # CSVファイル名
    csv_file = "invoices.csv"

    # ヘッダーを決定（JSONのキーから）
    header = billing_data[0].keys()

    # CSVファイルを書き込みモードで開き、データを書き込む
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(billing_data)

def main():
    # 「data」フォルダ以下のPDFファイルを読み込み、json形式のデータを受け取る
    billing_data = load_pdf.load_all_pdfs("data")
    print("読み込みが完了しました")

    # json形式のデータをCSVファイルに書き込む
    write_to_csv(billing_data)
    print("CSVファイルへの書き込みが完了しました")

if __name__ == "__main__":
    main()
