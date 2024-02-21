import load_pdf
import csv
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FuncFormatter
def write_to_csv(billing_data):
    # CSV 파일명
    csv_file = "invoices.csv"

    # 헤더를 결정(JSON의 키에서)
    header = billing_data[0].keys()

    # CSV 파일을 쓰기 모드로 열어 데이터를 쓰기
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(billing_data)

def main():
    # data 폴더의 모든 PDF 파일을 읽어 JSON 형식의 데이터를 받음
    billing_data = load_pdf.load_all_pdfs("data")
    print("読み込みが完了しました")

    # JSON 형식의 데이터를 CSV 파일로 작성
    write_to_csv(billing_data)
    print("CSV 파일 쓰기가 완료되었습니다")

if __name__ == "__main__":
    main()
