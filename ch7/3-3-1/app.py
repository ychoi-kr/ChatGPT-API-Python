import load_pdf
import csv
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
def write_to_csv(billing_data):
    # CSV 파일명
    csv_file = "invoices.csv"

    # 헤더를 결정 (JSON의 키에서)
    header = billing_data[0].keys()

    # CSV 파일을 쓰기 모드로 열어 데이터를 쓰기
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(billing_data)

def draw_graph(filename):
    # pandas의 DataFrame으로 'invoices.csv' 파일에서 데이터 읽기 (숫자의 콤마 구분에 대응)
    df = pd.read_csv("invoices.csv", thousands=",")

    # 날짜 형식 변환
    df["발행일"] = pd.to_datetime(
        df["발행일"].str.replace(" ", "").str.replace("년", "-").str.replace("월", "-").str.replace("일", ""),
        format="%Y-%m-%d",
    )

    # 그래프 그리기
    fig, ax = plt.subplots()
    ax.bar(df["발행일"], df["청구금액(총액)"])
    ax.set_xlabel("date")
    ax.set_ylabel("price")
    ax.set_xticks(df["발행일"])
    ax.set_xticklabels(df["발행일"].dt.strftime("%Y-%m-%d"), rotation=45)

    # y축의 최솟값을 0으로 설정
    ax.set_ylim(0, max(df["청구금액(총액)"]) + 100000)

    # y축 라벨을 원래 숫자로 표시
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ",")))

    plt.tight_layout()
    plt.show()


def main():
    # data 폴더 아래의 PDF 파일을 읽고 JSON 형태의 데이터 받기
    billing_data = load_pdf.load_all_pdfs("data")
    print("데이터 로드 완료")

    # JSON 형태의 데이터를 CSV 파일로 쓰기
    write_to_csv(billing_data)
    print("CSV 파일 쓰기 완료")

    draw_graph("invoices.csv")


if __name__ == "__main__":
    main()
