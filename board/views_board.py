import django.urls
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

from .serializers import BoardSerialzer
from .models import Article as ArticleModel
from user.models import Planet as PlanetModel
from user.models import User as UserModel
from user.models import UserInfo as UserInfoModel

def is_okay(request, planet_id):
    user = request.user

    if user.is_authenticated:

        if user.is_admin:
            return True
    
        if planet_id == PlanetModel.objects.get(name="Solar").id:
            return True
        
        if planet_id == UserInfoModel.objects.get(id=user.id).planet.id:
            return True

    return False


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

        my_data = {}
        my_data["user_id"] = user
        my_data["nickname"] = user_data.nickname

        if UserInfoModel.objects.filter(user__id=user):
            my_planet = user_data.userinfo.planet
            url = f'/board/board.html?board={my_planet.id}&page=1'
            name = my_planet.name
            id = my_planet.id
            planet_data = [name, id, url]
            my_data["planet_data"] = planet_data

        if user_data.is_admin:
            admin_data = {}
            all_planets = PlanetModel.objects.all()
            for planet in all_planets:
                name = planet.name
                url = f'/board/board.html?board={planet.id}&page=1'
                if name == 'Solar':
                    pass
                else:
                    admin_data[name] = url
                my_data["admin_data"] = admin_data
        
        return Response(my_data, status=status.HTTP_200_OK)


class BoardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, planet_id, page):
        '''
        게시글 목록을 조회합니다.
        '''
        
        if is_okay(request, planet_id):

            cnt = ArticleModel.objects.filter(planet__id=planet_id).count()

            if cnt == 0:
                return Response({"message": "작성된 글이 없어요!"}, status=status.HTTP_200_OK)

            if page == 1:
                start_num = page
                end_num = page *20

            else:
                start_num = (page-1) *20 +1
                end_num = page *20

            if cnt < end_num:
                end_num = start_num + (cnt-start_num)
                                
            articles = ArticleModel.objects.filter(planet__id=planet_id).order_by('-create_date')[start_num-1:end_num]
            article_serializer = BoardSerialzer(articles, many=True).data
            article_serializer[0]["num"] = [i for i in range(start_num, end_num+1)] # 출력할 넘버링
            article_serializer[0]["count"] = cnt # 검색 결과 개수

            return Response(article_serializer, status=status.HTTP_200_OK)

        return Response({"detail": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)


class BoardSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, planet_id, keyword, page):
        '''
        게시글을 검색합니다.
        검색범위: 제목+내용+작성자
        '''

        if is_okay(request, planet_id):

            cnt = ArticleModel.objects.filter(Q (title__icontains=keyword) | Q (content__icontains=keyword) | Q (author__nickname__icontains=keyword) \
                    & Q(planet__id=planet_id)).count()
            if cnt == 0:
                return Response({"message": "작성된 글이 없어요!"}, status=status.HTTP_200_OK)
            
            if page == 1:
                start_num = page
                end_num = page *20

            else:
                start_num = (page-1) *20 +1
                end_num = page *20


            if cnt < end_num:
                end_num = start_num + (cnt-start_num)
                                
            articles = ArticleModel.objects.filter(Q (title__icontains=keyword) | Q (content__icontains=keyword) | Q (author__nickname__icontains=keyword) \
                & Q(planet__id=planet_id)).order_by('-create_date')[start_num-1:end_num]
            article_serializer = BoardSerialzer(articles, many=True).data
            article_serializer[0]["num"] = [i for i in range(start_num, end_num+1)] # 출력할 넘버링
            article_serializer[0]["count"] = cnt # 검색 결과 개수

            return Response(article_serializer, status=status.HTTP_200_OK)

        return Response({"detail": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)







    