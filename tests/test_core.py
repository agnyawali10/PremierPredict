from app.data import sample_data
from ml.features import build_training_frame
from ml.model import train_model, probabilities
from ml.simulation import simulate

def test_pipeline():
    matches,fixtures=sample_data(); X,y,stats=build_training_frame(matches); model=train_model(X,y)
    result=simulate(model,stats,fixtures,n=100,seed=1)
    assert len(result)==20
    assert all(1 <= r["predicted_position"] <= 20 for r in result)
    assert all(0 <= r["top4_probability"] <= 100 for r in result)
