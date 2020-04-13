import numpy as np
import pandas as pd
from libpyhat.examples import get_path
import libpyhat.regression.sm as sm
import libpyhat.regression.regression as reg

def test_sm_blend():
    df = pd.read_csv(get_path('test_data.csv'), header=[0, 1])
    x = df['wvl']
    y = df[('comp','SiO2')]

    model1 = reg.regression(method=['PLS'], params=[{'n_components': 3, 'scale': False}])
    model1.fit(x, y)
    df[('predict','model1')] = model1.predict(x)

    model2 = reg.regression(method=['PLS'], params=[{'n_components': 5, 'scale': False}])
    model2.fit(x, y)
    df[('predict','model2')] = model2.predict(x)

    model3 = reg.regression(method=['PLS'], params=[{'n_components': 4, 'scale': False}])
    model3.fit(x, y)
    df[('predict','model3')] = model3.predict(x)

    predictions = [df[('predict','model2')],df[('predict','model1')],df[('predict','model3')],df[('predict','model1')]]

    blendranges = [[-9999,30],[20,60],[50,9999]]
    sm_obj = sm.sm(blendranges)
    blended_predictions = sm_obj.do_blend(np.array(predictions)) #without optimization
    rmse = np.sqrt(np.average((blended_predictions - df[('comp', 'SiO2')]) ** 2))
    assert rmse==12.703434300128926

    blended_predictions = sm_obj.do_blend(np.array(predictions),truevals=np.array(df[('comp','SiO2')])) #with optimization
    rmse = np.sqrt(np.average((blended_predictions-df[('comp','SiO2')])**2))
    expected_blendranges = [-9999., 36.5198746, 47.98157746, 56.2537253, 118.94036468, 9999.]
    assert rmse==9.954065130533083
    np.testing.assert_array_almost_equal(expected_blendranges,sm_obj.blendranges)
