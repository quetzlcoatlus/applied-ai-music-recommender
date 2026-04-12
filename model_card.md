# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Music Master 1.0
 
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration

This music recommender is designed to generate personalized song recommendations based on a user's preferences for various musical features. It assumes that users have specific tastes and preferences that can be quantified on a scale from 0 to 1 for each feature. The recommender is intended for classroom exploration to demonstrate how different scoring logic can impact the recommendations generated for users with varying preferences.

This system shouldn't be used in a real-world application without significant improvements, as it currently has limitations in terms of diversity and fairness in recommendations.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The model uses several features of each song, including genre, mood, energy, valence, danceability, and acousticness. Each user has preferences for these features, which are represented as values between 0 and 1. The model calculates a score for each song by comparing the song's features to the user's preferences. For the energy, valence, danceability, and acousticness features, the model uses a Gaussian proximity function to assign higher scores to songs that are closer to the user's preferences and lower scores to those that are farther away. For the genre and mood features, the model uses a similarity matrix to determine how closely the song's genre and mood match the user's preferences. The overall score for each song is a weighted sum of these components, with the weights adjusted based on experimentation to better capture user preferences.

I changed the UserProfile to include additional features. I also adjusted the weights for each feature in the overall scoring formula to better reflect their importance in the recommendation process. I also implemented a more nuanced similarity matrix for genres and moods to capture the relationships between different musical styles more effectively.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset

The dataset contains a catalog of 20 songs. The genres represented in the dataset include:
- pop
- lofi
- rock
- ambient
- jazz
- synthwave
- indie pop
- classical
- hip hop
- country
- reggae
- metal
- folk
- blues
- world
- latin
- r&b
The moods represented include:
- happy
- chill
- intense
- relaxed
- moody
- focused
- melancholic
- playful
- nostalgic
- dreamy
- triumphant
- wistful
- yearning
- spirited
- celebratory
- romantic

I asked GitHubCopilot to add 10 songs to the original dataset, which had only 10 songs. I aimed to include a wider variety of genres and moods to create a more diverse catalog for the recommender system. However, the dataset still has limitations in terms of representing the full spectrum of musical tastes, as it may not include certain niche genres or moods that some users might prefer. Additionally, the dataset is relatively small, which can limit the diversity of recommendations and may not capture the full range of musical preferences that users might have. Some songs have the only genre or mood in the dataset, which can lead to isolation for users who prefer those genres or moods.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system seems to work well for users with mainstream preferences, such as pop fans, who receive a higher number of high-scoring recommendations due to the dataset's bias towards pop songs and the similarity matrix's connections. The scoring captures the proximity of song features to user preferences effectively, allowing for personalized recommendations based on energy, valence, danceability, and acousticness. For example, a user with moderate preferences for these features receives recommendations that closely match their tastes, which aligns with my intuition about how a music recommender should function. Additionally, the use of a similarity matrix for genres and moods allows for more nuanced recommendations that can capture the relationships between different musical styles, providing users with a broader range of options that still align with their preferences.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Because of the Gaussian proximity function, users with extreme preferences (e.g., energy=0.95 or 0.05) are heavily penalized for any song that does not match their preference closely, leading to very low scores and poor recommendations. This can create a feedback loop where users with niche tastes receive fewer and less relevant recommendations, reinforcing their isolation from the broader music catalog.

Pop fans receive significantly more high-scoring recommendations than fans of less represented genres like classical or metal, due to the dataset's bias towards pop songs and the similarity matrix's connections. This creates a mainstream superiority bias where users with popular tastes are rewarded with better recommendations, while those with niche preferences are penalized.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Others visible in main.py, using the first 3 user profiles:
- pop_happy
- energetic_pop
- chill_lofi

pop_happy user received a high number of recommendations with high scores, which matched my expectations given the dataset's bias towards pop songs and happy moods. Lower energy and higher valence songs were recommended compared to energetic_pop, which aligned with the user's preferences. Higher energy, valence and danceability songs were recommended compared to chill_lofi, which also made sense given the user's profile.

The energetic_pop user also received several high-scoring recommendations, although not as many as the pop_happy user, which was consistent with the fact that energetic songs are less represented in the dataset. Higher energy, valence and danceability songs were recommended compared to chill_lofi, which made sense given the user's profile.

The chill_lofi user received fewer high-scoring recommendations, which was expected due to the limited number of lofi songs and chill moods in the dataset.

In the recommendations, I looked for how closely the songs matched the user's preferences. I was somewhat surprised to see how heavily the scoring penalized users with extreme preferences, leading to very low scores and poor recommendations for those users.

I also ran a simple test where I removed the mood similarity component from the scoring and observed how it affected the recommendations. This helped me understand the impact of mood on the overall scoring.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

To improve the model, I would consider weighing more features to capture a wider range of musical preferences, such as tempo and artist within a larger data set. This could help provide more personalized recommendations that better reflect individual tastes.

I would also work on improving the explainability of the recommendations by providing users with insights into why certain songs were recommended based on their preferences and the features of the songs.

To enhance diversity among the top results, I would implement a diversity ranking rule in the scoring to ensure that the recommended songs are not too similar to each other.

Finally, to handle more complex user tastes, I would consider implementing a more sophisticated user profiling system that can capture multiple dimensions of musical preferences and allow for more nuanced recommendations. E.g. a user might prefer multiple genres or moods, and the model could be designed to accommodate that by allowing users to specify multiple preferences for each feature and adjusting the scoring accordingly.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

My biggest learning moment was understanding how the scoring mechanism could penalize users with extreme preferences, leading to very low scores and poor recommendations for those users. This experience has made me more aware of the importance of considering the underlying data and scoring mechanisms when evaluating music recommendation apps, and it has me curious about how real world systems implement these features and the need for continuous improvement to ensure that these systems provide personalized and diverse recommendations.

To ensure correctness of the AI tool outputs, I had to double check the generated code and outputs against my understanding of the problem and the requirements of the project. It was helpful for identifying blind spots in my design as well as documenting the reasoning behind my design choices.

I also discovered that even a simple dataset can introduce biases that affect the fairness and diversity of recommendations. Still, the recommendations were relatively good for users with mainstream preferences, which was interesting to see how the model's design and dataset can impact the user experience in different ways.

If I were to extend this project, I would consider implementing a more complex user profiling system that can capture multiple dimensions of musical preferences and allow for more nuanced recommendations. I would also explore ways to improve the diversity of recommendations while still maintaining relevance to the user's preferences. Additionally, I would look into ways to make the recommendations more explainable, so I can understand why certain songs were recommended based on user preferences and continually improve the system.