**1. data_generation.ipynb**
- 가상 유저 데이터 생성
- user_id, install_date, platform, country, session_count, total_spend, ad_source, retention_1d/7d/30d, cohort
- 광고 캠페인 A/B 테스트 데이터 생성
- pandas DataFrame → CSV 저장
- 출력: users.csv, ab_campaign.csv

**2. ltv_prediction.ipynb**
- 데이터 불러오기 + 전처리
- Feature Engineering
- 모델 학습: Linear Regression → RandomForest/XGBoost
- 교차검증, 하이퍼파라미터 튜닝
- Feature Importance 시각화
- 예측 결과 시각화 (실제 vs 예측)
- 출력: 예측 결과 + 시각화 그래프

**3. user_segmentation.ipynb**
- 코호트 분석
- K-means 클러스터링 (session_count, total_spend, retention)
- 클러스터별 유저 특성 분석
- 개인화 추천 전략 제안
- 출력: 클러스터별 분석 그래프, 추천 전략 요약

**4_ab_test_analysis.ipynb**
- 광고 캠페인 A/B 데이터 불러오기
- KPI 계산: installs, revenue
- 통계적 유의성 검증 (t-test, chi-square)
- 결과 시각화 (bar plot, p-value)
- 출력: A/B 테스트 분석 결과, 인사이트
