[CSV/JSON 주문 데이터 / 운영 PostgreSQL DB] -> [ETL 과정] -> [데이터 웨어하우스] -> [분석/시각화]

- ETL 과정
  - 데이터 추출 (Extract)
  - 데이터 정제 / 변환 (Transform)
  - DW 적재 (Load)
- 데이터 웨어하우스
  - Fact: 주문
  - Dimension: 고객, 상품, 시간
- 고객별 구매 패턴, 인기 상품, 월별 매출 추이

터미널 실행 명령어 
pip install pandas sqlalchemy psycopg2-binary
pip install google-cloud-bigquery

추출 (E)	PostgreSQL에 접속하여 로우 데이터를 df로 가져옴.	sqlalchemy, psycopg2, pandas.read_sql
변환 (T)	df에서 중복/음수 제거, total_price 및 날짜 차원 생성.	pandas
적재 (L)	analysis_df를 BigQuery의 최종 분석 테이블로 업로드.	google-cloud-bigquery
