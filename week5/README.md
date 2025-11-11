# [Week 5] 콘크리트 압축 강도 예측 모델

**프로젝트 제목**
- 콘크리트 배합 요소를 활용한 압축 강도 예측 회귀 모델링

**핵심 주제**
- 회귀(Regression) 기반 예측 모델
- 재료 구성 요소가 강도에 미치는 영향 분석
- 머신러닝을 활용한 실측값 예측

**사용 데이터**
- Concrete Compressive Strength Dataset
- 구성 컬럼 예시: Cement, Slag, Fly Ash, Water, Superplasticizer, Coarse Aggregate, Fine Aggregate, Age 등

**사용 기술 / 라이브러리**
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

**분석·모델링 내용 요약**
- 데이터 탐색: 분포 확인, 상관관계 분석
- 데이터 전처리: 정규화/스케일링 적용 가능
- 모델 구축:
  - 선형 회귀(Linear Regression)
  - 랜덤 포레스트 회귀(RandomForestRegressor)
  - 의사결정나무(DecisionTreeRegressor)
- 모델 평가: RMSE, MAE, R² 등
- 중요 변수 분석(Feature Importance)

**결과/성과**
- 머신러닝 회귀 모델을 통한 콘크리트 강도 예측 성공
- 재료별 강도 기여도 및 영향도 파악 가능

EDA → 모델링 → 평가의 전 과정을 갖춘 완성형 ML 프로젝트

이후 Week 6, 7과 함께 ML·DL 포트폴리오의 핵심 구성 요소로 활용 가능
