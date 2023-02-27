from rest_framework.views import APIView, Response, Request, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from .serializers import MovieSerializer
from .models import Movie
from .permissions import CheckProperty
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MovieViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CheckProperty]
    pagination_class = CustomPagination

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        paginated_movies = self.paginate_queryset(movies)

        serializer = MovieSerializer(paginated_movies, many=True)

        to_return = self.get_paginated_response(serializer.data)

        return Response(to_return.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class MovieDetailViews(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CheckProperty]

    def get_movie(self, movie_id):
        try:
            return Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            raise NotFound('Movie not found')

    def get(self, request: Request, movie_id) -> Response:
        movie = self.get_movie(movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, movie_id):
        movie = self.get_movie(movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MovieOrderDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CheckProperty]

    def get_movie(self, movie_id):
        try:
            return Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            raise NotFound('Movie not found')

    def create_movie_order(self, serializer, movie, user):
        serializer.save(user=user, movie=movie)

    def post(self, request: Request, movie_id) -> Response:
        movie = self.get_movie(movie_id)

        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.create_movie_order(serializer, movie, request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)