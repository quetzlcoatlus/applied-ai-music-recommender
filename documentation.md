Algorithm Recipe: Set of rules system will use to score songs.

Collaborative filtering: A method of making automatic predictions about the interests of a user by collecting preferences from many users. Not viable for this project.

Content-based filtering: A method of making automatic predictions about the interests of a user by analyzing the content of items and the user's preferences. This is the primary method used in this project.

Going to be using content-based filtering using the energy, valence, danceability, and acousticness features of the dataset.

Need to use a Scoring Rule (for one song) and a Ranking Rule (for multiple songs).

Scoring Rule: A function that assigns a score to a song based on its features and the user's preferences. The score is used to rank the songs in the recommendation list. Absolute for a given user.

Ranking Rule: A function that takes the scores of multiple songs and ranks them in order of preference. The ranking is used to generate the final recommendation list for the user. Relative to other songs in the dataset. Additional rules like "diversity" can be used to ensure that the recommended songs are not too similar to each other, which can help to increase the novelty of the recommendations.

Separating these provides separation of concerns and allows for more flexibility in the recommendation system.

Proximity-Based Scoring Rule: A scoring rule that assigns a score to a song based on its proximity to the user's preferences in the feature space. The closer the song is to the user's preferences, the higher the score. Using a "Gaussian proximity function" to calculate the score based on the distance between the song's features and the user's preferences.

Weights for starting (energy=0.35, valence=0.30, danceability=0.20, accousticness=0.15) - these weights can be adjusted based on experimentation.

Example for clarity:
u_energy = 0.40,  u_valence = 0.60,  u_danceability = 0.60,  u_acousticness = 0.75
Song 2 — "Midnight Coding" (0.42, 0.56, 0.62, 0.71)

P(energy)       = exp(-5 × (0.42 - 0.40)²) = exp(-0.002) = 0.998
P(valence)      = exp(-5 × (0.56 - 0.60)²) = exp(-0.008) = 0.992
P(danceability) = exp(-5 × (0.62 - 0.60)²) = exp(-0.002) = 0.998
P(acousticness) = exp(-5 × (0.71 - 0.75)²) = exp(-0.008) = 0.992

Overall Score = 0.35(0.998) + 0.30(0.992) + 0.20(0.998) + 0.15(0.992) = 0.995
exp(x) means e^x, where e is the base of the natural logarithm (approximately 2.71828). 

The exponential function is used to convert the distance between the song's features and the user's preferences into a score that reflects how closely the song matches the user's preferences. The closer the song's features are to the user's preferences, the higher the score will be. Farther away values will be penalized more harshly the farther out they are rather than being penalized linearly, which is why the exponential function is used in this case.