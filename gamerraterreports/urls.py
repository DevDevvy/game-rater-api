from django.urls import path
from .views import GamerWithMostAddedGamesList, Top3ReviewersList, BottomRatedGamesList, CategoryGamesCountList, GamesWithNoPicturesList
from .views import Over5PlayersList, MostReviewedGameList,GamesForChildrenList, TopRatedGamesList

urlpatterns = [
    path('reports/top5', TopRatedGamesList.as_view() ),
    path('reports/bottom5', BottomRatedGamesList.as_view() ),
    path('reports/5plus_players', Over5PlayersList.as_view() ),
    path('reports/category_game_count', CategoryGamesCountList.as_view() ),
    path('reports/most_reviewed', MostReviewedGameList.as_view() ),
    path('reports/top_contributor', GamerWithMostAddedGamesList.as_view() ),
    path('reports/children_games', GamesForChildrenList.as_view() ),
    path('reports/nopics', GamesWithNoPicturesList.as_view() ),
    path('reports/topreviewers', Top3ReviewersList.as_view() ),
]