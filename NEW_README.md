# AI Music Recommender

This repository contains code for an AI-powered music recommendation system. It uses a combination of user preferences and song features in a dataset to generate personalized music recommendations. The system includes a self-iterative agentic workflow that refines the recommendation algorithm to improve the quality of recommendations over time. This matters because it allows for a more personalized and dynamic music recommendation experience, which can lead to increased user satisfaction and engagement.

## Architecture Overview

The input layer consists of user preferences and song features from the dataset. The recommendation engine layer includes scoring rules that evaluate how well each song matches the user's preferences, and a ranking rule that orders the songs based on their scores. The output is a list of recommended songs for the user that is checked for quality and relevance. The system also includes an agentic feedback loop where the quantitative quality metrics of recommended songs are used to refine the recommendation algorithm over time, allowing for continuous improvement in the quality of recommendations. These are then passed to the quality gates where automated tests and checks are performed to ensure that the recommendations meet certain standards before being presented to the user.

## Setup Instructions



## Sample Interactions



## Design Decisions



## Testing Summary



## Reflection



