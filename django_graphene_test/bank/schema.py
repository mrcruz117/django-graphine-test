import graphene
import graphene_django
from .models import User, TransactionHistory
from django.db import transaction


class UserType(graphene_django.DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class TransactionHistoryType(graphene_django.DjangoObjectType):
    class Meta:
        model = TransactionHistory
        fields = "__all__"



class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    total_users = graphene.Int()
    transaction_history = graphene.List(TransactionHistoryType)
    def resolve_users(self, info):
        return User.objects.all()

    def resolve_total_users(self, info):
        return User.objects.count()

    def resolve_transaction_history(self, info):
        return TransactionHistory.objects.all()


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        age = graphene.Int(required=True)
        balance = graphene.Decimal(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, name, email, age, balance):
        user = User(name=name, email=email, age=age, balance=balance, is_active=True)
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        email = graphene.String()
        age = graphene.Int()
        balance = graphene.Decimal()
        is_active = graphene.Boolean()

    def mutate(self, info, id, name, email, age, balance, is_active):
        user = User.objects.get(id=id)
        user.name = name
        user.email = email
        user.age = age
        user.balance = balance
        user.is_active = is_active
        user.save()
        return UpdateUser(ok=True, user=user)


class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return DeleteUser(ok=True)


class TransferMoney(graphene.Mutation):
    class Arguments:
        from_user_id = graphene.ID(required=True)
        to_user_id = graphene.ID(required=True)
        amount = graphene.Decimal(required=True)

    ok = graphene.Boolean()
    from_user = graphene.Field(UserType)
    to_user = graphene.Field(UserType)

    @transaction.atomic
    def mutate(self, info, from_user_id, to_user_id, amount):
        from_user = User.objects.select_for_update().get(id=from_user_id)
        to_user = User.objects.select_for_update().get(id=to_user_id)

        if from_user.balance < amount:
            raise graphene.GraphQLError("Insufficient funds")

        from_user.balance -= amount
        to_user.balance += amount

        from_user.save()
        to_user.save()

        TransactionHistory.objects.create(
            from_user=from_user, to_user=to_user, amount=amount
        )

        return TransferMoney(ok=True, from_user=from_user, to_user=to_user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    transfer_money = TransferMoney.Field()  # Add this line


schema = graphene.Schema(query=Query, mutation=Mutation)
