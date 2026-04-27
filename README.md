# AI Music Recommender

This repository contains code for an AI-powered music recommendation system. It uses a combination of user preferences and song features in a dataset to generate personalized music recommendations. The system includes a self-iterative agentic workflow that refines the recommendation algorithm to improve the quality of recommendations over time. This matters because it allows for a more personalized and dynamic music recommendation experience, which can lead to increased user satisfaction and engagement.

## Project Showcase

[Loom Link](https://www.loom.com/share/3f183c63653b42d1a6c09e9c79661642)

## Architecture Overview

The input layer consists of user preferences and song features from the dataset. The recommendation engine layer includes scoring rules that evaluate how well each song matches the user's preferences, and a ranking rule that orders the songs based on their scores. The output is a list of recommended songs for the user that is checked for quality and relevance. The system also includes an agentic feedback loop where the quantitative quality metrics of recommended songs are used to refine the recommendation algorithm over time, allowing for continuous improvement in the quality of recommendations. These are then passed to the quality gates where automated tests and checks are performed to ensure that the recommendations meet certain standards before being presented to the user.

## Setup Instructions

1. Clone this repository:

```bash
git clone https://github.com/yourusername/ai-music-recommender.git
cd ai-music-recommender
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your environment variable in a `.env` file:

```bash
GEMINI_API_KEY=your_api_key_here
```

5. Run the recommendation system:

```bash
streamlit run app.py
```

## Sample Interactions

### Chill Lofi Profile

![Chill Lofi Input](./assets/input_1.png)
![Chill Lofi Output 1](./assets/output_1.1.png)
![Chill Lofi Output 1](./assets/output_1.2.png)

### Intense Classical Profile

![Intense Classical Input](./assets/input_2.png)
![Intense Classical Output 1](./assets/output_2.1.png)
![Intense Classical Output 2](./assets/output_2.2.png)

## Design Decisions

- Separation of scoring rules and ranking rules: Scoring rules evaluate how well each song matches the user's preferences, while ranking rules order the songs based on their scores. This separation allows for more flexibility in the recommendation system, as different scoring and ranking rules can be easily swapped in and out without affecting the overall architecture.
- Proximity-based scoring rule for quantitative features: This scoring rule assigns a score to a song based on its proximity to the user's preferences in the feature space. The closer the song is to the user's preferences, the higher the score. This allows for a more nuanced evaluation of how well each song matches the user's preferences, rather than just a binary match or mismatch.
- User profile design: The user profile is designed as a dictionary with keys for each feature (energy, mood, valence, danceability, acousticness) and values representing the user's preferences for each feature. This allows for a more flexible and extensible user profile that can easily accommodate additional features in the future. Categorical values are handled using a similarity matrix, which allows for more nuanced recommendations based on genre and mood preferences.
- Agentic feedback loop: The system includes an agentic feedback loop where the quantitative and qualitative metrics of recommended songs are used to refine the recommendation algorithm over time. This allows for continuous improvement in the scoring algorithm, as the system can learn from user interactions and adjust its recommendations accordingly. It uses Gemini's API to analyze data from the PLAN step to improve the scoring algorithm in the CHECK step, which is then viewable by a human to improve the codebase. This iterative process allows for a more dynamic and personalized recommendation experience for the user.

## Testing Summary

- Took several iterations to refine the scoring and ranking rules to produce decent quality recommendations that align with user preferences. Given the the subjective nature of music preferences, it was challenging to achieve great recommendations without user feedback, but the system was able to generate recommendations that were generally in line with what I expected given a set of user preferences after several iterations.
- API calls to Gemini were somewhat successful in analyzing the quality of recommendations and providing feedback for improvement. The algorithm that decides whether Gemini should improve the function is a simple value check which only looks at the top value of the recommendation list, which is a very basic approach and could be improved by looking at a broader range of recommendations and using more sophisticated metrics for evaluation. Additionally, the feedback provided by Gemini was somewhat generic and could be improved by providing more specific suggestions for how to improve the scoring algorithm based on the analysis of the recommendations.
- Human evaluation is used to review the output from Gemini for the function which is critical for the subjective nature of music recommendations. The human evaluation process is somewhat time-consuming and could be improved by developing more efficient ways to review and analyze the recommendations, such as using a larger sample of recommendations or developing a more structured evaluation framework.

## Reflection

The dataset is relatively biased towards certain genres and moods, which can limit the diversity of recommendations. Additionally, the scoring algorithm is based on a simple proximity-based approach, which may not capture all the nuances of user preferences and song features. The agentic feedback loop helped improve the recommendation algorithm over time, but it requires careful human review to ensure that it effectively incorporates user feedback and leads to meaningful improvements in the quality of recommendations over time.

AI could be misused in this context if the recommendation system is designed to manipulate user preferences or promote certain songs or artists over others for commercial gain, rather than providing genuinely personalized recommendations based on user preferences. Additionally, there is a risk of reinforcing existing biases in the dataset, which could lead to a lack of diversity in the recommendations and limit the discovery of new music for users.

I was surprised that the proximity-based scoring rule was able to produce reasonably good recommendations after several iterations of refinement, even without user feedback. I expected that it would be more difficult to achieve good recommendations, but the system was able to generate recommendations that were generally in line with what I expected given a set of user preferences.

AI (Claude) was generally helpful throught the development of this project, particularly in providing feedback for improving the scoring algorithm and code implementation as well as error resolution. However, the feedback provided by Gemini was somewhat generic and could be improved by providing more specific suggestions for how to improve the scoring algorithm based on the analysis of the recommendations.

This project taught me a lot about the design and implementation of a music recommendation system, including how to use user preferences and song features to generate personalized recommendations. I also learned about the importance of separating scoring rules and ranking rules, and how to use a proximity-based scoring rule for quantitative features. Additionally, I gained experience with designing user profiles and implementing an agentic feedback loop to refine the recommendation algorithm over time. 

Overall, this project was a valuable learning experience that has given me a deeper understanding of AI-powered recommendation systems as well as AI-assisted software development. I am excited to continue exploring this area and applying what I have learned to future projects.