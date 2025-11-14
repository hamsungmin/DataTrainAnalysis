[CSV/JSON 주문 데이터 / 운영 PostgreSQL DB] -> [ETL 과정] -> [데이터 웨어하우스] -> [분석/시각화]

- ETL 과정
  - 데이터 추출 (Extract)
  - 데이터 정제 / 변환 (Transform)
  - DW 적재 (Load)
- 데이터 웨어하우스
  - FactSales: 주문
  - DimCustomer: 고객, 국가
  - DimProduct: 상품 정보
- 고객별 구매 패턴, 인기 상품, 월별 매출 추이

터미널 실행 명령어 
pip install pandas sqlalchemy psycopg2-binary
pip install google-cloud-bigquery
pip install pyarrow

추출 (E)	PostgreSQL에 접속하여 로우 데이터를 df로 가져옴.	sqlalchemy, psycopg2, pandas.read_sql

변환 (T)	df에서 중복/음수 제거, total_price 및 날짜 차원 생성.	pandas

적재 (L)	analysis_df를 BigQuery의 최종 분석 테이블로 업로드.	google-cloud-bigquery

빅쿼리에서 SQL 진행하여 데이터 확인

- 상품별 매출 TOP 10 쿼리 실행
  ​
  ```
  SELECT 
      p.Description, 
      SUM(f.TotalPrice) AS revenue
  FROM 
      onlineretail-478205.onlineretail_dataset.FactSales f  -- Fact 테이블
  JOIN 
      onlineretail-478205.onlineretail_dataset.DimProduct p  -- Dimension 테이블
      ON f.StockCode = p.StockCode
  WHERE p.Description != ''
  GROUP BY 
      1 -- description
  ORDER BY 
      revenue DESC
  LIMIT 10;

- 국가별 일일 매출 쿼리 실행
​
  ```
  SELECT 
      f.Date AS date, -- Fact 테이블에 date를 키로 사용했다고 가정
      dc.Country, 
      SUM(f.TotalPrice) AS daily_revenue
  FROM 
      onlineretail-478205.onlineretail_dataset.FactSales f 
  JOIN 
      onlineretail-478205.onlineretail_dataset.DimCustomer dc -- 고객 테이블에 country가 있다면
      ON f.CustomerID = dc.CustomerID
  WHERE f.Date is not null
  GROUP BY 
      1, 2
  ORDER BY 
      1;
