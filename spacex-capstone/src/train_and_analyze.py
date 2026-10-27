from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import pandas as pd,numpy as np,json,sqlite3,hashlib,sklearn
from sklearn.model_selection import train_test_split,StratifiedKFold,GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score,recall_score,f1_score
D=pd.read_csv(str(ROOT/'data/dataset_part_2.csv')); S=pd.read_csv(str(ROOT/'data/Spacex.csv')); A=pd.read_csv(str(ROOT/'data/spacex_launch_dash.csv')); G=pd.read_csv(str(ROOT/'data/spacex_launch_geo.csv'))
con=sqlite3.connect(str(ROOT/'results/spacex.db'));S.to_sql('launches',con,index=False,if_exists='replace')
queries=["SELECT DISTINCT Launch_Site FROM launches ORDER BY Launch_Site", "SELECT Date,Booster_Version,Launch_Site FROM launches WHERE Launch_Site LIKE 'CCA%' ORDER BY Date LIMIT 5", "SELECT SUM(PAYLOAD_MASS__KG_) AS kg FROM launches WHERE Customer='NASA (CRS)'", "SELECT AVG(PAYLOAD_MASS__KG_) AS kg FROM launches WHERE Booster_Version LIKE 'F9 v1.1%'", "SELECT MIN(Date) AS Date FROM launches WHERE Landing_Outcome='Success (ground pad)'", "SELECT DISTINCT Booster_Version FROM launches WHERE Landing_Outcome='Success (drone ship)' AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000", "SELECT TRIM(Mission_Outcome) AS Mission_Outcome,COUNT(*) AS n FROM launches GROUP BY TRIM(Mission_Outcome)", "SELECT Booster_Version,PAYLOAD_MASS__KG_ FROM launches WHERE PAYLOAD_MASS__KG_=(SELECT MAX(PAYLOAD_MASS__KG_) FROM launches)", "SELECT Date,Booster_Version,Launch_Site FROM launches WHERE Date LIKE '2015%' AND Landing_Outcome='Failure (drone ship)'", "SELECT Landing_Outcome,COUNT(*) AS n FROM launches WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY n DESC"]
res={'sql':[{'query':q,'rows':pd.read_sql_query(q,con).to_dict('records')} for q in queries]}
num=['FlightNumber','PayloadMass','Flights','Block','ReusedCount'];cat=['Orbit','LaunchSite','GridFins','Reused','Legs']
X=D[num+cat];y=D.Class
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
prep=ColumnTransformer([('num',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),num),('cat',OneHotEncoder(handle_unknown='ignore'),cat)])
cv=StratifiedKFold(5,shuffle=True,random_state=42)
models=[('Logistic regression',LogisticRegression(max_iter=3000),{'model__C':[.01,.1,1,10,100]}),('SVM',SVC(),{'model__C':[.1,1,10,100],'model__kernel':['linear','rbf'],'model__gamma':['scale',.01,.1]}),('Decision tree',DecisionTreeClassifier(random_state=42),{'model__max_depth':[2,3,4,5,None],'model__min_samples_leaf':[1,2,4],'model__criterion':['gini','entropy']}),('KNN',KNeighborsClassifier(),{'model__n_neighbors':[3,5,7,9],'model__weights':['uniform','distance'],'model__p':[1,2]})]
res['ml']=[]
for name,model,params in models:
 search=GridSearchCV(Pipeline([('prep',prep),('model',model)]),params,cv=cv,scoring='accuracy',n_jobs=1).fit(Xtr,ytr); pred=search.predict(Xte)
 res['ml'].append(dict(name=name,cv=search.best_score_,cvstd=search.cv_results_['std_test_score'][search.best_index_],test=accuracy_score(yte,pred),precision=precision_score(yte,pred),recall=recall_score(yte,pred),f1=f1_score(yte,pred),cm=confusion_matrix(yte,pred).tolist(),params=search.best_params_))
res.update(rows=len(D),date=[D.Date.min(),D.Date.max()],outcomes=D.Outcome.value_counts().to_dict(),site=D.groupby('LaunchSite').Class.agg(['sum','count','mean']).reset_index().to_dict('records'),orbit=D.groupby('Orbit').Class.agg(['sum','count','mean']).reset_index().to_dict('records'),year=D.assign(Year=D.Date.str[:4]).groupby('Year').Class.agg(['sum','count','mean']).reset_index().to_dict('records'),dash=A.groupby('Launch Site')['class'].agg(['sum','count','mean']).reset_index().to_dict('records'),versions=A.groupby('Booster Version Category')['class'].agg(['sum','count','mean']).reset_index().to_dict('records'),sklearn=sklearn.__version__,train_ids=D.loc[Xtr.index,'FlightNumber'].tolist(),test_ids=D.loc[Xte.index,'FlightNumber'].tolist(),data=D.to_dict('records'))
open(str(ROOT/'results/analysis_results.json'),'w').write(json.dumps(res,indent=2,default=str));print(json.dumps({k:v for k,v in res.items() if k not in ['data','train_ids','test_ids']},indent=2))
