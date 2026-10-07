from __future__ import annotations
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


def train_model(X, y):
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(n_estimators=250, max_depth=6, min_samples_leaf=2, random_state=42, class_weight="balanced")),
    ])
    model.fit(X,y)
    return model

def probabilities(model, X):
    raw=model.predict_proba(X)[0]
    classes=model.named_steps["classifier"].classes_
    out={c:float(p) for c,p in zip(classes,raw)}
    return {"home":out.get("H",0.0),"draw":out.get("D",0.0),"away":out.get("A",0.0)}
