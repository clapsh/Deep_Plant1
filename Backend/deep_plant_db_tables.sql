-- PostgreSQL
CREATE TABLE meat ( -- 육류 데이터 저장 DB
  id VARCHAR PRIMARY KEY, -- 관리 번호 (현재 정책: "이력(묶음)번호-종-대분할-소분할-index")
  email VARCHAR NOT NULL, -- 관리 번호 생성 유저 email
  saveTime VARCHAR NOT NULL, -- 관리 번호 생성 시간 "ISO 8601 형식"
  traceNumber VARCHAR NOT NULL, -- 육류 이력(묶음) 번호
  species VARCHAR NOT NULL, -- 육류 종 (pig, meat)
  l_division VARCHAR NOT NULL, -- 육류 대분류
  s_division VARCHAR NOT NULL, -- 육류 소분류
  gradeNm VARCHAR NOT NULL, -- 육류 등급
  farmAddr VARCHAR NOT NULL, -- 육류 농장 주소
  butcheryPlaceNm VARCHAR NOT NULL, -- 육류 도축장명
  butcheryYmd VARCHAR NOT NULL -- 육류 도축 일자 (20170920 형식)
);

CREATE TABLE deep_aging ( -- 딥에이징 이력 저장 DB
  id VARCHAR PRIMARY KEY, -- 관리 번호 (현재 정책: "이력(묶음)번호-종-대분할-소분할-index")
  period BYTEA, -- 딥에이징 이력 저장 (현재 형식: "딥에이징년도/월/일/시간(분)") (예시: 120분 60분 총 2회 실행 -> ["2023/04/21/120","2023/05/06/60"])
  FOREIGN KEY (id) REFERENCES meat (id) 
);

CREATE TABLE fresh ( -- 신선육 관능 검사 데이터 저장 DB
  id VARCHAR PRIMARY KEY, -- 관리 번호 (현재 정책: "이력(묶음)번호-종-대분할-소분할-index")
  marbling FLOAT, 
  color FLOAT, 
  texture FLOAT,
  surfaceMoisture FLOAT,
  total FLOAT,
  FOREIGN KEY (id) REFERENCES meat (id)
);

CREATE TABLE heated ( -- 가열육 관능 검사 데이터 저장 DB
  id VARCHAR PRIMARY KEY, -- 관리 번호 (현재 정책: "이력(묶음)번호-종-대분할-소분할-index")
  flavor FLOAT,
  juiciness FLOAT,
  tenderness FLOAT,
  umami FLOAT,
  palability FLOAT,
  FOREIGN KEY (id) REFERENCES meat (id)
);

CREATE TABLE tongue ( -- 전자혀 데이터 저장 DB
  id VARCHAR PRIMARY KEY, -- 관리 번호 (현재 정책: "이력(묶음)번호-종-대분할-소분할-index")
  sourness FLOAT,
  bitterness FLOAT,
  umami FLOAT,
  richness FLOAT,
  FOREIGN KEY (id) REFERENCES meat (id)
);

CREATE TABLE lab_data ( -- 실험 데이터 저장 DB
  id VARCHAR PRIMARY KEY, -- 관리 번호 (현재 정책: "이력(묶음)번호-종-대분할-소분할-index")
  L FLOAT,
  a FLOAT,
  b FLOAT,
  DL FLOAT,
  CL FLOAT,
  RW FLOAT,
  ph FLOAT,
  WBSF FLOAT,
  cardepsin_activity FLOAT,
  MFI FLOAT,
  FOREIGN KEY (id) REFERENCES meat (id)
);

CREATE TABLE user ( -- 유저 데이터 저장 DB   
  id VARCHAR PRIMARY KEY, -- 유저 id (현재 정책: 유저 email)
  lastLogin VARCHAR NOT NULL, -- 최근 로그인 이력 (ISO 8601 형식)
  name VARCHAR NOT NULL, -- 유저 이름
  company VARCHAR, -- 유저 회사 정보
  position VARCHAR, -- 유저 직함 정보
  type VARCHAR(50) -- 유저 타입 ("normal" - 일반 사용자, "researcher" - 연구원, "manager" - 관리자)
);

CREATE TABLE normal ( -- "일반 사용자" 데이터 저장 DB
  id VARCHAR PRIMARY KEY, -- 유저 id (현재 정책: 유저 email)
  FOREIGN KEY (id) REFERENCES "user" (id)
);

CREATE TABLE researcher ( -- "연구원" 데이터 저장 DB
  id VARCHAR PRIMARY KEY, -- 유저 id (현재 정책: 유저 email)
  FOREIGN KEY (id) REFERENCES "user" (id)
);

CREATE TABLE manager ( -- "관리자" 데이터 저장 DB
  id VARCHAR PRIMARY KEY, -- 유저 id (현재 정책: 유저 email)
  pwd VARCHAR NOT NULL, -- 관리자 비밀번호 (hashlib의 SHA256방식 암호화 이용)
  FOREIGN KEY (id) REFERENCES "user" (id)
);

CREATE TABLE meat_user ( -- 관리번호 생성 데이터 저장 DB
  meat_id VARCHAR REFERENCES meat (id), -- 육류의 관리번호 (현재 정책: "이력(묶음)번호-종-대분할-소분할-index")
  user_id VARCHAR REFERENCES normal (id), -- 해당 육류의 관리번호를 생성한 유저 id (현재 정책: 유저 email)
  PRIMARY KEY (meat_id, user_id)
);

CREATE TABLE meat_user2 ( -- 관리번호 수정(추가입력) 데이터 저장 DB
  meat_id VARCHAR REFERENCES meat (id),  -- 육류의 관리번호 (현재 정책: "이력(묶음)번호-종-대분할-소분할-index")
  user_id VARCHAR REFERENCES researcher (id),  -- 해당 육류에 데이터(전자혀 데이터, 실험 데이터, 가열육 데이터)를 추가적으로 입력한 유저 id (현재 정책: 유저 email)
  PRIMARY KEY (meat_id, user_id)
);
