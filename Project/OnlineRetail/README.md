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

