from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from spending.serializers import UserSerializers,ExpenseSerializer
from spending.models import Expense
from spending.permission import IsOwner

from datetime import datetime
from django.db.models import Sum


from spending.ai_service import get_budget_plan




class SignUpView(APIView):

    def post(self,request):

        form_data=request.data

        serializers_inst=UserSerializers(data=form_data)

        if serializers_inst.is_valid():

            cleaned_data =serializers_inst.validated_data

            instance=User.objects.create_user(**cleaned_data)

            serializers_inst =UserSerializers(instance)

            return Response(data=serializers_inst.data)

        else:

            return Response(data=serializers_inst.errors)


class GetMeView(APIView):


    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def get(self,request):


        auth_user =request.user

        instance =User.objects.get(username=auth_user)

        serializer_inst =UserSerializers(instance)

        return Response(data=serializer_inst.data)

class ExpenseListCreateView(APIView):

    # authentication_classes =[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        instance =Expense.objects.filter(owner=request.user)

        serializer_int = ExpenseSerializer(instance,many=True)

        return Response (data= serializer_int.data)



    def post(self,request):


        form_data =request.data

        serializer_inst =ExpenseSerializer(data=form_data)

        if serializer_inst.is_valid():

            serializer_inst.save(owner=request.user)

            return Response(data=serializer_inst.data)

        else:

            return Response(data=serializer_inst.errors)

class ExpenseRetrieveUpdateDeleteView(APIView):


    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwner]

    def get(self,request,pk=None):

      instance =get_object_or_404(Expense,id=pk)

      self.check_object_permissions(request,instance)

      serializer_inst=ExpenseSerializer(instance)

      return Response (data=serializer_inst.data)


    def put(self,request,pk= None):

        instance =get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        form_data =request.data

        serializer_inst =ExpenseSerializer(data=form_data,instance=instance)

        if serializer_inst.is_valid():

            serializer_inst.save()

            return Response(data=serializer_inst.data)

        else:

            return Response (data=serializer_inst.errors)


    def delete(self,request,pk=None):

        instance =get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response ({"message":"deleted....."})


from datetime import datetime

from django.db.models import Sum

class ExpenseSummaryView(APIView):

    authentication_classes =[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data={

            "todays_total":0
        }

        cur_date =datetime.now().date()

        cur_year=datetime.now().year

        cur_month =datetime.now().month

          #monthly summary

        monthly_summary =Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_summary:

            monthly_total =monthly_summary.values("amount").aggregate(total=Sum("amount")).get("total")

            response_data["monthly_total"] =monthly_total


        # today summary

        todays_transactions =Expense.objects.filter(owner=request.user,created_at__date =cur_date)


        if todays_transactions:

            todays_total =todays_transactions.values("amount").aggregate(total=Sum("amount")).get("total")

            category_summary =todays_transactions.values("category").annotate(total=Sum("amount"))


            response_data["todays_total"] =todays_total

            response_data["category_summary"] =category_summary

        return Response(data=response_data)



class BudgetPlanView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data ={
            "monthly_total":0
        }

        cur_date =datetime.now().date()

        cur_month =datetime.now().month

        cur_year =datetime.now().year

        monthly_transactions=Expense.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_transactions:

            monthly_total =monthly_transactions.values("amount").aggregate(total =Sum("amount")).get("total")

            category_summary =monthly_transactions.values("category").annotate(total=Sum("amount"))


            response_data["monthly_total"] =monthly_total

            response_data["category_summary"] =category_summary

            budgetplan=get_budget_plan(response_data)

            response_data ["plan"]=budgetplan

        return Response(data=response_data)
        



    


    












