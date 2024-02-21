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

def draw_graph(filename):
    # invoices.csvファイルからpandasのDataFrameに読み込み（数値のカンマ区切りに対応）
    df = pd.read_csv("invoices.csv", thousands=",")

    # 日付のフォーマットを変換
    df["日付"] = pd.to_datetime(
        df["日付"].str.replace("年", "-").str.replace("月", "-").str.replace("日", ""),
        format="%Y-%m-%d",
    )

    # グラフを描画
    fig, ax = plt.subplots()
    ax.bar(df["日付"], df["請求金額（合計）"])
    ax.set_xlabel("date")
    ax.set_ylabel("price")
    ax.set_xticks(df["日付"])
    ax.set_xticklabels(df["日付"].dt.strftime("%Y-%m-%d"), rotation=45)

    # y軸の最小値を0に設定
    ax.set_ylim(0, max(df["請求金額（合計）"]) + 100000)

    # 縦軸のラベルを元の数字のまま表示
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    plt.tight_layout()
    plt.show()


def main():
    # 「data」フォルダ以下のPDFファイルを読み込み、json形式のデータを受け取る
    billing_data = load_pdf.load_all_pdfs("data")
    print("読み込みが完了しました")

    # json形式のデータをCSVファイルに書き込む
    write_to_csv(billing_data)
    print("CSVファイルへの書き込みが完了しました")

    draw_graph("invoices.csv")


if __name__ == "__main__":
    main()
