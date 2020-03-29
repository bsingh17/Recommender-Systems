import numpy as np
import pandas as pd

credit=pd.read_csv('tmdb_5000_credits.csv')
movies=pd.read_csv('tmdb_5000_movies.csv')

#DATA PREPROCESSING
credits_rename=credit.rename(index=str,columns={"movie_id":"id"})
movies=movies.merge(credits_rename,on='id')
movies=movies.drop(['homepage','title_x','title_y','status','production_countries'],axis='columns')

#NOW CALCUALTING WEIGHTED AVERAGE FOR EACH MOVIE RATING
v=movies['vote_count']
R=movies['vote_average']
C=movies['vote_average'].mean()
m=movies['vote_count'].quantile(0.70)

movies['weighted_average']=((R*v)+(C*m))/(v+m)

movies=movies.sort_values('weighted_average',ascending=False)


#PLotting the curve
import matplotlib.pyplot as plt
import seaborn as sns
weight_average=movies.sort_values('weighted_average',ascending=False)
plt.figure(figsize=(12,6))
axis1=sns.barplot(x=weight_average['weighted_average'].head(10), y=weight_average['original_title'].head(10), data=weight_average)
plt.xlim(4, 10)
plt.title('Best Movies by average votes', weight='bold')
plt.xlabel('Weighted Average Score', weight='bold')
plt.ylabel('Movie Title', weight='bold')
plt.savefig('best_movies.png')