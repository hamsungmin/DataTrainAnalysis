import pandas as pd
from sqlalchemy import create_engine
from google.cloud import bigquery

# 1. PostgreSQL 연결 설정
#python 파일에서 PostgreSQL 연결 설정
PG_USER = "gamlog"
PG_PASSWORD = "gamlog1100!"
PG_HOST = "127.0.0.1"
PG_PORT = "5432"
PG_DATABASE = "gamlog_db"

# SQLAlchemy 연결 문자열 생성
try:
    pg_engine = create_engine(
        f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
    )
    print("PostgreSQL 연결 엔진 생성 성공.")
except Exception as e:
    print(f"연결 엔진 생성 오류: {e}")
    exit()

# ------------------------------------------------------------------------------
#2. 데이터 추출(SQL 실행)
SQL_QUERY = """
SELECT
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country"
FROM
    online_retail;
"""

# SQL 쿼리를 실행하고 데이터를 Pandas DataFrame으로 읽어오기
try:
    df = pd.read_sql(SQL_QUERY, pg_engine)
    print(f"데이터 추출 완료! 가져온 로우 수: {len(df)}")
    print("[추출된 데이터 미리보기]")
    print(df.head())

except Exception as e:
    print(f"PostgreSQL 데이터 추출 오류: {e}")
    exit()

# ------------------------------------------------------------------------------
# 3. 데이터 변환(데이터 정제 및 가공)
# 중복 제거
# DataFrame 전체 행이 동일한 경우에만 제거
df.drop_duplicates(inplace=True)
print(f"1. 중복 제거 완료. 남은 로우 수: {len(df)}")

#2. 음수 Quantity 처리 (Negative Value Handling)
# Quantity 0 이상인 행만 필터링하여 남깁니다.
df = df[df["Quantity"] >= 0]
print(f"2. 음수 Quantity 제거 완료. 남은 로우 수: {len(df)}")

#3. 수익 컬럼 (total_price) 생성
# 'TotalPrice' = 'Quantity' * 'Quantity'
df["TotalPrice"] = df["Quantity"] * df["Quantity"]
print("3. 수익 컬럼 (TotalPrice) 생성 완료.")

#4. 날짜 관련 차원 생성
# invoice_date를 datetime 객체로 변환 (변환 전에 에러가 나지 않도록 error='coerce' 사용)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors='coerce')

# 날짜 (Date) 부분만 추출하여 새로운 컬럼 생성
df["Date"] = df["InvoiceDate"].dt.date

# (선택 사항) 분석에 유용한 추가 차원 생성 (예: 연-월)
df["YearMonth"] = df["InvoiceDate"].dt.strftime("%Y-%m")

print("4. 날짜 관련 차원 (Date, YearMonth) 생성 완료.")

#최종 DataFrame 준비 및 미리보기
# 5. BigQuery 적재용 최종 컬럼 선택 및 DataFrame 확정
analysis_df = df[[
    "InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice",
    "CustomerID", "Country", "InvoiceDate", "Date", "YearMonth", "TotalPrice"
]]

print("--- 최종 변환된 데이터 미리보기 (analysis_df) ---")
print(analysis_df.head())

# 변환된 데이터의 자료형 확인 (BigQuery 적재 시 중요)
print("[컬럼별 자료형 (Dtype)]")
print(analysis_df.info())

# DimProduct (상품 정보)
dim_product_df = analysis_df[['StockCode', 'Description', 'UnitPrice']].drop_duplicates(subset=['StockCode']).reset_index(drop=True)

# DimCustomer (고객 정보)
dim_customer_df = analysis_df[['CustomerID', 'Country']].drop_duplicates(subset=['CustomerID']).reset_index(drop=True)
# *참고: DimCountry를 별도로 분리하려면 이 단계에서 country_id를 생성해야 합니다.

# FactSales 테이블 생성 준비
fact_sales_df = analysis_df[[
    'InvoiceNo',
    'StockCode',
    'CustomerID',
    'Date',
    'Quantity',
    'TotalPrice'
]]

# *참고: DimCountry를 별도로 만들었다면, country 대신 country_id를 Fact 테이블에 추가해야 합니다.
# ------------------------------------------------------------------------------
# 4. BigQuery 적재
# --- 1. BigQuery 연결 및 대상 정의 ---
# 실제 GCP 정보로 대체해야 합니다.
BQ_PROJECT = "onlineretail-478205"
BQ_DATASET = "onlineretail_dataset"  # 예: sales_data

client = bigquery.Client(project=BQ_PROJECT)
try:
    # WRITE_APPEND: 테이블이 있으면 데이터 추가
    # WRITE_TRUNCATE: 테이블을 덮어쓰고 기존 데이터 삭제
    # WRITE_EMPTY: 테이블이 비어있을 때만 적재 허용

    # --- 1. DimProduct 테이블 적재 ---
    table_id_product = f"{BQ_PROJECT}.{BQ_DATASET}.DimProduct"
    client.load_table_from_dataframe(
        dim_product_df,
        table_id_product,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE") # 매번 덮어쓰기
    ).result()
    print(f"대상 BigQuery 테이블: {table_id_product}")

    # --- 2. DimCustomer 테이블 적재 ---
    table_id_customer = f"{BQ_PROJECT}.{BQ_DATASET}.DimCustomer"
    client.load_table_from_dataframe(
        dim_customer_df,
        table_id_customer,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    ).result()
    print(f"대상 BigQuery 테이블: {table_id_customer}")

    # ... (DimDate, DimCountry도 동일하게 반복) ...

    # --- 3. FactSales 테이블 적재 ---
    table_id_sales = f"{BQ_PROJECT}.{BQ_DATASET}.FactSales"
    client.load_table_from_dataframe(
        fact_sales_df, 
        table_id_sales, 
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND") # 또는 TRUNCATE
    ).result()

    print(f"대상 BigQuery 테이블: {table_id_sales}")
    print(" 데이터 BigQuery 적재 성공!")

except Exception as e:
    print(f" BigQuery 데이터 적재 오류 발생: {e}")
