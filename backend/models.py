"""

USERS
id	INTEGER/SERIAL PK
email VARCHAR(255)
password_hash VARCHAR(255)
created_at TIMESTAMP

USER DATA
id	INTEGER/SERIAL PK
user_id	FK - users (1:1)
Sex	Bool
Age	Int
HighBP Bool
HighChol Bool
CholCheck Bool
Smoker Bool
Stroke Bool
HeartDisease Bool
AnyHealthcare Bool
NoDocbcCost	Bool
DiffWalk Bool


LOGS (te dane sie licza dzisiejszego dnia)
id	INTEGER/SERIAL PK
user_id	FK - users (N:1)
log_date Date
ate_fruit Bool
ate_veggie Bool
physical_activity Bool
alcohol_drinks Int
bad_mental_day Bool
bad_physical_day Bool
weight Decimal
height Decimal

HISTORY
id INTEGER/SERIAL PK
user_id FK - users (N:1)
created_at TIMESTAMP
result INTEGER
probability FLOAT
input_snapshot JSON


"""

