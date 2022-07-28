from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

from .serializers import BoardSerialzer
from .models import Article as ArticleModel
from user.models import Planet as PlanetModel
from user.models import User as UserModel


class BoardListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        '''
        메인 화면입니다.
        이용가능한 게시판 목록을 출력합니다.

        가입 시 solar only
        입주 완료 후 solar + my planet
        '''
        user = request.user.id
        user_data = UserModel.objects.get(id=user)

        # 관리자일 때
        if user_data.is_admin:
            all_board_list = {}
            all_planets = PlanetModel.objects.all()
            for planet in all_planets:
                name = planet.name
                url = f'board.html?board={planet.id}'
                if name == 'Solar':
                    pass
                else:
                    all_board_list[name] = url
            return Response(all_board_list, status=status.HTTP_200_OK)

        board_list = []

        try: # userinfo 존재
            my_planet = user_data.userinfo.planet
            url = f'board.html?board={my_planet.id}'
            name = my_planet.name
            board_list.append(url)
            board_list.append(name)
            board_list.append(user)

        except: # userinfo 존재하지 않음
            pass

        board_list.append(user_data.nickname)
        return Response(board_list, status=status.HTTP_200_OK)


class BoardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, planet_id):
        '''
        게시글 목록을 조회합니다.

        필요한 정보
        - 글 제목, 작성자, 작성일자, 코멘트 개수, pk(혹은 디테일 페이지 링크?)
        '''
        user = request.user.id
        user_data = UserModel.objects.get(id=user)

        #관리자일 때
        if user_data.is_admin:
            articles = ArticleModel.objects.filter(planet__id=planet_id).order_by('-create_date')
            article_serializer = BoardSerialzer(articles, many=True).data
            return Response(article_serializer, status=status.HTTP_200_OK)

        # 소속 행성 조회를 위한 접근 가능 게시판 리스트
        solar = PlanetModel.objects.get(name="Solar").id
        board_list = [solar]

        try: # userinfo 존재
            my_planet = user_data.userinfo.planet.id
            board_list.append(my_planet)

        except: # userinfo 존재하지 않음
            pass

        if planet_id in board_list:
            articles = ArticleModel.objects.filter(planet__id=planet_id).order_by('-create_date')
            article_serializer = BoardSerialzer(articles, many=True).data
            return Response(article_serializer, status=status.HTTP_200_OK)

        # print(article_serializer.errors)
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, planet_id, keyword):
        '''
        게시글을 검색합니다.
        검색범위: 제목+내용+작성자
        '''
        user = request.user.id
        user_data = UserModel.objects.get(id=user)

        #관리자일 때
        if user_data.is_admin:
            articles = ArticleModel.objects.filter(Q(planet__id=planet_id) & Q (title__icontains=keyword) | Q (content__icontains=keyword) | Q (author__nickname__icontains=keyword)).order_by('-create_date')
            article_serializer = BoardSerialzer(articles, many=True).data
            return Response(article_serializer, status=status.HTTP_200_OK)

        # 소속 행성 조회를 위한 접근 가능 게시판 리스트
        solar = PlanetModel.objects.get(name="Solar").id
        board_list = [solar]

        try: # userinfo 존재
            my_planet = user_data.userinfo.planet.id
            board_list.append(my_planet)

        except: # userinfo 존재하지 않음
            pass

        if planet_id in board_list:
            articles = ArticleModel.objects.filter(Q(planet__id=planet_id) & Q (title__icontains=keyword) | Q (content__icontains=keyword) | Q (author__nickname__icontains=keyword)).order_by('-create_date')
            article_serializer = BoardSerialzer(articles, many=True).data
            print(len(article_serializer))
            if len(article_serializer) == 0:
                return Response({"message": "검색 결과가 없습니다."}, status=status.HTTP_200_OK)

            return Response(article_serializer, status=status.HTTP_200_OK)

        # print(article_serializer.errors)
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    