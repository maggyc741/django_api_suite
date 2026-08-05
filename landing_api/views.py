from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
import datetime


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing"  # Actualiza este nombre si tu colección es diferente
