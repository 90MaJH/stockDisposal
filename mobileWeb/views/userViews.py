import requests
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from ipware.ip import get_ip


#user
@csrf_exempt
def signin(request):
    try:
        ip = get_ip(request)
        #코드 받아오기
        login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'

        client_id = '0740ded9c3a412ea9c59d6aabf872ad3'
        if ip=='127.0.0.1' or ip == 'localhost':
            redirect_uri = 'http://127.0.0.1:8000/oauth'
        elif ip[:3] == '192':
            redirect_uri = 'http://192.168.0.37:8000/oauth'
        else:
            redirect_uri = 'http://www.pocketmarket.site:8000/oauth'

        login_request_uri += 'client_id=' + client_id
        login_request_uri += '&redirect_uri=' + redirect_uri
        login_request_uri += '&response_type=code'

        request.session['client_id'] = client_id
        request.session['redirect_uri'] = redirect_uri

        return redirect(login_request_uri)
    except Exception as ex:
        print('error occured : ', ex)

@csrf_exempt
def signup(request):
    try:
        return render(request, 'mobileWeb/userPages/user/signUp.html')
    except Exception as ex:
        print('error occured : ', ex)

@csrf_exempt
def signout(request):
    try:
        accessToken = request.COOKIES.get('accessToken')
        testRequestData = requests.post(
            'https://kapi.kakao.com/v1/user/logout', headers={'Authorization': f"Bearer {accessToken}"},
        )
        response = redirect(reverse('index'))
        response.delete_cookie('userEmail')
        response.delete_cookie('accessToken')
        return response
    except Exception as ex:
        print('error occured : ', ex)

@csrf_exempt
def profile(request):
    try:
        return render(request, 'mobileWeb/userPages/user/profile.html')
    except Exception as ex:
        print('error occured : ', ex)

@csrf_exempt
def oauth(request):
    try:
        #코드 받아오기

        code = request.GET['code']

        client_id = request.session.get('client_id')
        redirect_uri = request.session.get('redirect_uri')

        # 토큰 받기
        access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"

        access_token_request_uri += "client_id=" + client_id
        access_token_request_uri += "&redirect_uri=" + redirect_uri
        access_token_request_uri += "&code=" + code

        access_token_request_uri_data = requests.get(access_token_request_uri)
        json_data = access_token_request_uri_data.json()
        access_token = json_data['access_token']

        # 프로필 받기
        user_profile_info_uri = "https://kapi.kakao.com/v1/api/talk/profile?access_token="
        user_profile_info_uri += str(access_token)

        user_profile_info_uri_data = requests.get(user_profile_info_uri)
        user_json_data = user_profile_info_uri_data.json()
        userNickName = user_json_data['nickName']
        userProfileImageURL = user_json_data['profileImageURL']
        userThumbnailURL = user_json_data['thumbnailURL']

        # 토큰정보 받기

        testRequestData = requests.get(
            'https://kapi.kakao.com/v2/user/me', headers={'Authorization': f"bearer {access_token}"},
        )
        userEmail = testRequestData.json()['kakao_account']['email']

        #쿠키만들기
        response = redirect(reverse('index'))
        response.set_cookie('userEmail', userEmail)
        response.set_cookie('accessToken', access_token)
        # response.set_cookie('userNickName', userNickName)
        # response.set_cookie('userProfileImage', userProfileImageURL)
        return response
    except Exception as ex:
        print('error occured : ', ex)
