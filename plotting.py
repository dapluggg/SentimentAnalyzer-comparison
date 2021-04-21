#%%
import pandas as pd
from plotnine import *
from plotnine.labels import xlab
import json
import matplotlib.pyplot as plt
import seaborn as sn
# ggplot, aes, geom_boxplot, scale_y_log10, coord_flip, theme, element_blank
#%%
results = pd.read_csv('./data-extended/tweets-results.csv',
                             parse_dates=['date', 'created_at'])
#%%
VADER_corrected = []
for result_dict in results['VADER']:
    result_parsed = eval(result_dict)
    if result_parsed['compound'] > 0:
        thisresult = 'POSITIVE'
    elif result_parsed['compound'] == 0:
        thisresult = 'NEUTRAL'
    else:
        thisresult = 'NEGATIVE' 
    VADER_corrected.append(thisresult)
    
results['VADER_corrected'] = VADER_corrected
#%%
Flair_corrected = []
for result_string in results['Flair']:
    if 'POSITIVE' in result_string:
        thisresult = 'POSITIVE'
    elif 'NEGATIVE' in result_string:
        thisresult = 'NEGATIVE'
    Flair_corrected.append(thisresult)
results['Flair_Corrected'] = Flair_corrected
#%%
# Likes by Username
(
    ggplot(results) +
    aes(y="likes_count", x="username") +
    geom_boxplot() +
    scale_y_log10()+
    coord_flip()
)
# %%
# Likes by Username
(
    ggplot(results) +
    aes(y="retweets_count", x=0) +
    geom_boxplot() +
    scale_y_log10() +
    theme(axis_text_y = element_blank()) +
    xlab('') +
    coord_flip()
)
# %%
confusion_mat = pd.crosstab(results['VADER_corrected'], 
                            results['Flair_Corrected'])
conf_plot = sn.heatmap(confusion_mat, annot=True, fmt='d')
conf_plot
# %%
